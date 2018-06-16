from django.shortcuts import render
from .models import Car, Review, Renter, Rent
from .forms import ReviewForm, RentForm, RenterForm, CarForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import datetime
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

def index(request):

    if request.method == 'GET':
        if 'clas_type' in request.GET and request.GET['clas_type']:
            cars = Car.objects.filter(clas=request.GET['clas_type'])
            context = {'cars': cars, }
            return render(request, 'auto/index.html', context)
        if 'trans_type' in request.GET and request.GET['trans_type']:
            cars = Car.objects.filter(transmission=request.GET['trans_type'])
            context = {'cars': cars, }
            return render(request, 'auto/index.html', context)
        if 'body_type' in request.GET and request.GET['body_type']:
            cars = Car.objects.filter(body=request.GET['body_type'])
            context = {'cars': cars, }
            return render(request, 'auto/index.html', context)
        if 'price' in request.GET and request.GET['price']:
            cars = Car.objects.all().order_by(request.GET['price'])
            context = {'cars': cars, }
            return render(request, 'auto/index.html', context)
        else:
            cars = Car.objects.all()
            context = {'cars': cars, }
            return render(request, 'auto/index.html', context)


def about_car(request, c_id):
    car = Car.objects.get(pk=c_id)
    reviews = Review.objects.filter(car=c_id)
    if request.method == "POST":
        if 'new_price' in request.POST and request.POST['new_price'] and request.user.is_authenticated:
            Car.objects.filter(pk=c_id).update(price_day=request.POST['new_price'])
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            review = review_form.save()
            review.car = car
            review.publication_date = datetime.datetime.today()
            review.save()
        else:
            print(review_form.errors)
    else:
        review_form = ReviewForm(initial={'car': car, 'publication_date': datetime.datetime.today()})
    return render(request, 'auto/about_car.html', context={'review_form': review_form, 'car': car, 'reviews': reviews, })

def rent_car(request):
    rented = False
    if request.method == "POST":
        renter_form = RenterForm(data=request.POST)
        rent_form = RentForm(data=request.POST)
        if renter_form.is_valid() and rent_form.is_valid():

            renter = renter_form.save()
            renter.save()
            r = Renter.objects.get(pk=renter.pk)
            rent = rent_form.save(commit=False)
            car = Car.objects.get(pk=rent.car.pk)
            rent.renter = r
            total = rent.day_end - rent.day_start
            rent.price = total.days * car.price_day
            rent.save()

            rented = True
        else:
            print(renter_form.errors, rent_form.errors)
    else:
        renter_form = RenterForm()
        rent_form = RentForm(initial={'renter': 1, 'manager': 1, })


    return render(request, 'auto/rent.html', {'renter_form': renter_form, 'rent_form': rent_form, 'rented': rented, })

def rent_car_def(request, c_id):
    rented = False
    car = Car.objects.get(pk=c_id)
    if request.method == "POST":
        renter_form = RenterForm(data=request.POST)
        rent_form = RentForm(data=request.POST)
        if renter_form.is_valid() and rent_form.is_valid():

            renter = renter_form.save()
            renter.save()
            r = Renter.objects.get(pk=renter.pk)
            rent = rent_form.save(commit=False)
            rent.renter = r
            total = rent.day_end - rent.day_start
            rent.price = total.days * car.price_day
            rent.save()

            rented = True
        else:
            print(renter_form.errors, rent_form.errors)
    else:
        renter_form = RenterForm()
        rent_form = RentForm(initial={'car': car, 'renter': 1, 'manager': 1, })

    return render(request, 'auto/rent_id.html', {'renter_form': renter_form, 'rent_form': rent_form, 'rented': rented, 'car': car, })

def stats_id(request, c_id):
    car = Car.objects.get(pk=c_id)
    rents = Rent.objects.filter(car=c_id)
    return render(request, 'auto/stats_id.html', {'rents': rents, 'car': car, })

def stats(request):
    cars = Car.objects.all()
    sums = Rent.objects.raw('SELECT Distinct 1 as id, car_id, sum(price) over(partition by car_id) as sum_price FROM auto_rent')
    return render(request, 'auto/stats.html', {'cars': cars, 'sums': sums, })

def contr_infos(request):
    return render(request, 'auto/contr_infos.html')

@login_required
def add_car(request):
    if request.user.is_authenticated:
        added = False
        if request.method == "POST":
            car_form = CarForm(data=request.POST)
            if car_form.is_valid():
                car = car_form.save()
                car.save()
                added = True
            else:
                print(car_form.errors, car_form.errors)
        else:
            car_form = CarForm()
        return render(request, 'auto/add_car.html', {'car_form': car_form, 'added': added})
    else:
        return render(request, 'auto/add_car.html', {'wrong': 'Something goes wrong!'})

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return redirect('index')
            else:
                return ValidationError('Account not active')
        else:
            print("Username: {} and password {}".format(username,password))
            return ValidationError("invalid login details supplied!")
    else:
        return render(request, 'auto/login.html')