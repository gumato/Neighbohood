from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url('^$',views.index,name = 'index'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'signup/', views.Signup, name="signup"),
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^edit/profile/$',views.edit_profile,name='edit_profile'), 
    url(r'^hood/(?P<id>\d+)', views.hood, name='hood'),
    url(r'^business/(?P<hood_id>\d+)', views.business, name='business'),
    url(r'^post/$', views.add_post,name='add_post'),
    url(r'^upload/$', views.upload_business, name='upload_business'),
    url(r'^new_neighbourhood/$', views.new_neighbourhood, name='new_neighbourhood'),
    url(r'^business/', views.business, name='business'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)