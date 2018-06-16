from django import forms
from .models import Review, Renter, Rent, Car
from django.utils import timezone

class ReviewForm(forms.ModelForm):
    publication_date = forms.DateTimeField(widget=forms.HiddenInput(), required=False, initial=timezone.localtime(timezone.now()))
    text = forms.CharField(widget=forms.TextInput(attrs={'size': '115%'}))
    class Meta:
        model = Review
        fields = ['car', 'publication_date', 'author_name', 'text']

class RenterForm(forms.ModelForm):
    class Meta:
        model = Renter
        fields = ['full_name', 'email', 'phone', 'age', 'passport', 'driving_experience']


class RentForm(forms.ModelForm):

    day_start = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='День начала')
    day_end = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='День окончания')
    start_time = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}), label='Время начала')
    end_time = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}), label='Время окончания')
    pickup_point = forms.CharField(label='Место подачи')
    return_point = forms.CharField(label='Место возврата')
    class Meta:
        model = Rent
        fields = ['renter', 'car', 'manager', 'day_start', 'start_time', 'pickup_point',
                  'day_end', 'end_time', 'return_point', 'notes']

class CarForm(forms.ModelForm):
    body = forms.ChoiceField(widget=forms.Select(), choices=([('Седан', 'Седан'),
                                                              ('Внедорожник', 'Внедорожник'),
                                                              ('Купе', 'Купе'),
                                                              ('Минивен', 'Минивен'), ]))

    clas = forms.ChoiceField(widget=forms.Select(), choices=([('Бюджетные', 'Бюджетные'),
                                                              ('Внедорожники', 'Внедорожники'),
                                                              ('Комфорт', 'Комфорт'),
                                                              ('Премиум', 'Премиум'), ]))

    transmission = forms.ChoiceField(widget=forms.Select(), choices=([('Автомат', 'Автомат'),
                                                              ('Ручная', 'Ручная'), ]))
    date_of_registration = forms.DateField(widget=forms.HiddenInput(), required=False,
                                     initial=timezone.localtime(timezone.now()).date())
    class Meta:
        model = Car
        fields = ['mark', 'model', 'body', 'licence_plate', 'transmission', 'clas',
                  'release_year', 'engine_capacity', 'passengers', 'price_day', 'photo' ]