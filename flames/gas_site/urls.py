from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),

    url(r'^$', HomePage.as_view(), name='home'),
    url(r'^home/$', HomePage.as_view(), name='home'),
    url(r'^users/home$', UserPage.as_view(), name='user_home'),
    url(r'^users/logout$', logout, name='user_logout'),
    url(r'^admin1/logout$', logout, name='admin_logout'),
    url(r'^email$', ForgotPassword.as_view(), name='email'),
    url(r'^password/change$', PasswordChange.as_view(), name='email'),
    url(r'^admin1/home', AdminPage.as_view(), name='admin_home'),
    url(r'^admin1/requests', Order.as_view(), name='requests'),
    url(r'^admin1/consumers', Consumer.as_view(), name='admin_consumers'),
    url(r'^users/refil$', Refil.as_view(), name='refil'),
    url(r'^users/refil/refil_new$', Refil_new, name='refil_new'),
]
