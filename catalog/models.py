from django.db import models

# Create your models here.
class Category(models.Model):
  """A top-level product grouping shown as a filter chip (e.g. Cut Vegetables)."""
  name = models.CharField(max_length=100)
  slug = models.SlugField(unique=True)

  class Meta:
        verbose_name_plural = "categories"

  def __str__(self):
        return self.name

class Product(models.Model):
    """A single sellable item — a pack of cut fruit, a veg mix, a cooking kit."""
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    weight_label = models.CharField(max_length=50, help_text="e.g. '250 g', '1 kg'")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name