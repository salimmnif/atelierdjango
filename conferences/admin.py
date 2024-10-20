from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet # type: ignore
from django.db.models import Count
from .models import Conferences
from users.models import *
from django.utils.timezone import now
from datetime import timedelta


# Register your models here.

class ReservationInLine(admin.StackedInline):
    model=Reservations
    extra=1
    readonly_fields=('reservation_date',)
    can_delete=True


class participantfilter(admin.SimpleListFilter):
    title = ('participant filter')
    parameter_name = 'participant_filter'
    def lookups(self, request, model_admin):
        return (
            ('0',('No participants')),
            ('more',('More participants'))
        )
    """
    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count=0) # Count('reservations') el reservation mel related name li aamelnah fel model
        if self.value()=='more':
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count__gt=0)

        
        return queryset
        """
    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(reservations__isnull=True)
        if self.value()=='more':
            return queryset.filter(reservations__isnull=False)
        return queryset

class ConferenceDateFilter(admin.SimpleListFilter):
    title = ('conference date')
    parameter_name = 'conference_date'

    def lookups(self, request, model_admin):
        return (
            ('past', ('Past Conferences')),
            ('today', ('Today Conferences')),
            ('upcoming', ('Upcoming Conferences')),
        )

    def queryset(self, request, queryset):
        today = now().date()  

        if self.value() == 'past':
            
            return queryset.filter(end_date__lt=today)

        if self.value() == 'today':
            
            return queryset.filter(start_date__lte=today, end_date__gte=today)

        if self.value() == 'upcoming':
            
            return queryset.filter(start_date__gt=today)

        return queryset



class ConferenceAdmin(admin.ModelAdmin): # type: ignore
    list_display = ('title','location', 'start_date','end_date', 'price')
    search_fields=('title',)
    #list_per_page=1
    ordering=('start_date','title') # ordre inverse ordering=('-start_date') 
    fieldsets=(
        ('description',{
            'fields':('title','description','location','category')
        }),
        ('horaire',{
            'fields':('start_date','end_date','created_at','updated_at')
        }),
        ('documents',{
            'fields':('program','price','capacity')
        }
    ))
    readonly_fields=('created_at','updated_at')
    inlines=[ReservationInLine]
    autocomplete_fields=('category',)
    list_filter=('title',participantfilter,ConferenceDateFilter)


admin.site.register(Conferences,ConferenceAdmin)