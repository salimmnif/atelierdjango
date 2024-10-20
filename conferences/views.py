from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render # type: ignore
from .models import Conferences
from django.views.generic import ListView,DetailView
# Create your views here.


def conferenceList(req):
    liste=Conferences.objects.all()
    return render(req,'conferences/conferencelist.html',{'conference_liste':liste})
class ConferenceListView(ListView):
    model=Conferences
    context_object_name='conferences'
    def get_queryset(self):
        return Conferences.objects.order_by('-start_date')
class detailViewConferences(DetailView):
    model =Conferences
    template_name='conferences/conferences_detail.html'
    context_object_name='details_conf'
