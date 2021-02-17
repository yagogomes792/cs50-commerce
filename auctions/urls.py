from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('listing', views.listing, name='listing'),
    path('new_listing', views.new_listing, name='new_listing'),
    path('category/<str:category>', views.category, name='category'),
    path('categories', views.categories, name='categories'),
    path('view_listing/<int:product_id>', views.view_listing, name='view_listing'),
    path('watchlist/<int:product_id>', views.watchlist, name='watchlist'),
    path('addcomment/<int:product_id>', views.addcomment, name='addcomment'),
    path('closebid/<int:product_id>', views.closebid, name='closebid'),
    path('closelisting', views.closelisting, name='closelisting'),
    path('info', views.info, name='info'),
]
