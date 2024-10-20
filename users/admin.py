from django.contrib import admin # type: ignore
from .models import Participant,Reservations


class ReservationInline(admin.TabularInline):
    model = Reservations
    extra = 1  
    readonly_fields = ("reservation_date",)  
    autocomplete_fields = ('participant',)  


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("username","first_name","last_name","email","cin","participant_category", "created_at","updated_at",)
    search_fields = ("username", "first_name", "last_name", "email", "cin")
    list_per_page = 5
    ordering = ("created_at",)
    readonly_fields = ("created_at", "updated_at")  
    fieldsets = (
        ('Personal info', {
            'fields': ('username', 'first_name', 'last_name', 'email', 'cin', 'participant_category') 
        }),
        ('follow_up time', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    inlines = [ReservationInline] 
    list_filter = ('participant_category',)
    list_editable = ('first_name', 'last_name')





class ReservationAdmin(admin.ModelAdmin):
    list_display = ["conference","participant","confirmed"]
    actions=['confirmed','unconfirmed']
    def confirmed(self,request,queryset):
        queryset.update(confirmed=True)
        self.message_user(request,"les messages sont confirmés")
    confirmed.short_description = "Confirmer les messages"
    def unconfirmed(self,request,queryset):
        queryset.update(confirmed=False)
        self.message_user(request,"les messages sont inconfirmés")
    unconfirmed.short_description = "inConfirmer les messages"

# Register your models here.
admin.site.register(Participant,ParticipantAdmin)
admin.site.register(Reservations,ReservationAdmin)