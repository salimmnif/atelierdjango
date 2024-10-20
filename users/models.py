from django.db import models  # type: ignore
from django.contrib.auth.models import AbstractUser  # type: ignore
from conferences.models import Conferences
from django.core.validators import RegexValidator # type: ignore
import re
from django.core.exceptions import ValidationError # type: ignore
from datetime import datetime

def email_validator(value):
    if not value.endswith('@esprit.tn'):
        raise ValidationError('Invalid email,only domain @esprit.tn is allowed')


class Participant(AbstractUser):
    only_numbers=RegexValidator(regex=r'^\d{8}$',message='must contain exactly 8 numbers')
    cin = models.CharField(primary_key=True, max_length=8,validators=[only_numbers])
    email = models.EmailField(unique=True, max_length=255,validators=[email_validator])
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    USERNAME_FIELD = 'username'
    CHOICES = (
        ('etudiant', 'etudiant'),
        ('chercheur', 'chercheur'),
        ('docteur', 'docteur'),
        ('enseignant', 'enseignant')
    )
    participant_category = models.CharField(max_length=255, choices=CHOICES)
    reservations = models.ManyToManyField(
        Conferences,
        through='Reservations',
        related_name='reservations'  
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural="participants"
    def __str__(self) :
        return f"cin de user  ={self.cin} , first_name = {self.first_name}"


class Reservations(models.Model):
    conference = models.ForeignKey(
        Conferences,
        on_delete=models.CASCADE,
        related_name='conference_reservations'  
    )
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name='participant_reservations' 
    )
    confirmed = models.BooleanField(default=False)
    reservation_date = models.DateTimeField(auto_now_add=True)
    def clean(self):
        if self.conference.start_date<datetime.now().date():
            raise ValidationError ('you can only reserve for upcoming conferences')
        reservation_count=Reservations.objects.filter(
            participant=self.participant,
            reservation_date=self.reservation_date
        ).count()
        if reservation_count>=3:
            raise ValidationError ('you can only reserve for 3 conferences at a time')
    class Meta:
        unique_together = ('conference', 'participant')
        verbose_name_plural="reservations"
