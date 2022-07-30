from tempfile import tempdir
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.core.signing import BadSignature

from . import models as model
from .forms import ChangeUserInfoForm, RegisterUserForm
from .utilities import signer

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))

class EALoginView(LoginView):
    template_name = 'main/login.html'

@login_required
def profile(request):
    return render(request, 'main/profile.html')

class EALogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'

class ChangeUserInfoView(SuccessMessageMixin,
    LoginRequiredMixin, UpdateView):
    model = model.AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

class EAPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin,
                                            PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменен'

class RegisterUserView(CreateView):
    model = model.AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')

class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'

def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(model.AdvUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)

class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = model.AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удалён')
        return super().post(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

@login_required
def tools_page(request, tool):
    context = {}
    try:
        template = get_template('main/tools/' + tool + '.html')
        if tool == 'connections':
            context['connections'] = [model.Connection.objects.all(), model.CSV_File.objects.all()]
            print(context)
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(context=context,request=request))

@login_required
def csv_upload(request):
    if request.method == 'POST':
        my_file=request.FILES.get('file')
        model.Connection.objects.create(user_id=request.user, name=str(my_file), connection_type='CSV')
        model.CSV_File.objects.create(file=my_file, connection_id=model.Connection.objects.latest('pk'))
        return HttpResponse('')
    return JsonResponse({'post':'false'})