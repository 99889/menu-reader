# menus/urls.py
from django.urls import path
from .views import upload_image, get_restaurants, get_menus, get_menu_items

urlpatterns = [
    path('upload/', upload_image, name='upload_image'),
    path('restaurants/', get_restaurants, name='get_restaurants'),
    path('restaurants/<int:restaurant_id>/menus/', get_menus, name='get_menus'),
    path('menus/<int:menu_id>/items/', get_menu_items, name='get_menu_items'),
]
