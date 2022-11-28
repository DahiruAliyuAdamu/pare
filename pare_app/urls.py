from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('staffDetail', views.staffDetail, name='staffDetail'),
    path('staffDetail/edit/<int:p_id>', views.staffEdit, name='staffEdit'),
    path('staffDetail/delete/<int:p_id>', views.staffDelete, name='staffDelete'),
    path('addTraining/', views.addTraining, name='addTraining'),
    path('viewTraining/', views.viewTraining, name='viewTraining'),
    path('addBeneficiary', views. addBeneficiary, name='beneficiary'),
    path('viewBeneficiary', views.viewBeneficiary, name='viewBeneficiary'),
    path('ajax/beneficiary/search/', views.searchBeneficiary, name='searchData'),
    path('complaint/', views.complaints, name='complaint'),
    path('view_complaint/', views.viewComplaint, name='view_complaint'),
    path('view_complaint/viewsingleFeedback/<int:p_id>/', views.viewsingleFeedback, name='viewsingleFeedback'),
    path('attendance/', views.attendance, name='attendance'),
    path('attendance/add/take/', views.takeAttendance, name='takeAttendance'),


    path('attendance/add/', views.add_attendance, name='add_attendance'),
    path('attendance_detail' , views.attendance_detail, name='attendance_detail'),
    path('viewAttendance/', views.viewAttendance, name='viewAttendance'),

    path('logout/', views.pareLogout, name='pareLogout'),
]