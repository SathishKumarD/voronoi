from django import template
register = template.Library()
from voronoi.models import House
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D

import socket
socket.gethostname()


def nearby_places(latitude, longitude, distance_miles, count):

	ref_location = Point(longitude, latitude)
   	houses = House.gis.filter(point__distance_lte=(ref_location, D(mi=distance_miles))).distance(ref_location).order_by('distance')[1:count]
	return {
	'houses':houses,
	'is_present': True
	}

register.inclusion_tag('voronoi/nearby_places.html')(nearby_places)