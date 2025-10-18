/*
  Cloudberry Clay Stripe Elements Integration
*/

console.log("Stripe Elements loaded");

const stripePublicKey = JSON.parse(document.getElementById('id_stripe_public_key').textContent);
const clientSecret = JSON.parse(document.getElementById('id_client_secret').textContent);

const stripe = Stripe(stripePublicKey);
const elements = stripe.elements();

const style = {
  base: {
    color: '#333',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSize: '16px',
    '::placeholder': { color: '#aab7c4' },
  },
  invalid: {
    color: '#dc3545',
    iconColor: '#dc3545',
  },
};

const card = elements.create('card', {
  style,
  hidePostalCode: true, // Hide Stripe's default ZIP field
});
card.mount('#card-element');

card.on('change', function (event) {
  const errorDiv = document.getElementById('card-errors');
  if (event.error) {
    errorDiv.innerHTML = `<i class="fas fa-times text-danger"></i> ${event.error.message}`;
  } else {
    errorDiv.textContent = '';
  }
});

const form = document.getElementById('payment-form');
const submitBtn = document.getElementById('submit-button');
const overlay = document.getElementById('loading-overlay');

form.addEventListener('submit', function (e) {
  e.preventDefault();

  // Disable inputs and show overlay
  submitBtn.disabled = true;
  card.update({ disabled: true });
  overlay.style.display = 'flex';

  stripe.confirmCardPayment(clientSecret, {
    payment_method: {
      card: card,
    },
  })
  .then(function (result) {
    if (result.error) {
      const errorDiv = document.getElementById('card-errors');
      errorDiv.innerHTML = `<i class="fas fa-times text-danger"></i> ${result.error.message}`;
      overlay.style.display = 'none';
      submitBtn.disabled = false;
      card.update({ disabled: false });
    } else if (result.paymentIntent.status === 'succeeded') {
      form.submit();
    }
  })
  .catch(function (error) {
    console.error("Stripe JS error:", error);
    overlay.style.display = 'none';
    const errorDiv = document.getElementById('card-errors');
    errorDiv.textContent = 'Something went wrong, please try again.';
    submitBtn.disabled = false;
    card.update({ disabled: false });
  });
});
