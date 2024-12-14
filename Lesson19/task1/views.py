from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from .forms import UserRegister
from .models import *


def sign_up_by_django(request):
    info = {}
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            age = form.cleaned_data['age']
            # Проверяем, существует ли пользователь
            try:
                Buyer.objects.get(name=name)
                info['error'] = "Пользователь с таким именем уже существует"
            except Buyer.DoesNotExist:
                # Создаем пользователя, если его нет
                new_buyer = Buyer.objects.create(name=name, balance=5000, age=age)
                return HttpResponseRedirect('success/')
        else:
            info['error'] = form.errors.as_text()
    else:
        form = UserRegister()
        info['form'] = form
    # Получаем всех покупателей из базы данных
    buyers = Buyer.objects.all()
    info['buyers'] = buyers  # Передаем покупателей в шаблон
    return render(request, 'first_task/reg_page.html', {'info': info})


def success(request):
    return render(request, 'first_task/success_page.html')


def main_pg_view(request):
    title = 'SirCianid Games'
    text0 = 'Главная страница'
    context = {
        'title': title,
        'text0': text0,
    }
    return render(request, 'first_task/menu.html', context)


def games_shp_page(request):
    title = 'Наш Магазин'
    text0 = 'Каталог Игр:'
    text1 = 'Быстрая покупка'
    text2 = 'Добавить в корзину'
    games = Game.objects.all()
    context = {
        'title': title,
        'text0': text0,
        'text1': text1,
        'text2': text2,
        'games': games
    }
    return render(request, 'first_task/games.html', context)


def cart_page(request):
    title = 'Ваша Корзина Товаров'
    text0 = 'Корзина: '
    text1 = 'Похоже, в вашей корзине еще нет товаров. Нужно это исправить!'
    context = {
        'title': title,
        'text0': text0,
        'text1': text1
    }
    return render(request, 'first_task/cart.html', context)


def news_page(request):
    news = News.objects.all().order_by('-date')
    paginator = Paginator(news, 4)
    page_num = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'first_task/news.html', {'page_obj': page_obj})
