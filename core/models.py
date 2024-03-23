from django.db import models
from authen.models import CustomUser

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from django.contrib.auth import get_user_model
from milon.system.template import wordize
from enums import E_Status, E_StudentBatch

Base = declarative_base()


class StudentRequest(models.Model):
    subject = models.CharField(max_length=100)
    description = models.TextField()
    student_id = models.IntegerField()
    teacher_id = models.IntegerField()
    status = models.IntegerField()
    date = models.DateField()
    teacher_email = models.EmailField(max_length=100)
    student_no = models.TextField()
    batch_id = models.IntegerField()

    class Meta:
        db_table = 'student_requests'

    def __str__(self):
        return self.subject


class StudentRequestModel(Base):
    __tablename__ = 'student_requests'

    id = Column(Integer, primary_key=True)
    subject = Column(String)
    description = Column(String)
    student_id = Column(Integer)
    teacher_id = Column(Integer)
    status = Column(Integer)
    date = Column(Date)
    teacher_email = Column(String)
    student_no = Column(String)
    batch_id = Column(Integer)


def status_text(status_id):
    val = (int)(E_Status.Pending.index)
    if status_id:
        val = status_id
    return wordize(str(E_Status[val]))


def batch_text(batch_id):
    if batch_id:
        return wordize(str(E_StudentBatch[int(batch_id)]))
    return ''
