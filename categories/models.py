from django.db import models # type: ignore
from django.core.validators import RegexValidator # type: ignore
import re
from django.core.exceptions import ValidationError # type: ignore

def validate_letters_only(value):
    if not re.match("^[a-zA-Z]*$", value):
        raise ValidationError("Only letters are allowed")
# Create your models here.
class Category(models.Model):
    letters_only=RegexValidator(r'^[A-Za-z\s]+$',message='only letters are allowed')
    title=models.CharField(max_length=255,validators=[validate_letters_only])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural="categories"
    def __str__(self) :
        return f"title  ={self.title} "
