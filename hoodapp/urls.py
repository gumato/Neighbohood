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
    url(r'^new/hood$', views.new_hood, name='new-hood'),
    url(r'^hoods/(\d+)',views.hoods,name='hoods'),
    url(r'^hoods/new/business/(\d+)$',views.post_business, name='new-business'),
    url(r'^new/hood$', views.new_hood, name='new-hood'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)