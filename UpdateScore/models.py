from decimal import *
from math import sin, cos, sqrt, atan2, radians
from django.db import models
from django.contrib.auth.models import User


class NearbyManager(models.Manager):
	def near_by(self, location, radius):
		from django.db import connection
		cursor = connection.cursor()
		cursor.execute("""SELECT id FROM biteit_phone_storeinfo""")
		result_list = []

		for row in cursor.fetchall():
			storeInfos = self.get_queryset().filter(id=row[0])

			for storeInfo in storeInfos:
				if storeInfo.is_near(location, radius):
					result_list.append(storeInfo)
		return result_list

'''
class FriendsManager(models.Manager):
	def friend_photo_comment(self):
		from django.db import connection
		cursor = connection.cursor()
		cursor.execute("""SELECT id FROM biteit_phone_photocomment""")
		result_list = []

		for row in cursor.fetchall():
			storePhotoComments = self.get_queryset().filter(id=row[0])

			for storePhotoComment in storePhotoComments:
				if storePhotoComment.is_near(location, radius):
					result_list.append(storeInfo)
		return result_list
'''

class FriendshipManager(models.Manager):
	def is_friends(self, user_a, user_b):
		if self.get_query_set().filter(
			user__id=user_a.id, friend__id=user_b.id).exists() or self.get_query_set().filter(
			user__id=user_b.id, friend__id=user_a.id).exists():
			return True
		else:
			return False


class UserDetail(models.Model):
	user_id = models.ForeignKey(User)
	login_type = models.CharField(max_length=10)
	third_id = models.CharField(max_length=200, unique=True)
	gcm_id = models.CharField(max_length=254, unique=True)

	class Meta:
		db_table = 'biteit_phone_userdetail'


