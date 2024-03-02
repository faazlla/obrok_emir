from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, CollaborationForm, DonationForm, DonationUserForm, EditRestaurantForm
from django.contrib.auth.decorators import login_required
import random, string
from django.shortcuts import get_object_or_404
from .models import NewsItem, Donation, Restaurant 
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Sum, Count

#LOGIN I LOGOUT SISTEM
def home(request):    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
		
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:
        return render(request, 'home.html', {})
    

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')

#Register sistem
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
            
    
    return render(request, 'register.html', {'form':form})


#Kolaboracije - ZA RESTORANE, registrovanje kako bi suradjivali
@login_required
def collaboration(request):
    if request.method == 'POST':
        form = CollaborationForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.user = request.user
            restaurant.save()
            #################################
            create_restaurant_news(restaurant)

            messages.success(request, "You Have Successfully Registered your restaurant! Welcome!")
            return redirect('news')
    else:
        form = CollaborationForm()

    return render(request, 'collaboration.html', {'form': form})

def generate_random_code(length=10):
    """Generiše slučajan kod od zadate dužine."""
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def add_funds(request, restaurant_id, amount):
    """Dodaje određeni iznos novca restoranu i generiše novi kod."""
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    restaurant.available_funds += amount
    restaurant.code = generate_random_code()  # Generisanje novog koda
    restaurant.save()
    return JsonResponse({'message': 'Funds added successfully.'})

def subtract_funds(request, restaurant_id, amount):
    """Oduzima određeni iznos novca iz dostupnih sredstava restorana."""
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    if restaurant.available_funds >= amount:
        restaurant.available_funds -= amount
        restaurant.code = generate_random_code()  # Generisanje novog koda
        restaurant.save()
        return JsonResponse({'message': 'Funds subtracted successfully.'})
    else:
        return JsonResponse({'error': 'Insufficient funds.'}, status=400)

#DONACIJE novcanih sredstava u restorane
@login_required
def donation(request):
    form = DonationForm(request.POST or None)
    if 'city' in request.POST:
        city_id = request.POST['city']
        form.fields['restaurant'].queryset = Restaurant.objects.filter(city_id=city_id)

    if request.method == 'POST' and form.is_valid():
        city_id = form.cleaned_data['city'].id
        restaurant_id = form.cleaned_data['restaurant'].id
        amount = form.cleaned_data['amount']
        restaurant_code = form.cleaned_data['restaurant_code']

        # Provera da li kod odgovara odabranom restoranu
        restaurant = Restaurant.objects.filter(id=restaurant_id, code=restaurant_code).first()
        if restaurant:
            restaurant.add_funds(amount)
            
            donation_instance = Donation.objects.create(user=request.user, restaurant=restaurant, amount=amount)
            create_donation_news(donation_instance)
            
            messages.success(request, f"Successfully donated {amount} BAM to {restaurant.restaurant_name}. Thank you!")
        else:
            messages.error(request, "Invalid restaurant code. Donation failed.")

    return render(request, 'donation.html', {'form': form})

#Filtriranje restorana po odredjenom gradu
def get_restaurants(request, city_id):
    restaurants = list(Restaurant.objects.filter(city_id=city_id).values('id', 'restaurant_name'))
    return JsonResponse({'restaurants': restaurants})

#Korisnik donacija
@login_required
def donation_user(request):
    form = DonationUserForm(request.POST or None)
    if 'city' in request.POST:
        city_id = request.POST['city']
        form.fields['restaurant'].queryset = Restaurant.objects.filter(city_id=city_id)
        
    if request.method == 'POST' and form.is_valid():
        city_id = form.cleaned_data['city'].id
        restaurant_id = form.cleaned_data['restaurant'].id
        amount = form.cleaned_data['amount']
        restaurant_code = form.cleaned_data['restaurant_code']

        # Provera da li kod odgovara odabranom restoranu
        restaurant = Restaurant.objects.filter(id=restaurant_id, code=restaurant_code).first()

        if restaurant and restaurant.city_id == city_id:
            # Provera da li restoran ima dovoljno novca za donaciju
            if restaurant.available_funds >= amount:
                # Ako restoran ima dovoljno novca, smanjujemo iznos sa njegovih sredstava
                restaurant.subtract_funds(amount)
                messages.success(request, f"Successfully used {amount} BAM for donation to {restaurant.restaurant_name}. Thank you!")
            else:
                messages.error(request, "Insufficient funds. Donation failed.")
                restaurant.code = generate_random_code()
                restaurant.save()
        else:
            messages.error(request, "Invalid restaurant code or city. Donation failed.")

    return render(request, 'donation_user.html', {'form': form})

