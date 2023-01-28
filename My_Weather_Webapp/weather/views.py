from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm
# Create your views here.
def index(request):
   
   
    err_msg = ''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
               
                url = "https://api.openweathermap.org/data/2.5/weather?APPID=2a9ce9ecca5ad85a5346c73b74d78712&q=" + new_city
                r = requests.get(url).json()
               
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist!'
            else:
                err_msg = 'City already exists!'
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added Successfully!'
            message_class = 'is_success'
    
    form = CityForm()
    cities = City.objects.all()
    
    weather_data = []
    for city in cities:
        print(city.name)
        urls = "https://api.openweathermap.org/data/2.5/weather?APPID=2a9ce9ecca5ad85a5346c73b74d78712&q=" + city.name
        print(urls)
        r = requests.get(urls).json()
        print(r)
        city_weather = {
            'city' : city.name,
            'temperature' : round(r['main']['temp'] - 273.15,2),
            'max' : r['main']['temp_max'],
            'min' : r['main']['temp_min'],           
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)
    context = {
        'weather_data' : weather_data, 
        'form' : form,
        'message' : message,
        'message_class' : message_class
        }
    return render(request,'weather/weather.html', context)
def delete_city(requests, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
