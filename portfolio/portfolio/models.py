from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.avi']
    if ext not in allowed_extensions:
        raise ValidationError(f'❌ الملف يجب أن يكون صورة أو فيديو (الامتدادات المسموحة: {", ".join(allowed_extensions)})')

def validate_video_size(value):
    file_size = value.size
    max_size = 50 * 1024 * 1024
    if file_size > max_size:
        raise ValidationError(f'❌ الحد الأقصى لحجم الفيديو هو 50MB، الحجم الحالي: {file_size / (1024*1024):.2f}MB')

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    media = models.FileField(
        upload_to='projects/',
        validators=[validate_file_extension],
        blank=True, null=True
    )

    # ✅ حقل جديد لرابط Google Drive
    google_drive_link = models.URLField(blank=True, null=True)

    github_link = models.URLField(blank=True, null=True)
    live_demo_link = models.URLField(blank=True, null=True)

    def clean(self):
        super().clean()
        if self.media and self.media.name.endswith(('.mp4', '.mov', '.avi')):
            validate_video_size(self.media)

class Certificate(models.Model):
    title = models.CharField(max_length=200)
    issued_by = models.CharField(max_length=200)
    date_received = models.DateField()
    image = models.ImageField(upload_to='certificate_images/', null=True, blank=True)

    google_drive_link = models.URLField(blank=True, null=True)



    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.name}'

    def save(self, *args, **kwargs):
        print(f"New Contact Message from: {self.name}, Email: {self.email}")
        super().save(*args, **kwargs)
