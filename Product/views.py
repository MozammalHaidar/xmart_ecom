from django.shortcuts import render
from .models import SliderItem

def product(request):
    return render(request, 'product/product.html') 

def slider(request):
    sliders = SliderItem.objects.all()
    return render(request, 'home/home.html', {'sliders': sliders})  
