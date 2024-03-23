from django.http import JsonResponse
from authen.models import CustomUser
from core.models import StudentRequest
from django.db.models import Count


def query(teacher_id):
    result = (
        StudentRequest.objects
            .filter(teacher_id=teacher_id)
            .values('student_id')
            .annotate(student_count=Count('student_id'))
            .order_by('student_id')
    )
    return result


def request_api(request, **kwargs):
    user_id = request.user.id
    user_obj = CustomUser.objects.get(id=user_id)
    data_list = {
        'labels': [],
        'data_list': []
    }
    if user_obj.parent_id:
        teacher_id = user_obj.parent_id
    else:
        teacher_id = user_obj.teacher_id
    result = query(teacher_id)
    for item in result:
        student_id = item['student_id']
        full_name = CustomUser.objects.filter(id=student_id).values_list('full_name',
                                                                         flat=True).first() or f"User#{student_id}"
        data_list['labels'].append(full_name)
        data_list['data_list'].append(item['student_count'])

    return JsonResponse(data_list)
