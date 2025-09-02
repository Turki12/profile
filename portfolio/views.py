from urllib import request
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Certificate, Project
from .forms import ContactMessageForm, ProjectForm
from django.contrib.auth import login
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlencode
from django.http import JsonResponse
from .models import Project
from django.conf import settings
from django.templatetags.static import static
from .models import Project, Certificate


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class CustomLoginView(LoginView):
    model = Project
    template_name = "auth/login.html"
    # This is the line you need to change.
    # It redirects to the URL with the name 'project-add'.
    success_url = reverse_lazy("project-add")
    
    def form_valid(self, form):
        print("✅ تسجيل دخول ناجح للمستخدم:", form.get_user())
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("❌ فشل تسجيل الدخول")
        return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    next_page = "auth/login.html"
    
    def dispatch(self, request, *args, **kwargs):
        print("👋 تسجيل خروج المستخدم:", request.user)
        return super().dispatch(request, *args, **kwargs)

class ProjectListView(ListView):
    model = Project
    template_name = "portfolio/home.html"
    context_object_name = "projects"
    
    def get_queryset(self):
        print("📌 عرض قائمة المشاريع")
        return super().get_queryset()

class Home_ListView(ListView):
    model = Project
    template_name = "portfolio/home.html"
    context_object_name = "projects"
    
    def get_queryset(self):
        print("🏠 عرض الصفحة الرئيسية")
        return super().get_queryset()
    
def home(request):
    projects = Project.objects.all()
    certificates = Certificate.objects.all()
    for i, cert in enumerate(certificates):
        cert.delay = f"{i * 0.2:.1f}"

    return render(request, 'portfolio/home.html', {
        'projects': projects,
        'certificates': certificates,
    })
    

def project_detail(request, pk):
    print(f"🔍 عرض تفاصيل المشروع ID: {pk}")
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'portfolio/project_detail.html', {'project': project})

class ProjectCreateView(AdminRequiredMixin, LoginRequiredMixin, CreateView):
    model = Project
    template_name = "portfolio/project_form.html"
    fields = ["title", "description", "media","github_link","live_demo_link"]
    success_url = reverse_lazy("project-list")
    
    def form_valid(self, form):
        print("✅ إنشاء مشروع جديد:", form.cleaned_data)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("❌ فشل إنشاء المشروع، الأخطاء:", form.errors)
        return super().form_invalid(form)

class ProjectUpdateView(AdminRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Project
    template_name = "portfolio/project_form.html"
    fields = ["title", "description", "media", "link","live_demo_link"]
    success_url = reverse_lazy("project-list")
    
    def form_valid(self, form):
        print("✅ تحديث المشروع:", form.cleaned_data)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("❌ فشل تحديث المشروع، الأخطاء:", form.errors)
        return super().form_invalid(form)

class ProjectDeleteView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "portfolio/project_confirm_delete.html"
    success_url = reverse_lazy("project-list")
    
    def delete(self, request, *args, **kwargs):
        project = self.get_object()
        print(f"🗑️ حذف المشروع: {project.name} (ID: {project.id})")
        return super().delete(request, *args, **kwargs)
    
    

class ContactView(FormView):
    template_name = "portfolio/contact.html"
    form_class = ContactMessageForm
    success_url = reverse_lazy('contact_success')

    def form_valid(self, form):
        # استخراج البيانات من النموذج
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        # إرسال البريد الإلكتروني
        send_mail(
            subject=f"New Contact Form Submission from {name}",
            message=f"Sender: {name} \nEmail: {email} \n\nMessage:\n{message}",
            from_email=settings.EMAIL_HOST_USER,  # يجب أن يكون مطابقًا لحساب SMTP
            recipient_list=['turkialshehri168@gmail.com'],  # ضع بريدك الإلكتروني هنا
            fail_silently=False,  # يُظهر الأخطاء في حال فشل الإرسال
        )
        phone_number = "YOUR_PHONE_NUMBER"  # استبدل هذا برقم WhatsApp الخاص بك مع كود الدولة
        text_message = f"Hello, my name is {name}. My email is {email}. Here is my message:\n{message}"
        encoded_text = urlencode({"text": text_message})
        whatsapp_link = f"https://api.whatsapp.com/send?phone={phone_number}&{encoded_text}"

        # تمرير الرابط إلى `context`
        self.request.session['whatsapp_link'] = whatsapp_link

        return super().form_valid(form)
    
class ContactSuccessView(TemplateView):
    template_name = "portfolio/contact_success.html"



def project_list(request):
    projects = Project.objects.all()
    project_data = []
    for project in projects:
        media_url = project.media.url if project.media else static('media/projects')
        project_data.append({
            'title': project.title,
            'description': project.description,
            'media': request.build_absolute_uri(media_url),
            'github_link': project.github_link,
            'live_demo_link': project.live_demo_link,
        })
    return JsonResponse({'projects': project_data})
