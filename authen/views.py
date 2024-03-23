from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from authen.forms import SignUpForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from authen.models import CustomUser


class CustomLoginView(LoginView):
    template_name = 'auth/login.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)


def home(request, **kwargs):
    user_id = request.user.id
    user_obj = CustomUser.objects.get(id=user_id)
    is_teacher = False
    if user_obj.parent_id:
        is_teacher = True
    return render(request, 'auth/home.html', {'is_teacher': is_teacher})


from django.http import HttpResponseRedirect
from django.urls import reverse
import random
from core.task import send_email


def signup(request, **kwargs):
    role = request.GET.get('role', None)
    if request.method == 'POST':
        confirmation_code = request.POST.get('confirmation_code')
        if confirmation_code:
            if confirmation_code == request.session.get('confirmation_code'):
                signup_data = request.session.get('signup_data')
                form = SignUpForm(signup_data)
                if form.is_valid():
                    user = form.save(commit=False)
                    role = request.session.get('role')
                    if role == 'student':
                        teacher_id = request.session.get('teacher_id')
                        user.teacher_id = teacher_id
                    else:
                        parent_id = request.session.get('parent_id')
                        user.parent_id = parent_id
                    user = form.save()
                    raw_password = form.cleaned_data.get('password1')
                    user = authenticate(username=user.username, password=raw_password)
                    login(request, user)
                    return redirect('home')
            else:
                return render(request, 'auth/confirm_signup.html', {'error_message': 'Invalid confirmation code.'})
        else:
            form = SignUpForm(request.POST)
            if form.is_valid():
                signup_data = request.POST.dict()
                signup_data['role'] = role
                request.session['signup_data'] = signup_data
                if role == 'student':
                    teacher_id = request.POST.get('teacher_id')
                    request.session['teacher_id'] = teacher_id
                else:
                    parent_id = request.POST.get('parent_id')
                    request.session['parent_id'] = parent_id

                request.session['role'] = role
                confirmation_code = ''.join(random.choices('0123456789', k=6))
                request.session['confirmation_code'] = confirmation_code
                send_confirmation_email(request.POST['email'], confirmation_code)
                return HttpResponseRedirect(reverse('confirm_signup'))

    else:
        form = SignUpForm()

    from enums import E_Teachers
    teachers = E_Teachers.dict(empty=True)
    return render(request, 'auth/signup.html', {'form': form, 'role': role, 'teachers': teachers})


def send_confirmation_email(email, confirmation_code):
    subject = 'Confirmation Code for Approver System Registration!'
    message = f'<div><h3 style="color: crimson;">Your confirmation code is: <strong style="color: darkgreen; background-color: gold;">{confirmation_code}<strong></h3> </div>'
    send_email(email, email, subject, message)


def confirm_signup(request):
    return render(request, 'auth/confirm_signup.html', {})
