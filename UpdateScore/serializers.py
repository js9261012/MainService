from rest_framework import serializers
from UpdateScore.models import StoreInfo, StorePhotoComment, FeedbackPoint, FeedbackPointsRecord,FoundNewStore, FoundNewStorePhotoComment, ReportErrorStore, ReportErrorStorePhotoComment, NotExistsStore, StoreReportRecord, StorePhotoReportRecord, AdjustedPoints, UserDetail

class StoreInfoSerializer(serializers.ModelSerializer):

	class Meta:
		model = StoreInfo
		fields = ('id', 'google_store_id', 'name', 'address', 'phone', 'url', 'email', 'longitude', 'latitude', 'first_level', 'third_level', 'ratingClean', 'ratingService', 'ratingAtmos', 'ratingFlavor', 'ratingUnknow', 'is_favor', 'is_blocked', 'tags', 'created_at', 'updated_at')

class StorePhotoCommentSerializer(serializers.ModelSerializer):
	#store_id = serializers.Field(source=StoreInfo.pk)
	#user_id = serializers.Field(source=User.pk)

	class Meta:
		model = StorePhotoComment
		fields = ('id','store_id', 'user_id', 'photo', 'comment', 'attend_no', 'created_at', 'updated_at')

class FeedbackPointSerializer(serializers.ModelSerializer):
	# user_id = serializers.PrimaryKeyRelatedField()
	class Meta:
		model = FeedbackPoint
		fields = ('id', 'user_id', 'new_store', 'fill_empty', 'report_error', 'rating_feedback', 'photo_feedback', 'comment_feedback', 'total_score', 'created_at', 'updated_at')
		url_field_name = 'user_id'

class FeedbackPointRecordSerializer(serializers.ModelSerializer):
	# user_id = serializers.PrimaryKeyRelatedField()
	class Meta:
		model = FeedbackPointsRecord
		fields = ('id', 'user_id', 'new_store', 'fill_empty', 'report_error', 'rating_feedback', 'photo_feedback', 'comment_feedback', 'total_score', 'created_at', 'updated_at')
		url_field_name = 'user_id'		

class FoundNewStoreSerializer(serializers.ModelSerializer):
	class Meta:
		model = FoundNewStore
		fields = ('id', 'user_id', 'name', 'address', 'phone', 'longitude', 'latitude', 'first_level', 'third_level', 'created_at', 'updated_at')

class FoundNewStorePhotoSerializer(serializers.ModelSerializer):
	class Meta:
		model = FoundNewStorePhotoComment
		fields = ('id', 'new_store_id', 'user_id', 'photo', 'comment', 'created_at', 'updated_at')

class ReportErrorStoreSerializer(serializers.ModelSerializer):
	class Meta:
		model = ReportErrorStore
		fields = ('id', 'user_id', 'store_id', 'name', 'address', 'phone', 'longitude', 'latitude', 'first_level', 'third_level', 'created_at', 'updated_at')

class ReportErrorStorePhotoCommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = ReportErrorStorePhotoComment
		fields = ('id', 'store_id', 'user_id', 'uri', 'comment', 'attend_no', 'created_at', 'updated_at')

class NotExistsStoreSerializer(serializers.ModelSerializer):
	class Meta:
		model = NotExistsStore
		fields = ('user_id', 'store_id', 'created_at', 'updated_at')


class StoreInfoRecordSerializer(serializers.ModelSerializer):

	class Meta:
		model = StoreReportRecord
		fields = ('id', 'types', 'status', 'user_id','google_store_id', 'name', 'address', 'phone', 'url', 'email', 'longitude', 'latitude', 'first_level', 'third_level', 'ratingClean', 'ratingService', 'ratingAtmos', 'ratingFlavor', 'ratingUnknow', 'is_favor', 'is_blocked', 'tags', 'created_at', 'updated_at')

class StorePhotoReportRecordSerializer(serializers.ModelSerializer):
	#store_id = serializers.Field(source=StoreInfo.pk)
	#user_id = serializers.Field(source=User.pk)

	class Meta:
		model = StorePhotoReportRecord
		fields = ('id', 'types', 'store_id', 'user_id', 'photo', 'comment', 'attend_no', 'created_at', 'updated_at')

class AdjustedPointSerializer(serializers.ModelSerializer):
	class Meta:
		model = AdjustedPoints
		fields = ('id', 'user_id', 'new_store', 'fill_empty', 'report_error', 'rating_feedback', 'photo_feedback', 'comment_feedback', 'is_adjusted', 'created_at', 'updated_at')

class UserDetailSerializer(serializers.ModelSerializer):
	# user_id = serializers.Field(source=User.pk)
	class Meta:
		model = UserDetail
		fields = ('id', 'user_id', 'login_type', 'third_id', 'gcm_id')