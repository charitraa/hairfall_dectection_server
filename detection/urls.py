
from django.urls import path
from detection.views import DailyHairScanApiView, HairScanAPIView, ProgressAPIView, HairAnalysisView, ProgressDailyHairScanAPIView
urlpatterns = [
    path('scan/', HairScanAPIView.as_view(), name='hair-scan'),
    path('progress/', ProgressAPIView.as_view(), name='progress'),
    path('analysis/', HairAnalysisView.as_view(), name='hair-analysis'),
    path('progress-daily/', ProgressDailyHairScanAPIView.as_view(), name='progress-daily'),
    path('daily-scan/', DailyHairScanApiView.as_view(), name='daily-scan'),
] 