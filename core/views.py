from django.shortcuts import render, redirect
from core.forms import StudentRequestForm, StudentRequest
from core.models import StudentRequestModel, status_text, batch_text
from DB.db import create_session
from sqlalchemy import select
from authen.models import CustomUserModel, CustomUser
from datetime import datetime
from core.task import send_email
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from core.templates import email_template


def add_request(request, **kwargs):
    used_id = None
    if request.user:
        used_id = request.user.id
    date_today = datetime.now().strftime('%Y-%m-%d')

    if request.method == 'POST':
        form = StudentRequestForm(request.POST, request=request)
        session = create_session()
        stmt = select([CustomUserModel.teacher_id]).where(CustomUserModel.id == used_id)
        t_id = session.execute(stmt).scalar()
        if form.is_valid():
            try:
                subject = form.cleaned_data['subject']
                description = form.cleaned_data['description']
                date = form.cleaned_data['date']
                teacher_email = form.cleaned_data['teacher_email']
                student_no = form.cleaned_data['student_no']
                batch_id = form.cleaned_data['batch_id']
                student_id = used_id
                teacher_id = None
                if t_id:
                    teacher_id = t_id
                new_request = StudentRequestModel(subject=subject, description=description, student_id=student_id,
                                                  teacher_id=teacher_id, status=1, date=date,
                                                  teacher_email=teacher_email, student_no=student_no, batch_id=batch_id)
                session.add(new_request)

                user = CustomUser.objects.get(pk=used_id)
                teacher_obj = CustomUser.objects.get(parent_id=teacher_id)
                batch_name = batch_text(batch_id)
                message_template = email_template(user.full_name, teacher_obj.full_name, subject, description,
                                                  student_no, date, user.email, batch_name)

                send_email(teacher_email, teacher_email, subject, message_template)
                session.commit()
                session.close()
            except Exception as e:
                raise e

            return redirect('home')

    else:
        form = StudentRequestForm(request=request)
    from enums import E_StudentBatch
    batch = E_StudentBatch.dict(empty=True)
    return render(request, 'auth/add_request.html', {'form': form, 'date_today': date_today, 'batch': batch})


def student_list(request, **kwargs):
    user_id = request.user.id
    user_obj = CustomUser.objects.get(pk=user_id)
    par_id = user_obj.parent_id
    if par_id is None:
        teacher_id = user_obj.teacher_id
    else:
        teacher_id = par_id
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        students = CustomUser.objects.filter(teacher_id=teacher_id).values('id', 'full_name', 'email')
        data = []
        for student in students:
            student_id = student.get('id')
            student_obj = StudentRequest.objects.filter(student_id=student_id).first()
            if student_obj:
                batch_id = student_obj.batch_id
                student['batch_name'] = batch_text(batch_id)
                student['student_no'] = student_obj.student_no
            else:
                student['batch_name'] = ''
                student['student_no'] = ''
            data.append(student)
        return JsonResponse({'requests': data})
    return render(request, 'auth/student_list.html')


def request_list(request, **kwargs):
    user_id = request.user.id
    is_teacher = False
    session = create_session()
    stmt = select([CustomUserModel.parent_id]).where(CustomUserModel.id == user_id)
    t_parent_id = session.execute(stmt).scalar()
    if t_parent_id:
        is_teacher = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if is_teacher:
            requests = StudentRequest.objects.filter(teacher_id=t_parent_id).values('id', 'subject', 'description',
                                                                                    'teacher_email', 'date',
                                                                                    'student_id', 'teacher_id',
                                                                                    'status', 'student_no', 'batch_id')
        else:
            requests = StudentRequest.objects.filter(student_id=user_id).values('id', 'subject', 'description',
                                                                                'teacher_email', 'date', 'student_id',
                                                                                'teacher_id', 'status', 'student_no',
                                                                                'batch_id')
        data = []
        for request_data in requests:
            student_id = request_data.get('student_id')
            teacher_id = request_data.get('teacher_id')
            status_id = request_data.get('status')
            batch_id = request_data.get('batch_id')
            student = get_user_model().objects.get(id=student_id)
            teacher = get_user_model().objects.get(parent_id=teacher_id)
            student_name = student.full_name
            teacher_name = teacher.full_name
            request_data['student_name'] = student_name
            request_data['teacher_name'] = teacher_name
            request_data['status'] = status_text(status_id)
            request_data['batch_name'] = batch_text(batch_id)
            data.append(request_data)
        return JsonResponse({'requests': data})
    return render(request, 'auth/request_list.html', {'is_teacher': is_teacher})


def status_mail_send(full_name, status_id, from_email, to_email, request_obj, status_flag):
    if status_flag == '0':
        subject = 'Request Rejected'
        message = 'Hello Dear, ' + full_name + '\nYour Request Has been Rejected.'
    else:
        subject = 'Request Approved'
        message = 'Hello Dear, ' + full_name + '\nYour Request Has been Approved.'
    try:
        send_email(from_email, to_email, subject, message)
        request_obj.status = status_id
        request_obj.save()
    except Exception as e:
        raise e


def status_change(request, request_id, **kwargs):
    uses_id = request.user.id
    status_flag = request.GET.get('status')

    request_obj = StudentRequest.objects.get(pk=request_id)
    from enums import E_Status
    if request_obj.status == E_Status.Approved.index:
        return JsonResponse({'error': 'Status has been already approved'}, status=400)
    if request_obj.status == E_Status.Rejected.index:
        return JsonResponse({'error': 'Status has been already Rejected'}, status=400)

    teacher = get_user_model().objects.get(pk=uses_id)
    student = get_user_model().objects.get(pk=request_obj.student_id)
    from_email = teacher.email
    to_email = student.email
    try:
        if status_flag == '1':
            status_mail_send(student.full_name, E_Status.Approved.index, from_email, to_email, request_obj, status_flag)
        else:
            status_mail_send(student.full_name, E_Status.Rejected.index, from_email, to_email, request_obj, status_flag)
    except Exception as e:
        raise e

    return redirect('/request/request_list')
