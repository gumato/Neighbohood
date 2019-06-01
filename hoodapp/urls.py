from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url('^$',views.index,name = 'index'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'signup/', views.Signup, name="signup"),
    url(r'^profile/$',views.profile,name='profile'),
    # url(r'^review/(?P<pk>\d+)',views.add_review,name='review'),
    # url(r'profile/',views.profile_index, name='profile'),
    url(r'^edit/profile/$',views.edit_profile,name='edit_profile'), 
    url(r'^single/(\d+)',views.single_post,name='single'),
    # url(r'^ajax/project/$',views.ProjectList.as_view()),
    # url(r'^api/profile/$', views.ProfileList.as_view()),
]
# if settings.DEBUG:
#     urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)