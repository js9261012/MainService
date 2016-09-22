from django.shortcuts import render

from django.http import HttpResponse
from django.core import serializers

from django.views import generic
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from UpdateScore.models import AdjustedPoints, FeedbackPoint, FeedbackPointsRecord, UserDetail
from UpdateScore.serializers import AdjustedPointSerializer, FeedbackPointSerializer, FeedbackPointRecordSerializer, UserDetailSerializer


import urllib
import urllib2
import json
import requests

class AdjustedPointView(generics.ListCreateAPIView):
	queryset = AdjustedPoints.objects.all()
	serializer_class = AdjustedPointSerializer

class AdjustedPointDetail(generics.RetrieveUpdateAPIView):
	queryset = AdjustedPoints.objects.all()
	serializer_class = AdjustedPointSerializer

class FeedbackPointView(generics.ListCreateAPIView):
	queryset = FeedbackPoint.objects.all()
	serializer_class = FeedbackPointSerializer

class FeedbackPointDetail(generics.RetrieveUpdateAPIView):
	queryset = FeedbackPoint.objects.all()
	lookup_field = 'user_id'
	serializer_class = FeedbackPointSerializer	

	def update(self, request, user_id=None):
		feedbackPoint = FeedbackPoint.objects.get(user_id=user_id)
		feedbackPoint.new_store = request.DATA['new_store']
		feedbackPoint.fill_empty = request.DATA['fill_empty']
		feedbackPoint.report_error = request.DATA['report_error']
		feedbackPoint.rating_feedback = request.DATA['rating_feedback']
		feedbackPoint.photo_feedback = request.DATA['photo_feedback']
		feedbackPoint.comment_feedback = request.DATA['comment_feedback']
		feedbackPoint.total_score = request.DATA['total_score']
		feedbackPoint.save()
		return Response(FeedbackPointSerializer(feedbackPoint).data)

class FeedbackPointRecordView(generics.ListCreateAPIView):
	queryset = FeedbackPointsRecord.objects.all()
	serializer_class = FeedbackPointRecordSerializer

class FeedbackPointRecordDetail(generics.RetrieveUpdateAPIView):
	queryset = FeedbackPointsRecord.objects.all()
	serializer_class = FeedbackPointRecordSerializer

class UserDetailDetail(generics.RetrieveAPIView):
	lookup_field = 'user_id'
	queryset = UserDetail.objects.all()
	serializer_class = UserDetailSerializer


def getAdjustPointUrl():
	adjustedPoint_url = 'http://163.21.245.128:8000/MainService/adjustedPoint/'
	return adjustedPoint_url

def getFeedbackPointUrl(user_id):
	feedbackPoint_url = 'http://163.21.245.128:8000/MainService/feedbackPoint/' + str(user_id)
	return feedbackPoint_url

def getFeedbackPointRecordUrl():
	feedbackPointRecord_url = 'http://163.21.245.128:8000/MainService/feedbackPointRecord/'
	return feedbackPointRecord_url

@api_view(['GET'])
def UpdateScore(request):
	adjust_Response = urllib.urlopen(getAdjustPointUrl())
	adjust_Data = json.loads(adjust_Response.read())

	# feedback_Response = urllib.urlopen(getFeedbackPointUrl())
	# feedback_Data = json.loads(feedback_Response.read())

	feedbackRecord_Response = urllib.urlopen(getFeedbackPointRecordUrl())
	feedbackRecord_Data = json.loads(feedbackRecord_Response.read())
	
	show = []
	
	# for feedbackPoint in feedback_Data: #save before adjust feedback
		
	# 	feedbackPoint_content = {			
	# 		'user_id': feedbackPoint['user_id'],
	# 		'new_store': feedbackPoint['new_store'],
	# 		'fill_empty': feedbackPoint['fill_empty'],
	# 		'report_error': feedbackPoint['report_error'],
	# 		'rating_feedback': feedbackPoint['rating_feedback'],
	# 		'photo_feedback': feedbackPoint['photo_feedback'],
	# 		'comment_feedback': feedbackPoint['comment_feedback'],
	# 		'total_score': feedbackPoint['total_score']
	# 	}
	# 	try:
	# 		a = requests.post(getFeedbackPointRecordUrl(), feedbackPoint_content)
	# 	except:
	# 		None


	feedbackRes = []
	adjustRes = []

	for adjust in adjust_Data:

		if adjust['is_adjusted'] == False:

			# for feedbackPoint in feedback_Data:
			feedback_Response = urllib.urlopen(getFeedbackPointUrl(adjust['user_id']))
			feedbackPoint = json.loads(feedback_Response.read())

			# if adjust['user_id'] == feedbackPoint['user_id']:
			feedbackPoint_content = {			
				'user_id': feedbackPoint['user_id'],
				'new_store': feedbackPoint['new_store'],
				'fill_empty': feedbackPoint['fill_empty'],
				'report_error': feedbackPoint['report_error'],
				'rating_feedback': feedbackPoint['rating_feedback'],
				'photo_feedback': feedbackPoint['photo_feedback'],
				'comment_feedback': feedbackPoint['comment_feedback'],
				'total_score': feedbackPoint['total_score']
			}
			try:
				a = requests.post(getFeedbackPointRecordUrl(), feedbackPoint_content)
			except:
				None

			userId = feedbackPoint['user_id']
			newStoreScore = adjust['new_store'] + feedbackPoint['new_store']
			reportError = adjust['report_error'] + feedbackPoint['report_error']
			fillEmpty = adjust['fill_empty'] + feedbackPoint['fill_empty']
			ratingFeedback = adjust['rating_feedback'] + feedbackPoint['rating_feedback']
			photoFeedback = adjust['photo_feedback'] + feedbackPoint['photo_feedback']
			commentFeedback = adjust['comment_feedback'] + feedbackPoint['comment_feedback']
			totalScore = 60 * newStoreScore + 50 * reportError + 40 * fillEmpty + 30 * ratingFeedback + 20 * photoFeedback + 10 * commentFeedback

			feedbackPoint_adjust_content = {
				'user_id': userId,
				'new_store': newStoreScore,						
				'report_error': reportError,
				'fill_empty': fillEmpty,
				'rating_feedback': ratingFeedback,
				'photo_feedback': photoFeedback,
				'comment_feedback': commentFeedback,
				'total_score': totalScore
			}

			adjustPoind_adjust_content = {
				'user_id': adjust['user_id'],
				'new_store': adjust['new_store'],
				'report_error': adjust['report_error'],
				'fill_empty': adjust['fill_empty'],
				'rating_feedback': adjust['rating_feedback'],
				'photo_feedback': adjust['photo_feedback'],
				'comment_feedback': adjust['comment_feedback'],
				'is_adjusted': True
			}

			try:
				res = requests.put("http://163.21.245.128:8000/MainService/feedbackPoint/" + str(feedbackPoint['user_id']) + "/", data = feedbackPoint_adjust_content)
				feedbackRes.append(res)
			except Exception as e:
				feedbackRes.append(e)

			try:
				res = requests.put("http://163.21.245.128:8000/MainService/adjustedPoint/" + str(adjust['id']) + "/", data = adjustPoind_adjust_content)
				adjustRes.append(res)
			except Exception as e:
				adjustRes.append(e)

	return Response({'feedbackRes':feedbackRes, 'adjustRes':adjustRes})