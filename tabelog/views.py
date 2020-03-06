from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView

from .models import Pref, Category, Review
from .forms import SearchForm, SignUpForm, LoginForm, ReviewForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Avg
from django.contrib import messages
import json
import requests


def get_keyid():
    return "e69b765feb7e3902bdc22e281874aa97"


class IndexView(TemplateView):
    template_name = 'tabelog/index.html'
    # template_name = 'tabelog/test.html'

    def get_context_data(self, *args, **kwargs):
        searchform = SearchForm()
        
        query = get_gnavi_data("", "RSFST09000", "", "花見", 12)
        res_list = rest_search(query)
        pickup_list = extract_restaurant_info(res_list)
        review_list = Review.objects.all()[:10]

        params = {
            'searchform': searchform,
            'pickup_list': pickup_list,
            'review_list': review_list
            }
        return params


def Search(request):
    if request.method == 'GET':
        searchform = SearchForm(request.POST)

        if searchform.is_valid():
            category_l = request.GET['category_l']
            pref = request.GET['pref']
            freeword = request.GET['freeword']
            query = get_gnavi_data("", category_l, pref, freeword, 10)
            res_list = rest_search(query)
            total_hit_count = len(res_list)
            restaurants_info = extract_restaurant_info(res_list)

    params = {
        'total_hit_count': total_hit_count,
        'restaurants_info': restaurants_info,
    }

    return render(request, 'tabelog/search.html', params)


def get_gnavi_data(id, category_l, pref, freeword, hit_per_page):
    keyid = get_keyid()
    hit_per_page = hit_per_page
    id = id
    category_l = category_l
    pref = pref
    freeword = freeword
    # 今回は関東地方のみ（コール回数を少なくするため）
    area = "AREA110"
    query = {"keyid": keyid, "id": id, "area": area, "pref": pref,
             "category_l": category_l, "hit_per_page": hit_per_page, "freeword": freeword}

    return query


def rest_search(query):
    res_list = []
    res = json.loads(requests.get("https://api.gnavi.co.jp/RestSearchAPI/v3/", params=query).text)
    if "error" not in res:
        res_list.extend(res["rest"])
    return res_list


def extract_restaurant_info(restaurants: 'restaurant response') -> 'restaurant list':
    restaurant_list = []
    for restaurant in restaurants:
        id = restaurant["id"]
        name = restaurant["name"]
        name_kana = restaurant["name_kana"]
        latitude = restaurant["latitude"]
        longitude = restaurant["longitude"]
        url = restaurant["url"]
        url_mobile = restaurant["url_mobile"]
        shop_image1 = restaurant["image_url"]["shop_image1"]
        shop_image2 = restaurant["image_url"]["shop_image2"]
        qrcode = restaurant["image_url"]["qrcode"]
        address = restaurant["address"]
        tel = restaurant["tel"]
        opentime = restaurant["opentime"]
        holiday = restaurant["holiday"]
        station_line = restaurant["access"]["line"]
        station = restaurant["access"]["station"]
        station_exit = restaurant["access"]["station_exit"]
        walk = restaurant["access"]["walk"]
        parking_lots = restaurant["parking_lots"]
        pr_short = restaurant["pr"]["pr_short"]
        pr_long = restaurant["pr"]["pr_long"]
        budget = restaurant["budget"]
        party = restaurant["party"]
        lunch = restaurant["lunch"]
        credit_card = restaurant["credit_card"]
        e_money = restaurant["credit_card"]

        restaurant_list.append([id, name, name_kana, url, url_mobile, shop_image1,
                                shop_image2, address, tel, station_line, station, latitude, longitude, pr_long])
    return restaurant_list


def ShopInfo(request, restid):
    keyid = get_keyid()
    id = restid
    query = get_gnavi_data(id, "", "", "", 1)
    res_list = rest_search(query)
    restaurants_info = extract_restaurant_info(res_list)
    review_count = Review.objects.filter(shop_id=restid).count()
    score_ave = Review.objects.filter(shop_id=restid).aggregate(Avg('score'))
    average = score_ave['score__avg']
    if average:
        average_rate = average / 5 * 100
    else:
        average_rate = 0

    if request.method == 'GET':
        review_form = ReviewForm()
        review_list = Review.objects.filter(shop_id=restid)
    else:
        form = ReviewForm(data=request.POST)
        score = request.POST['score']
        comment = request.POST['comment']

        if form.is_valid():
            review = Review()
            review.shop_id = restid
            review.shop_name = restaurants_info[0][1]
            review.image_url = restaurants_info[0][5]
            review.user = request.user
            review.score = score
            review.comment = comment
            is_exist = 0
            is_exist = Review.objects.filter(shop_id = review.shop_id).filter(user = review.user).count()
            
            if not is_exist == 0:
                messages.error(request, '既にレビューを投稿済みです。')
                return redirect('tabelog:shop_info', restid)
            else:
                review.save()
                messages.success(request, 'レビューを投稿しました。')
                return redirect('tabelog:shop_info', restid)
        else:
            messages.error(request, 'エラーがあります。')
            return redirect('tabelog:shop_info', restid)
        return render(request, 'tabelog/index.html', {})

    params = {
        'title': '店舗詳細',
        'review_count': review_count,
        'restaurants_info': restaurants_info,
        'review_form': review_form,
        'review_list': review_list,
        'average': average,
        'average_rate': average_rate,
    }

    return render(request, 'tabelog/shop_info.html', params)


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'tabelog/signup.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('tabelog:index')
        return render(request, 'tabelog/signup.html', {'form': form})


class Login(LoginView):
    form_class = LoginForm
    template_name = 'tabelog/login.html'


class Logout(LogoutView):
    template_name = 'tabelog/logout.html'
