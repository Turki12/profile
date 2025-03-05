from django.shortcuts import render
from .models import Project




def base(request):
    projects = Project.objects.all()
    return render(request, 'base.html',{'project': projects})

def home(request):
    return render(request, 'home.html')

# def about(request):
#     return render(request, 'about.html')

# def gallery(request):
#     return render(request, 'gallery.html')

# def contact(request):
#     return render(request, 'contact.html')