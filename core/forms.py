# core/forms.py
from django import forms

from core.models import StudentRequest
import re


class StudentRequestForm(forms.ModelForm):
    class Meta:
        model = StudentRequest
        fields = ['subject', 'description', 'date', 'teacher_email', 'student_no', 'batch_id']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(StudentRequestForm, self).__init__(*args, **kwargs)

    def clean_student_no(self):
        student_no = self.cleaned_data.get('student_no')
        user_id = self.request.user.id
        pending_requests_count = StudentRequest.objects.filter(student_id=user_id, status=1).count()
        if pending_requests_count >= 2:
            error_msg = 'You cannot make more than two requests while request statuses are pending.'
            raise forms.ValidationError(error_msg)
        return student_no

    def clean_teacher_email(self):
        teacher_email = self.cleaned_data.get('teacher_email')

        email_regex = r'^\w+@mbstu\.ac\.bd$'
        if not re.match(email_regex, teacher_email):
            raise forms.ValidationError('Email must be in the format ex@mbstu.ac.bd')

        return teacher_email

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
