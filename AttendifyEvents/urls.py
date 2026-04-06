from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('home',views.home,name="home"),
    path('base',views.base,name="base"),
    path('about',views.about,name="about"),    
    path('contact',views.contact,name="contact"),    
    path('maincategory/',views.main_category,name="maincategory"),  
    path('postevent',views.postevent,name="postevent"),  
    path('eventprofile/<int:event_id>/',views.eventprofile,name="eventprofile"),          
        
    # path('user',views.user,name="user"),        
    path('subcategory/<int:category_id>/',views.subcategory,name="subcategory"), 
    
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),

    path('faq',views.faq,name="faq"),    

    path('user/events/', views.user_events, name='user_events'),
    path('event_detail_user/<int:event_id>/', views.event_detail_user, name='event_detail_user'),

    path('login',views.user_login,name="login"),
    path('logout/', views.user_logout, name='logout'),
    path('user/', views.signup, name='user'),    
    # path('', views.homepage, name='index'),
    # path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    # path('create_order/', views.create_order, name='create_order'),

    path('payment', views.payment,name="payment"),
    path('success/', views.payment_success, name='payment_success'),
    path('fail/', views.payment_fail, name='payment_fail'),

]
