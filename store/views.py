from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import RegisterForm
from .models import Category, Product

def catalog(request):
    products = Product.objects.select_related("category").all()
    category, query, kind = request.GET.get("category", ""), request.GET.get("q", "").strip(), request.GET.get("type", "")
    if category:
        products = products.filter(category__slug=category)
    if kind in Product.Kind.values:
        products = products.filter(kind=kind)
    if query:
        products = products.filter(Q(title__icontains=query) | Q(author__icontains=query) | Q(description__icontains=query))
    return render(request, "store/catalog.html", {"products": products, "categories": Category.objects.all(), "active_category": category, "active_kind": kind, "query": query, "result_count": products.count()})

def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug)
    related = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]
    return render(request, "store/product_detail.html", {"product": product, "related": related})

def register(request):
    if request.user.is_authenticated:
        return redirect("catalog")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your account is ready. Please sign in to continue.")
        return redirect("login")
    return render(request, "registration/register.html", {"form": form})

@require_POST
def newsletter_signup(request):
    if request.POST.get("email", "").strip():
        messages.success(request, "Thanks for joining our reading list!")
    return redirect("catalog")
