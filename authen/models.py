from django.db import models
from django.contrib.auth.models import AbstractUser
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer

# Define the declarative base
Base = declarative_base()


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100, blank=False)
    age = models.PositiveIntegerField(null=True, blank=True)
    teacher_id = models.IntegerField(null=True, blank=True)
    parent_id = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=100, blank=False)


class CustomUserModel(Base):
    __tablename__ = 'authen_customuser'
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer)
    parent_id = Column(Integer)
