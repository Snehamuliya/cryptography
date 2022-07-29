from django.urls import path
from .views import index, signup, login, a_login, logout, a_logout, ad_profile, encry, decry
from .views import a_endata, a_index, profile, u_activity, up_account

urlpatterns = [
    path('', index),
    path('signup', signup),
    path('en_data', encry, name='e_data'),
    path('de_data', decry, name='d_data'),
    path('account', profile, name='account'),
    path('uaccount', up_account, name='up_acc'),
    path('eview', u_activity, name='activity'),
    path('login', login, name='log'),
    path('a_login', a_login, name='alog'),
    path('a_home', a_index, name='ahome'),
    path('logout', logout, name='out'),
    path('a_logout', a_logout, name='a_out'),
    path('profile_data', ad_profile, name='u_profile'),
    path('ad_encry', a_endata, name='a_edata')

]