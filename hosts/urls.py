from django.urls import path
from .views import upload_view,  com_per_city
from .views import ListCommisionsAllView, ListCommisionsMonthView 



urlpatterns = [
    path('upload/', upload_view, name='upload'),
    path('list/', ListCommisionsAllView.as_view(), name='list-commision'),
    path('city/', com_per_city, name='list-commision-per-city'),
    path('month/', ListCommisionsMonthView.as_view(), name='list-commision-per-month'),
]


