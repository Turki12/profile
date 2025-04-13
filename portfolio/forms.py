from django import forms
from .models import Project, Certificate, ContactMessage

# نموذج إدخال بيانات المشروع
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'media', 'google_drive_link', 'github_link','live_demo_link']


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['title', 'issued_by', 'date_received', 'image','google_drive_link']

# نموذج إدخال رسائل التواصل
class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
