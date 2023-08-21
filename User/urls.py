
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from.forms import LoginForm,PasswordResetForm,PasswordChange,SetPasswordForm
urlpatterns = [
     path('',views.homepage),
     path('ShowPdt/<id>',views.ShowPdt,name='show'),
     path('ViewDetails/<id>',views.ViewDetails,name='ViewDetails'),
     path('add-to-cart',views.cart,name='add-to-cart'),
     path('show-cart', views.showcart, name='show-cart'),
     path('pluscart/', views.pluscart),
     path('minuscart/', views.minuscart),
     path('removecart/', views.removecart),
     path('checkout/',views.checkout, name='checkout'),
     path('paymentdone/', views.payment_done, name='paymentdone' ),
     path("orders/", views.orders , name="orders"),
     path("pluswishlist/",views.plus_wishlist),
     path("minuswishlist/",views.minus_wishlist),
     path("wishlist/",views.show_wishlist,name="wishlist"),

     path("search/", views.search , name="search"),

     path('signup',views.signup,name='signup'),

     path('accounts/login/',auth_view.LoginView.as_view
         (template_name = 'login.html',authentication_form= LoginForm),name='login'),
      
 
     path('profile',views.profile,name='profile'),
     path('address',views.Address ,name='address'),
     path('update/<id>',views.update,name='update'),
     path('passwordchnage/',auth_view.PasswordChangeView.as_view(template_name='changepassword.html', form_class = PasswordChange, success_url='/PasswordChngDone'),name='passwordchnage'),
     path('PasswordChngDone/',auth_view.PasswordChangeDoneView.as_view(template_name='PasswordChngDone.html'),name='PasswordChngDone'),

     path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout' ),
     
     path('password-reset/',auth_view.PasswordResetView.as_view
         (template_name='password_reset.html',form_class=PasswordResetForm), name='password-reset'),

     path('password-reset/done/',auth_view.PasswordResetDoneView.as_view
         (template_name='password_reset_done.html'), name='password_reset_done'),   
     
     path('password-reset-confirm/<uidb64>/<token>',auth_view.PasswordResetConfirmView.as_view
         (template_name='password_reset_confirm.html',form_class=SetPasswordForm), name='password_reset_confirm'),   
     
     path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view
         (template_name='password_reset_complete.html'), name='password_reset_complete'),   

]


