from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)
    description = models.CharField(max_length=180, blank=True)
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"
    def __str__(self):
        return self.name

class Product(models.Model):
    class Kind(models.TextChoices):
        NEW = "new", "New book"
        PREOWNED = "preowned", "Pre-owned book"
        BOOKMARK = "bookmark", "Bookmark"
        ACCESSORY = "accessory", "Accessory"
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.CharField(max_length=120, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    kind = models.CharField(max_length=16, choices=Kind.choices)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    cover_color = models.CharField(max_length=7, default="#7B5144", help_text="Hex colour used for the illustrated cover.")
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-featured", "title"]
    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:185]
            candidate, suffix = base, 2
            while Product.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate, suffix = f"{base}-{suffix}", suffix + 1
            self.slug = candidate
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})
    def __str__(self):
        return self.title
