from django.urls import path
from core import views
from core import api

urlpatterns = [

    path('add_request/', views.add_request, name="add_request"),
    path('request_list/', views.request_list, name="request_list"),
    path('student_list/', views.student_list, name="student_list"),
    path('status_change/<int:request_id>/', views.status_change, name="status_change"),

]

urlpatterns += [
    path('api/request_data/', api.request_api, name="request_api"),
]
