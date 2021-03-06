from django import forms
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from accounts.models import File

from django.views.generic import View

from accounts.forms import UploadForm
# Create your views here.

@login_required
def index(request):
    if request.user.is_authenticated:
        data = {'username':request.user.username}
        return render(request, 'index.html', context=data)
    else:
        return render(request, 'index.html')

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Account Not Active")

        else:
            context = {'notfound':True}
            print(f"NO ACCOUNT FOUND WITH USERNAME {username} AND PASSWORD {password}")
            print(context)
            return render(request, 'accounts/login.html',context)

    else:
        return render(request, 'accounts/login.html')

# def uploadPage(request):
#     return render(request, 'accounts/upload.html')

class UploadView(View):
    def get(self, request):
        form = UploadForm()
        file_obj = File.objects.all()
        return render(request, 'accounts/upload.html', context={'form':form, 'files':file_obj})

    def post(self, request):
        if request.method == 'POST':
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                data = {
                    'data_saved':True
                }

                return JsonResponse(data)
            else: 
                return JsonResponse({'error': True, 'errors': form.errors})

@login_required
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('home'))

def deleteFile(request):
    if request.is_ajax():
        file_id = request.GET.get('file_id')
        file_obj = get_object_or_404(File, id=file_id)
        file_obj.delete()
        return JsonResponse({'Deleted':True})