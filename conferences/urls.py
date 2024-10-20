from django.urls import path # type: ignore
from .views import *
urlpatterns=[
    path('list/', conferenceList, name='listconf'),
    path('listViewConferences/', ConferenceListView.as_view(), name='listview'),
    path('details/<int:pk>/', detailViewConferences.as_view(), name='details')
]


  