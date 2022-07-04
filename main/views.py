from django import shortcuts
from django.contrib import auth, messages
from django.contrib.auth import decorators
from django.contrib.auth import forms as auth_forms
from django.core import paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect

from . import constants
from . import forms
from . import models


def landing(request):
    return shortcuts.render(request, 'landing.html')


def search_vehicle(request):
    vehicle_type = request.GET.get('type')
    m = constants.get_model(vehicle_type)
    company_list = [
        x['company_name_id'] for x in m.objects.values('company_name_id').distinct()
    ]
    search_params = {'company_name_id', 'name', 'start_price', 'end_price', 'sort_by'}
    values = {x: request.GET.get(x) for x in search_params}
    args = {'price__gte': values['start_price'], 'price__lte': values['end_price']}
    if values['company_name_id']:
        args['company_name_id'] = values['company_name_id']
    if values['name']:
        args['name__icontains'] = values['name']
    data = m.objects.filter(**args).order_by(values['sort_by'])
    sort_crit = {'Default': 'vehicle_id', 'Price': 'price', 'Rating': 'rating'}
    page = request.GET.get('page', 1)
    pg = paginator.Paginator(data, 9)
    try:
        vol = pg.page(page)
    except paginator.PageNotAnInteger:
        vol = pg.page(1)
    except paginator.EmptyPage:
        vol = pg.page(pg.num_pages)
    return shortcuts.render(request, 'search_vehicle.html',
                            values | {'type': vehicle_type, 'sort_crit': sort_crit, 'data': vol,
                                      'company_list': company_list, 'user': request.user})


def signup(request):
    if request.user.is_authenticated:
        return shortcuts.render(request, 'landing.html', {'alert': 'You are already logged in!'})
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.customer.contact = form.cleaned_data.get('contact')
            user.customer.save()
            user.refresh_from_db(
            )  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = auth.authenticate(username=user.username, password=raw_password)
            auth.login(request, user)
            return shortcuts.redirect('landing')
    else:
        form = forms.SignUpForm()
    return shortcuts.render(request, 'signup.html', {'form': form})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def login(request):
    if request.user.is_authenticated:
        return shortcuts.redirect('landing')
    if request.method == "POST":
        form = auth_forms.AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return shortcuts.redirect('landing')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    form = auth_forms.AuthenticationForm()
    return shortcuts.render(request=request, template_name="login.html", context={'login_form': form})


@decorators.login_required(login_url='/login/')
def favourites(request):
    temp = models.Favourite.objects.filter(user_id=request.user.customer)
    data = [constants.get_type(x.vehicle_id) for x in temp]
    print(request.user)
    page = request.GET.get('page', 1)
    pg = paginator.Paginator(data, 9)
    try:
        vol = pg.page(page)
    except paginator.PageNotAnInteger:
        vol = pg.page(1)
    except paginator.EmptyPage:
        vol = pg.page(pg.num_pages)
    return shortcuts.render(request, 'favourites.html', {'data': vol})


def vehicle(request):
    vehicle_type = request.GET.get('type')
    vehicle_id = request.GET.get('vehicle_id')
    m = constants.get_model(vehicle_type)
    item = m.objects.filter(vehicle_id=vehicle_id)
    item[0].nvis += 1
    item[0].save()
    variants = None
    try:
        variants = m.objects.filter(model_name=item[0].model_name)
    except:
        pass        
    titles = constants.get_titles(vehicle_type)
    vals = {x: (item.values()[0][x],) + titles[x] for x in titles}
    reviews = models.Review.objects.filter(vehicle_id=vehicle_id)
    f = any(x.content for x in reviews)
    return shortcuts.render(request, 'vehicle.html', {'type': vehicle_type,
                                                      'variants': variants,
                                                      'item': item[0],
                                                      'vals': vals,
                                                      'reviews': reviews, 'f': f})


def remove_fav(request):
    vehicle_id = models.Vehicle.objects.get(vehicle_id=request.GET.get('vehicle_id'))
    models.Favourite.objects.get(user_id=request.user.customer, vehicle_id=vehicle_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_fav(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Login is required')
        return shortcuts.redirect('login')
    vehicle_id = models.Vehicle.objects.get(vehicle_id=request.GET.get('vehicle_id'))
    try:
        models.Favourite.objects.create(user_id=request.user.customer, vehicle_id=vehicle_id)
    except IntegrityError:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_review(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Login is required')
        return shortcuts.redirect('login')
    vehicle_id = models.Vehicle.objects.get(vehicle_id=request.POST.get('vehicle_id'))
    rating = int(request.POST.get('rating'))
    commented = request.POST.get('commentcheck')
    try:
        models.Review.objects.create(user_id=request.user.customer, vehicle_id=vehicle_id,
        content=(request.POST.get('review') if commented else None), rating=rating)
        vehicle_id.rating = (vehicle_id.rating * vehicle_id.nrated + rating) / (vehicle_id.nrated + 1)
        vehicle_id.nrated += 1
        vehicle_id.save()
    except IntegrityError:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def about(request):
    return shortcuts.render(request, 'about.html')