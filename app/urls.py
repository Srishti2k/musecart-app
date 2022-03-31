from django.contrib import auth
from app.forms import LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.urls import path
from app import views
from django.contrib.auth import logout, views as auth_views
from .forms import *
urlpatterns = [
  
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('showcart/' , views.showcart , name='showcart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minuscart),
    path('removecart/', views.removecart),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('buy/', views.buy_now, name='buy-now'),
    
    path('address/', views.address, name='address'),

    path('orders/', views.orders, name='orders'),

    path('changepassword/', views.change_password, name='changepassword'),
 
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),

    path('checkout/', views.checkout, name='checkout'),
    path('' , views.ProductView.as_view() , name = 'home'),  #class based 
    path('product-detail/<int:pk>' , views.product_detail.as_view() , name = 'product-detail'), #class based 
    


    path('profile/', views.ProfileView.as_view(), name='profile'),
    







    #login logout registration
    path('login/' , auth_views.LoginView.as_view(template_name='app/login.html' , authentication_form= LoginForm ), name='login'), #BUILTIN login view
    path('logout/' , auth_views.LogoutView.as_view(next_page='login'), name='logout'), #BUILTIN Logout view
    path('registration/', views.customerregistration.as_view() , name='customerregistration'), #class based 
    #password change
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),

    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone')
]

