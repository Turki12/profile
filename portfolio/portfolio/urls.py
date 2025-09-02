from django import views
from django.urls import path
from .views import home, project_list,Certificate
from .views import (
     Home_ListView, ProjectListView, project_detail,
    ProjectCreateView, ProjectUpdateView, ProjectDeleteView,CustomLoginView, CustomLogoutView,ContactView,ContactSuccessView
)
# from django.contrib.auth.views import CustomLoginView, CustomLogoutView

urlpatterns = [
    # ✅ الصفحة الرئيسية العامة
   path('', home, name='home'),

    # ✅ صفحة تحكم المشرف
    path('control/', Home_ListView.as_view(), name='control-page'),

    # ✅ عرض جميع المشاريع
    path('projects/', ProjectListView.as_view(), name='project-list'),

    # ✅ عرض تفاصيل المشروع
    path('projects/<int:pk>/', project_detail, name='project-detail'),

    # ✅ إضافة مشروع جديد (للمشرف فقط)
    path('projects/add/', ProjectCreateView.as_view(), name='project-add'),

    # ✅ تحديث مشروع موجود (للمشرف فقط)
    path('projects/edit/<int:pk>/', ProjectUpdateView.as_view(), name='project-edit'),

    # ✅ حذف مشروع (للمشرف فقط)
    path('projects/delete/<int:pk>/', ProjectDeleteView.as_view(), name='project-delete'),

    # ✅ تسجيل الدخول والخروج
    path('login/', CustomLoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', CustomLogoutView.as_view(next_page='/'), name='logout'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/success/', ContactSuccessView.as_view(), name='contact_success'),

    path('api/projects/', project_list, name='project_list'),
   
    path('api/Certificates/', Certificate, name='Certificate_list'), 


]
