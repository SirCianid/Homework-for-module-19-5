from django.urls import path
from .views import *

urlpatterns = [
    path('', sign_up_by_django),
    path('main_pg/', main_pg_view),
    path('shop_pg/', games_shp_page),
    path('cart_pg/', cart_page),
    path('success/', success),
    path('news/', news_page),
]