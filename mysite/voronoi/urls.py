from django.conf.urls import url

from . import views
from .HouseView import CreateHouseView

app_name = 'voronoi'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^house/create/$', CreateHouseView.as_view(), name='create'),
    #url(r'^get_search_results/$', views.get_search_results, name='get_search_results'),
    url(r'^get_search_json/$', views.get_search_json, name='get_search_json'),
    url(r'^get_search_suggestions/$', views.get_search_suggestions, name='get_search_suggestions'),

    
 	# ex: /polls/5/
    url(r'^(?P<house_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<house_id>[0-9]+)/ratings/$', views.ratings, name='ratings'),

]