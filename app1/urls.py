from django.conf.urls import url

from . import views

app_name = 'app1'
urlpatterns = [
#    url(r'^$', views.index, name='index'),
    url(r'^$', views.home, name='index'),

    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^i/(?P<picture_id>[0-9]+)/$', views.picture, name='picture'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^gallery/$', views.gallery, name='gallery'),
    url(r'^picupload/$', views.picupload, name='picupload'),
    url(r'^home/$', views.home, name='home'),
    url(r'^search_result/$', views.search_result, name='search_result'),
    url(r'^tag_list/$', views.tag_list, name='tag_list'),
    url(r'^api/api_get_picture_tags/$', views.api_get_picture_tags, name='api_get_picture_tags'),
    url(r'^api/api_remove_tag_from_picture/$', views.api_remove_tag_from_picture, name='api_remove_tag_from_picture'),
    url(r'^api/api_get_picture_tags_with_term/$', views.api_get_picture_tags_with_term, name='api_get_picture_tags_with_term'),
    url(r'^api/api_get_picture_tags_with_term_1/$', views.api_get_picture_tags_with_term_1, name='api_get_picture_tags_with_term_1'),
    url(r'^api/api_update_picture_tags/$', views.api_update_picture_tags, name='api_update_picture_tags'),
]