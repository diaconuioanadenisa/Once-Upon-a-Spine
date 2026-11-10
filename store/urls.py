from django.urls import path
from . import views

urlpatterns = [path("", views.catalog, name="catalog"), path("product/<slug:slug>/", views.product_detail, name="product_detail"), path("register/", views.register, name="register"), path("newsletter/", views.newsletter_signup, name="newsletter_signup")]
