# menus/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from PIL import Image
import pytesseract

from .models import Restaurant, Menu, MenuItem
from .forms import UploadImageForm

def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_file_url = fs.url(filename)
            items = ocr_image(fs.path(filename))
            # Save items to database (for demo purposes, assuming a single restaurant and menu)
            restaurant, _ = Restaurant.objects.get_or_create(name="Sample Restaurant", address="Sample Address")
            menu, _ = Menu.objects.get_or_create(restaurant=restaurant, category="Sample Category")
            for name, price in items:
                MenuItem.objects.create(menu=menu, name=name, price=price)
            return JsonResponse({'items': items})
    else:
        form = UploadImageForm()
    return render(request, 'upload.html', {'form': form})

def ocr_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return parse_menu_text(text)

def parse_menu_text(text):
    lines = text.split('\n')
    items = []
    for line in lines:
        if '₹' in line:
            item, price = line.rsplit('₹', 1)
            items.append((item.strip(), price.strip()))
    return items

def get_restaurants(request):
    restaurants = Restaurant.objects.all()
    data = [{"id": r.id, "name": r.name, "address": r.address} for r in restaurants]
    return JsonResponse(data, safe=False)

def get_menus(request, restaurant_id):
    menus = Menu.objects.filter(restaurant_id=restaurant_id)
    data = [{"id": m.id, "category": m.category} for m in menus]
    return JsonResponse(data, safe=False)

def get_menu_items(request, menu_id):
    items = MenuItem.objects.filter(menu_id=menu_id)
    data = [{"name": i.name, "price": i.price} for i in items]
    return JsonResponse(data, safe=False)
