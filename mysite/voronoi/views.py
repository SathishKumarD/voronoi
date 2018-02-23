from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
# Create your views here.
from .models import House
from django.db.models import CharField
from django.db.models import  Q
from django.core import serializers
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

def get_rating_labels():
	rating_labels = {1:"Very Bad",2:"Bad",3:"Okay",4:"Good",5:"Excellent"}
	return rating_labels

def search_results_query(search_text):
	houses = []
	if search_text is not None and search_text != u"":
		fields = [f for f in House._meta.fields if isinstance(f, CharField)]
		queries = [Q(**{f.name+"__icontains": search_text}) for f in fields]
		qs = Q()
		for query in queries:
			qs = qs | query
	return qs

def get_houses(request):
	page = request.GET.get('page', 1)
	rent_ = request.GET.get('rent',0)
	distance_ = request.GET.get('bus_stop_distance', 0)
	bus_stop_time_ = request.GET.get('bus_stop_time',0)
	address_ = request.GET.get('address', '')
	city_ = request.GET.get('city', '')
	neighborhood_ = request.GET.get('neighborhood', '')

	qs = Q()
	qs &= Q(rent__lt = rent_) if rent_ else qs
	qs &= Q(bus_stop_distance__lt = float(distance_)*1609.34) if distance_ else qs
	qs &= Q(bus_stop_time__lt = bus_stop_time_) if bus_stop_time_ else qs
	qs &= Q(city__icontains = city_) if city_ else qs
	qs &= Q(neighborhood__icontains= neighborhood_) if neighborhood_ else qs

	

	
	if address_ != u"":
		qs &= search_results_query(address_)
	houses = House.objects.filter(qs)
	return houses


def search(request):
	if request.method == "GET":
		houses = get_houses(request,30)
		paginator = Paginator(houses, 10)
		try:
			houses = paginator.page(page)
		except PageNotAnInteger:
			houses = paginator.page(1)
		except EmptyPage:
			houses = paginator.page(paginator.num_pages)
		
		context = {'houses': houses,'search_params':{'rent':rent_,'bus_stop_distance':distance_,'address':address_}}
		return render(request,'voronoi/search.html', context)

def get_search_json(request):
	houses = get_houses(request)[:30]
	results = [ob.as_json() for ob in houses]
	context = {'houses': houses}
	results_view = render(request,'voronoi/home_results.html', context)
	json_data = {"map_data":results, "search_data":results_view.content}

	return HttpResponse(json.dumps(json_data), content_type="application/json")


def get_search_suggestions(request):
	houses = get_houses(request)
	suggestions = []
	total_suggestions = 10

	# get neighborhoods
	neighborhoods = [house['neighborhood'] for house in houses.values('neighborhood').distinct()[:3]]
	suggestions+= [{'label':neighborhood,'value':'neighborhood'} for neighborhood in neighborhoods if neighborhood ]

	print suggestions
	# get maching cities
	cities = [house['city'] for house in houses.values('city').distinct()[:3]]
	suggestions+=[{'label':city,'value':'city'} for city in cities]

	print suggestions

	# get matching streets
	streets = [house['street'] for house in houses.values('street').distinct()[:3]]
	suggestions+=[{'label':street,'value':'street'} for street in streets]

	# fill the remaining with address suggestions
	remaining_val = total_suggestions - len(suggestions)
	suggestions+=[{'label':house.address,'value':'address','id':house.id} for house in houses[:10]]
	
	return HttpResponse(json.dumps(suggestions), content_type="application/json")


def create(request):
	return render(request,'voronoi/house_form.html')


def index(request):
	return render(request, 'voronoi/index.html', {'hot_houses':[]})

def detail(request, house_id):
	house = get_object_or_404(House, pk=house_id)
	return render(request, 'voronoi/detail3.html', {'house': house,'rating_labels':get_rating_labels()})

def ratings(request, house_id):
    response = "You're looking at the ratings of the house %s."
    return HttpResponse(response % house_id)