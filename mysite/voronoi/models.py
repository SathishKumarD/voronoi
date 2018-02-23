from django.db import models
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from django.utils.translation import ugettext, ugettext_lazy as _


import hashlib

class BusStop(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=100)
	latitude = models.FloatField(null=True, default=0)
	longitude = models.FloatField(null=True, default=0)

class Question(models.Model):
	id = models.AutoField(primary_key=True)
	question_text = models.CharField(max_length=200)
	published_date = models.DateTimeField()
	is_default = models.BooleanField()


class Answer(models.Model):
	id = models.AutoField(primary_key=True)
	answer_text = models.CharField(max_length=1000)
	published_date = models.DateTimeField()
	question = models.ForeignKey(Question)

class House(models.Model):
	gis = gis_models.GeoManager()
	objects = models.Manager()


	id = models.AutoField(primary_key=True)
	house_number = models.CharField(max_length=5, 
		verbose_name=_('House number'))
	street = models.CharField(max_length=200)
	city = models.CharField(max_length=200,
		verbose_name=_('City'))
	zipcode = models.CharField(max_length=7)
	state = models.CharField(max_length=20)
	user = models.ForeignKey(User)
	bus_stop_distance = models.FloatField(null=True)
	bus_stop = models.ForeignKey(BusStop,null=True)
	bus_stop_time = models.FloatField(null=True)
	latitude = models.FloatField()
	longitude = models.FloatField()
	address = models.CharField(max_length=500, null=True)
	rent = models.IntegerField(null=True)
	security_deposit = models.IntegerField(null=True)
	bed_rooms = models.IntegerField(null=True)
	bath_rooms = models.FloatField(null=True,default=0)
	subboard_listing_ids = models.CharField(max_length = 200, null = True)
	rent_type = models.CharField(max_length = 100, null = True)
	unit_type = models.CharField(max_length = 100,null = True)
	neighborhood = models.CharField(max_length=200,null = True)
	point = gis_models.PointField()

	def get_address(self):
		return str(self.house_number) + " "+ self.street + ", " + \
		self.city + ", "+ self.state + ", "+ str(self.zipcode)

	def __str__(self):
		return self.get_address()
		
	def as_json(self):
		return dict(
			id=self.id,
			house_number=self.house_number,
			street=self.street, 
			city=self.city,
			zipcode=self.zipcode,
			state = self.state,
			bus_stop_distance = self.bus_stop_distance*0.000621371 if self.bus_stop_distance else 0, # meters to miles conversion.
			bus_stop = self.bus_stop.name if self.bus_stop else "",
			bus_stop_time = self.bus_stop_time,
			latitude = self.latitude,
			longitude = self.longitude,
			address = self.get_address()
			)


class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name='profile')
	about_me = models.TextField(null=True, blank=True)

	def __unicode__(self):
		return "{}'s profile".format(self.user.username)

	class Meta:
		db_table = 'user_profile'

	def profile_image_url(self):
		"""
		Return the URL for the user's Facebook icon if the user is logged in via Facebook,
		otherwise return the user's Gravatar URL
		"""
		fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')

		if len(fb_uid):
			return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)

		return "http://www.gravatar.com/avatar/{}?s=40".format(
			hashlib.md5(self.user.email).hexdigest())

	def account_verified(self):
		"""
		If the user is logged in and has verified hisser email address, return True,
		otherwise return False
		"""
		result = EmailAddress.objects.filter(email=self.user.email)
		if len(result):
			return result[0].verified
		return False


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