#MOJ PROFIL - Restorani u mom vlasnistvu
@login_required
def user_restaurants(request):
    # Dohvati trenutno logovanog korisnika
    current_user = request.user

    # Filtriraj restorane koji imaju isti user_id kao trenutno logovani korisnik
    user_restaurants = Restaurant.objects.filter(user=current_user)

    # Prosledi listu restorana u template
    return render(request, 'user_restaurants.html', {'user_restaurants': user_restaurants})

#Uredjivanje podataka restorana
@login_required
def edit_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, user=request.user)

    if request.method == 'POST':
        form = EditRestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.error(request, "Uspjesno ste uredili podatke vaseg restorana!")
            return redirect('user_restaurants')
    else:
        form = EditRestaurantForm(instance=restaurant)

    return render(request, 'edit_restaurant.html', {'form': form, 'restaurant': restaurant})


#def news(request):
#    news_items = NewsItem.objects.all().order_by('-created_at')
#    return render(request, 'news.html', {'news_items': news_items})

#Novosti --- Kreiranje donacije, kreiranje restorana
def create_donation_news(donation):
    user = donation.user
    restaurant = donation.restaurant
    NewsItem.objects.create(user=user, news_type='donation', donation=donation, restaurant=restaurant, created_at=timezone.now())

def create_restaurant_news(restaurant):
    user = restaurant.user
    NewsItem.objects.create(user=user, news_type='restaurant', restaurant=restaurant, created_at=timezone.now())

from django.db.models import F, Max
#NEWS PAGE
def news(request):
    # Pronalazimo restoran sa najvećim iznosom dostupnih sredstava
    golden_restaurant = Restaurant.objects.order_by('-available_funds').first()

    # Provjeravamo da li postoji "golden restoran"
    if golden_restaurant:
        # Dohvatimo ime restorana, grad i dostupna sredstva
        restaurant_name = golden_restaurant.restaurant_name
        city = golden_restaurant.city.name
        available_funds = golden_restaurant.available_funds

        # Dohvatimo ostale vijesti iz baze podataka
        news_items = NewsItem.objects.all().order_by('-created_at')
        return render(request, 'news.html', {'news_items': news_items, 'golden_restaurant': {'name': restaurant_name, 'city': city, 'funds': available_funds}})
    else:
        # Ako nema restorana u bazi podataka, prikažemo samo ostale vijesti
        news_items = NewsItem.objects.all().order_by('-created_at')
        return render(request, 'news.html', {'news_items': news_items, 'golden_restaurant': None})

#############################################

#MOJ PROFIL
@login_required
def my_profile(request):
    user = request.user
    donations = Donation.objects.filter(user=user)  # Dohvati sve donacije trenutnog korisnika
    restaurants = Restaurant.objects.filter(user=user)  # Dohvati sve restorane trenutnog korisnika

    total_donated = donations.aggregate(Sum('amount'))['amount__sum'] or 0  # Ukupan iznos donacija
    num_donations = donations.count()  # Broj donacija
    max_donation = donations.aggregate(Max('amount'))['amount__max'] or 0  # Maksimalna donacija

    return render(request, 'myprofile.html', {
        'user': user,
        'donations': donations,
        'restaurants': restaurants,
        'total_donated': total_donated,
        'num_donations': num_donations,
        'max_donation': max_donation
    })

#Profili drugih korisnika
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    donations = Donation.objects.filter(user=profile_user)  # Dohvati sve donacije korisnika
    restaurants = Restaurant.objects.filter(user=profile_user)  # Dohvati sve restorane korisnika
    
    total_donated = donations.aggregate(Sum('amount'))['amount__sum'] or 0  # Ukupan iznos donacija
    num_donations = donations.count()  # Broj donacija
    max_donation = donations.aggregate(Max('amount'))['amount__max'] or 0  # Maksimalna donacija
    
    return render(request, 'userprofile.html', {
        'profile_user': profile_user,
        'donations': donations,
        'restaurants': restaurants,
        'total_donated': total_donated,
        'num_donations': num_donations,
        'max_donation': max_donation
    })


#Search forma
def search_profile(request):
    username = request.GET.get('username')
    if username:
        user = get_object_or_404(User, username=username)
        donations = Donation.objects.filter(user=user)
        restaurants = Restaurant.objects.filter(user=user)
        
        total_donated = donations.aggregate(Sum('amount'))['amount__sum'] or 0  # Ukupan iznos donacija
        num_donations = donations.count()  # Broj donacija
        max_donation = donations.aggregate(Max('amount'))['amount__max'] or 0  # Maksimalna donacija
        
        return render(request, 'userprofile.html', {
            'profile_user': user,
            'donations': donations,
            'restaurants': restaurants,
            'total_donated': total_donated,
            'num_donations': num_donations,
            'max_donation': max_donation
        })
    else:
        return render(request, 'userprofile.html', {'profile_user': None, 'donations': None, 'restaurants': None})
