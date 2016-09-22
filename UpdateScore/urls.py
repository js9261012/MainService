from django.conf.urls import patterns, url
 
from UpdateScore import views
 
urlpatterns = patterns('',

   url(r'^adjustedPoint/$', views.AdjustedPointView.as_view(), name='AdjustedPointView'),
   url(r'^adjustedPoint/(?P<pk>[0-9]+)/$', views.AdjustedPointDetail.as_view(), name='AdjustedPointDetail'),
   url(r'^feedbackPoint/$', views.FeedbackPointView.as_view(), name='FeedbackPointView'),
   url(r'^feedbackPoint/(?P<user_id>[0-9]+)/$', views.FeedbackPointDetail.as_view(), name='FeedbackPointDetail'),
   url(r'^feedbackPointRecord/$', views.FeedbackPointRecordView.as_view(), name='FeedbackPointRecordView'),
   url(r'^api/userdetail/(?P<user_id>[0-9]+)/$', views.UserDetailDetail.as_view(), name='userdetaildetail'),

   url(r'^UpdateScore/$', views.UpdateScore, name='UpdateScore'),
    
)