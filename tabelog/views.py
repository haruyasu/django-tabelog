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
    # template_name = 'tabelog/index.html'
    template_name = 'tabelog/test.html'

    def get_context_data(self, *args, **kwargs):
        searchform = SearchForm()
        category_l = "RSFST09000" # 居酒屋
        pref = "PREF13" # 東京都
        freeword = "歓送迎会"
        num = 9
        
        query = get_gnavi_data(
            "",
            category_l,
            pref,
            freeword,
            num
        )
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
            num = 10
            lunch = request.GET['lunch']
            no_smoking = request.GET['no_smoking']
            card = request.GET['card']
            mobilephone = request.GET['mobilephone']
            bottomless_cup = request.GET['bottomless_cup']
            sunday_open = request.GET['sunday_open']
            takeout = request.GET['takeout']
            private_room = request.GET['private_room']
            midnight = request.GET['midnight']
            parking = request.GET['parking']
            memorial_service = request.GET['memorial_service']
            birthday_privilege = request.GET['birthday_privilege']
            betrothal_present = request.GET['betrothal_present']
            kids_menu = request.GET['kids_menu']
            outret = request.GET['outret']
            wifi = request.GET['wifi']
            microphone = request.GET['microphone']
            buffet = request.GET['buffet']
            late_lunch = request.GET['late_lunch']
            sports = request.GET['sports']
            until_morning = request.GET['until_morning']
            lunch_desert = request.GET['lunch_desert']
            projecter_screen = request.GET['projecter_screen']
            with_pet = request.GET['with_pet']
            deliverly = request.GET['deliverly']
            special_holiday_lunch = request.GET['special_holiday_lunch']
            e_money = request.GET['e_money']
            caterling = request.GET['caterling']
            breakfast = request.GET['breakfast']
            desert_buffet = request.GET['desert_buffet']
            lunch_buffet = request.GET['lunch_buffet']
            bento = request.GET['bento']
            lunch_salad_buffet = request.GET['lunch_salad_buffet']
            darts = request.GET['darts']
            web_reserve = request.GET['web_reserve']
            query = get_gnavi_data(
                "",
                category_l,
                pref,
                freeword,
                num,
                lunch,
                no_smoking,
                card,
                mobilephone,
                bottomless_cup,
                sunday_open,
                takeout,
                private_room,
                midnight,
                parking,
                memorial_service,
                birthday_privilege,
                betrothal_present,
                kids_menu,
                outret,
                wifi,
                microphone,
                buffet,
                late_lunch,
                sports,
                until_morning,
                lunch_desert,
                projecter_screen,
                with_pet,
                deliverly,
                special_holiday_lunch,
                e_money,
                caterling,
                breakfast,
                desert_buffet,
                lunch_buffet,
                bento,
                lunch_salad_buffet,
                darts,
                web_reserve
            )
            res_list = rest_search(query)
            total_hit_count = len(res_list)
            restaurants_info = extract_restaurant_info(res_list)

    params = {
        'total_hit_count': total_hit_count,
        'restaurants_info': restaurants_info,
    }

    return render(request, 'tabelog/search.html', params)


def get_gnavi_data(
        id,
        category_l,
        pref,
        freeword,
        hit_per_page,
        lunch=0,
        no_smoking=0,
        card=0,
        mobilephone=0,
        bottomless_cup=0,
        sunday_open=0,
        takeout=0,
        private_room=0,
        midnight=0,
        parking=0,
        memorial_service=0,
        birthday_privilege=0,
        betrothal_present=0,
        kids_menu=0,
        outret=0,
        wifi=0,
        microphone=0,
        buffet=0,
        late_lunch=0,
        sports=0,
        until_morning=0,
        lunch_desert=0,
        projecter_screen=0,
        with_pet=0,
        deliverly=0,
        special_holiday_lunch=0,
        e_money=0,
        caterling=0,
        breakfast=0,
        desert_buffet=0,
        lunch_buffet=0,
        bento=0,
        lunch_salad_buffet=0,
        darts=0,
        web_reserve=0
    ):
    query = {
        "keyid": get_keyid(),
        "id": id,
        "area": "AREA110",
        "pref": pref,
        "category_l": category_l,
        "freeword": freeword,
        "hit_per_page": hit_per_page,
        "lunch": lunch,
        "no_smoking": no_smoking,
        "card": card,
        "mobilephone": mobilephone,
        "bottomless_cup": bottomless_cup,
        "sunday_open": sunday_open,
        "takeout": takeout,
        "private_room": private_room,
        "midnight": midnight,
        "parking": parking,
        "memorial_service": memorial_service,
        "birthday_privilege": birthday_privilege,
        "betrothal_present": betrothal_present,
        "kids_menu": kids_menu,
        "outret": outret,
        "wifi": wifi,
        "microphone": microphone,
        "buffet": buffet,
        "late_lunch": late_lunch,
        "sports": sports,
        "until_morning": until_morning,
        "lunch_desert": lunch_desert,
        "projecter_screen": projecter_screen,
        "with_pet": with_pet,
        "deliverly": deliverly,
        "special_holiday_lunch": special_holiday_lunch,
        "e_money": e_money,
        "caterling": caterling,
        "breakfast": breakfast,
        "desert_buffet": desert_buffet,
        "lunch_buffet": lunch_buffet,
        "bento": bento,
        "lunch_salad_buffet": lunch_salad_buffet,
        "darts": darts,
        "web_reserve": web_reserve
    }

    return query


def rest_search(query):
    res_list = []
    res = json.loads(requests.get(
        "https://api.gnavi.co.jp/RestSearchAPI/v3/", params=query).text)
    if "error" not in res:
        res_list.extend(res["rest"])
    return res_list


def extract_restaurant_info(restaurants):
    restaurant_list = []
    for restaurant in restaurants:
        id = restaurant["id"]
        name = restaurant["name"]
        name_kana = restaurant["name_kana"]
        url = restaurant["url"]
        url_mobile = restaurant["url_mobile"]
        shop_image1 = restaurant["image_url"]["shop_image1"]
        shop_image2 = restaurant["image_url"]["shop_image2"]
        address = restaurant["address"]
        tel = restaurant["tel"]
        station_line = restaurant["access"]["line"]
        station = restaurant["access"]["station"]
        latitude = restaurant["latitude"]
        longitude = restaurant["longitude"]
        pr_long = restaurant["pr"]["pr_long"]

        restaurant_list.append([id, name, name_kana, url, url_mobile, shop_image1,
                                shop_image2, address, tel, station_line, station, latitude, longitude, pr_long])
    return restaurant_list


def ShopInfo(request, restid):
    keyid = get_keyid()
    id = restid
    query = get_gnavi_data(
        id,
        "",
        "",
        "",
        1
    )
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
