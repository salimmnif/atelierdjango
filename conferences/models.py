from django.db import models # type: ignore
from  categories.models import Category
from django.core.validators import MaxValueValidator,FileExtensionValidator # type: ignore
from datetime import datetime

from django.core.exceptions import ValidationError # type: ignore




class Conferences(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    start_date=models.DateField(default=datetime.now().date())
    end_date=models.DateField()
    location=models.CharField(max_length=255)
    price=models.FloatField()
    capacity=models.IntegerField(validators=[MaxValueValidator(limit_value=50,message='capacity under 50')])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    program=models.FileField(upload_to='files/',validators=[FileExtensionValidator(allowed_extensions=['pdf','png','jpeg'],message='only pdf,pngand jpeg are allowed')])
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='conferences')
    def clean(self) :
        if self.start_date > self.end_date:
            raise ValidationError("start date must be less than end date")
    class Meta:
        verbose_name_plural="conferences"  
        constraints=[
            models.CheckConstraint(check=models.Q(start_date__gte=datetime.now().date()),name='the startdate must be greater or equal than today')
        ]  
    def __str__(self) :
        return f"titre de la confernece ={self.title} , location = {self.location} , price={self.price}"
