from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="Category", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=80, unique=True)), ("slug", models.SlugField(max_length=90, unique=True)), ("description", models.CharField(blank=True, max_length=180))], options={"ordering": ["name"], "verbose_name_plural": "categories"}),
        migrations.CreateModel(name="Product", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("title", models.CharField(max_length=180)), ("slug", models.SlugField(blank=True, max_length=200, unique=True)), ("author", models.CharField(blank=True, max_length=120)), ("kind", models.CharField(choices=[("new", "New book"), ("preowned", "Pre-owned book"), ("bookmark", "Bookmark"), ("accessory", "Accessory")], max_length=16)), ("description", models.TextField()), ("price", models.DecimalField(decimal_places=2, max_digits=8)), ("stock", models.PositiveIntegerField(default=1)), ("cover_color", models.CharField(default="#7B5144", help_text="Hex colour used for the illustrated cover.", max_length=7)), ("featured", models.BooleanField(default=False)), ("created_at", models.DateTimeField(auto_now_add=True)), ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="products", to="store.category"))], options={"ordering": ["-featured", "title"]}),
    ]