class StoreInfo(models.Model):
	google_store_id = models.CharField(max_length=200, unique=True)
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=200)
	phone = models.CharField(max_length=200, blank=True)
	url = models.CharField(max_length=500, blank=True)
	email = models.EmailField(max_length=254, blank=True)
	longitude = models.DecimalField(max_digits=35, decimal_places=28)
	latitude = models.DecimalField(max_digits=35, decimal_places=28)
	first_level = models.CharField(max_length=200, blank=True)
	third_level = models.CharField(max_length=200, blank=True)
	ratingClean = models.FloatField()
	ratingService = models.FloatField()
	ratingAtmos = models.FloatField()
	ratingFlavor = models.FloatField()
	ratingUnknow = models.FloatField()
	is_favor = models.BooleanField(default=False)
	is_blocked = models.BooleanField(default=False)
	tags = models.CharField(max_length=500, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = models.Manager()
	nearby_objects = NearbyManager()

	def is_near(self, location, radius):
		lon = self.longitude
		lat = self.latitude
		location = location.split(',')
		u_lon = Decimal(location[0])
		u_lan = Decimal(location[1])

		# div 1000 for kilometer
		radius = Decimal(radius) / 1000

		R = 6373.0

		lat1 = radians(lat)
		lon1 = radians(lon)
		lat2 = radians(u_lan)
		lon2 = radians(u_lon)

		dlon = lon2 - lon1
		dlat = lat2 - lat1
		a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
		c = 2 * atan2(sqrt(a), sqrt(1-a))
		distance = R * c

		if distance < radius:
			return True
		else:
			return False

	# like toString in JAVA. 
	# In Python3, using __str__(self)
	def __unicode__(self):
		return self.name + self.address + self.phone

	class Meta:
		db_table = 'biteit_phone_storeinfo'


class StorePhotoComment(models.Model):
	store_id = models.ForeignKey(StoreInfo)
	user_id = models.ForeignKey(User)
	photo = models.ImageField(upload_to='storePhotoComments', blank=True)
	comment = models.CharField(max_length=500, blank=True)
	attend_no = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	# objects = models.Manager()
	# firends_objects = models.FriendsManager()
	class Meta:
		db_table = 'biteit_phone_storephotocomment'


class Friend(models.Model):
	user_id = models.ForeignKey(User)
	friend_id = models.ForeignKey(User, related_name='friends')
	is_focused = models.BooleanField(default=False)
	is_blocked = models.BooleanField(default=False)

	objects = FriendshipManager()

	class Meta:
		db_table = 'biteit_phone_friend'
		unique_together = (('user_id', 'friend_id'), )


class Feedback(models.Model):
	user_id = models.ForeignKey(User)
	store_id = models.ForeignKey(StoreInfo)
	ratingClean = models.FloatField()
	ratingService = models.FloatField()
	ratingAtmos = models.FloatField()
	ratingFlavor = models.FloatField()
	ratingUnknow = models.FloatField()
	comment = models.CharField(max_length=200, blank=True)
	attend_no = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'biteit_phone_feedback'


class UserStore(models.Model):
	user_id = models.ForeignKey(User)
	store_id = models.ForeignKey(StoreInfo)
	is_focused = models.BooleanField(default=False)
	is_blocked = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'biteit_phone_userstore'


class FeedbackPoint(models.Model):
	user_id = models.ForeignKey(User, unique=True)
	new_store = models.IntegerField()
	fill_empty = models.IntegerField()
	report_error = models.IntegerField()
	rating_feedback = models.IntegerField()
	photo_feedback = models.IntegerField()
	comment_feedback = models.IntegerField()
	total_score = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'biteit_phone_feedbackpoint'


class FoundNewStore(models.Model):
	user_id = models.ForeignKey(User)
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=200)
	phone = models.CharField(max_length=200, blank=True)
	longitude = models.DecimalField(max_digits=35, decimal_places=28)
	latitude = models.DecimalField(max_digits=35, decimal_places=28)
	first_level = models.CharField(max_length=200, blank=True)
	third_level = models.CharField(max_length=200, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'biteit_phone_foundnewstore'


class FoundNewStorePhotoComment(models.Model):
	new_store_id = models.ForeignKey(FoundNewStore)
	user_id = models.ForeignKey(User)
	photo = models.ImageField(upload_to='newstorephotos', blank=True)
	comment = models.CharField(max_length=500, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'biteit_phone_foundnewstorephotocomment'


class ReportErrorStore(models.Model):
	user_id = models.ForeignKey(User)
	store_id = models.ForeignKey(StoreInfo)
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=200)
	phone = models.CharField(max_length=200, blank=True)
	longitude = models.DecimalField(max_digits=35, decimal_places=28)
	latitude = models.DecimalField(max_digits=35, decimal_places=28)
	first_level = models.CharField(max_length=200, blank=True)
	third_level = models.CharField(max_length=200, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'biteit_phone_reporterrorstore'


class ReportErrorStorePhotoComment(models.Model):
	user_id = models.ForeignKey(User)
	store_id = models.ForeignKey(StoreInfo)
	uri = models.CharField(max_length=200, blank=True)
	comment = models.CharField(max_length=500, blank=True)
	attend_no = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'biteit_phone_reporterrorstorephotocomment'


class NotExistsStore(models.Model):
	user_id = models.ForeignKey(User)
	store_id = models.ForeignKey(StoreInfo)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'biteit_phone_notexistsstore'


class StoreReportRecord(models.Model):
	user_id = models.ForeignKey(User)
	types = models.CharField(max_length=200)
	status = models.CharField(max_length=200)
	google_store_id = models.CharField(max_length=200, unique=True)
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=200)
	phone = models.CharField(max_length=200, blank=True)
	url = models.CharField(max_length=500, blank=True)
	email = models.EmailField(max_length=254, blank=True)
	longitude = models.DecimalField(max_digits=35, decimal_places=28)
	latitude = models.DecimalField(max_digits=35, decimal_places=28)
	first_level = models.CharField(max_length=200, blank=True)
	third_level = models.CharField(max_length=200, blank=True)
	ratingClean = models.FloatField()
	ratingService = models.FloatField()
	ratingAtmos = models.FloatField()
	ratingFlavor = models.FloatField()
	ratingUnknow = models.FloatField()
	is_favor = models.BooleanField(default=False)
	is_blocked = models.BooleanField(default=False)
	tags = models.CharField(max_length=500, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'main_storereportrecord'

class StorePhotoReportRecord(models.Model):
	store_id = models.ForeignKey(StoreReportRecord)
	user_id = models.ForeignKey(User)
	types = models.CharField(max_length=200)
	photo = models.CharField(max_length=500, blank=True)
	comment = models.CharField(max_length=500, blank=True)
	attend_no = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'main_storephotoreportrecord'


class AdjustedPoints(models.Model):
	user_id = models.ForeignKey(User)
	new_store = models.IntegerField()
	fill_empty = models.IntegerField()
	report_error = models.IntegerField()
	rating_feedback = models.IntegerField()
	photo_feedback = models.IntegerField()
	comment_feedback = models.IntegerField()
	is_adjusted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'main_adjustedpoints'

class FeedbackPointsRecord(models.Model):
	user_id = models.ForeignKey(User)
	new_store = models.IntegerField()
	fill_empty = models.IntegerField()
	report_error = models.IntegerField()
	rating_feedback = models.IntegerField()
	photo_feedback = models.IntegerField()
	comment_feedback = models.IntegerField()
	total_score = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	# class Meta:
	# 	db_table = 'UpdateScore_feedbackpointsrecord'

class UserDetail(models.Model):
	user_id = models.ForeignKey(User)
	login_type = models.CharField(max_length=10)
	third_id = models.CharField(max_length=200, unique=True)
	gcm_id = models.CharField(max_length=254, unique=True)
	
	class Meta:
		db_table = 'biteit_phone_userdetail'	