from django.db import models


class Category(models.Model):
    """
    Product categories like homeware, dining, or jewellery holders.
    """
    name = models.CharField(max_length=150)
    display_name = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.display_name or self.name

    def get_display_name(self):
        return self.display_name or self.name


class Product(models.Model):
    """
    Represents a product in the store.
    """
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products"
    )
    sku = models.CharField(max_length=100, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)


    def __str__(self):
        return self.name