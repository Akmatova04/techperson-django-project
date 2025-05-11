# learning_hub/urls.py
from django.urls import path
from . import views

app_name = 'learning_hub'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('courses/', views.course_list_view, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail_view, name='course_detail'),
    path('courses/<int:course_id>/enroll/', views.enroll_in_course_view, name='enroll_in_course'),
    
    path('mentors/', views.mentor_list_view, name='mentor_list'),
    path('mentors/<int:mentor_id>/', views.mentor_detail_view, name='mentor_detail'),
    path('mentors/<int:mentor_id>/add_review/', views.add_mentor_review_view, name='add_mentor_review'),

    path('contact/', views.contact_view, name='contact'),
    path('contact/success/', views.contact_success_view, name='contact_success'),

    path('search/', views.search_results_view, name='search_results'), # <-- ИЗДӨӨ URL'И
]