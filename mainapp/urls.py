from django.urls import path
from . import views

urlpatterns=[
path('',views.home,name="home"),
path('login',views.login,name="login"),
path('register',views.register,name="register"),
path('profile',views.profile,name="profile"),
path('logout',views.logout,name="logout"),
path('search',views.search,name="search"),
path("<str:username>",views.post, name="post")

]