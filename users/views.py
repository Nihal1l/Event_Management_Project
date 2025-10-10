from asyncio import Event
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
# from users.forms import AssignRoleForm, CreateGroupForm, LoginForm, EditProfileForm
from .forms import *
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import View
from django.views.generic import TemplateView, UpdateView
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView

User = get_user_model()


def is_admin(user):
    return user.groups.filter(name='Admin').exists()


"""def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(
                request, 'A Confirmation mail sent. Please check your email')
            return redirect('sign-in')

        else:
            print("Form is not valid")
    return render(request, 'registration/register.html', {"form": form})"""

class SignUpView(View):
    form_class = CustomRegistrationForm
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(
                request, 'A Confirmation mail sent. Please check your email')
            return redirect('sign-in')
        else:
            print("Form is not valid")
        return render(request, self.template_name, {"form": form})

class SignInView(View):
    form_class = LoginForm
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})

class SignOutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('sign-in')

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')
    

"""# @user_passes_test(is_admin, login_url='no-permission')
# def user_list(request):

#     users = User.objects.prefetch_related(
#         Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
#     ).all()

#     for user in users:
#         if user.all_groups:
#             user.group_name = user.all_groups[0].name
#         else:
#             user.group_name = 'No Group Assigned'
#     return render(request, 'admin/user_list.html', {"users": users})"""


user_passes_test_decorators = [login_required, user_passes_test(is_admin, login_url='no-permission')]
@method_decorator(user_passes_test_decorators, name='dispatch')
class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'admin/user_list.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_queryset(self):
        users = User.objects.prefetch_related(
            Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
        ).all()

        for user in users:
            if user.all_groups:
                user.group_name = user.all_groups[0].name
            else:
                user.group_name = 'No Group Assigned'
        return users



"""# @user_passes_test(is_admin, login_url='no-permission')
# def assign_role(request, user_id):
#     user_id = User.objects.get(id=user_id)
#     form = AssignRoleForm()

#     if request.method == 'POST':
#         form = AssignRoleForm(request.POST)
#         if form.is_valid():
#             user_id = form.cleaned_data.get('user_id')
#             role = form.cleaned_data.get('role')
#             user_id.groups.clear()  # Remove old roles
#             user_id.groups.add(role)
#             messages.success(request, f"User {user_id.username} has been assigned to the {role.name} role")
#             return redirect('admin-dashboard')

#     return render(request, 'admin/assign_role.html', {"form": form, "user_id": user_id})"""

@method_decorator(user_passes_test_decorators, name='dispatch')
class AssignRoleView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'admin/assign_role.html'
    context_object_name = 'users'
    form_class = AssignRoleForm

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_queryset(self):
        return User.objects.all()

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data.get('user_id')
            role = form.cleaned_data.get('role')
            user_id.groups.clear()  # Remove old roles
            user_id.groups.add(role)
            messages.success(request, f"User {user_id.username} has been assigned to the {role.name} role")
            return redirect('admin-dashboard')
        return render(request, self.template_name, {"form": form})



"""@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created successfully")
            return redirect('create-group')

    return render(request, 'admin/create_group.html', {'form': form})"""

@method_decorator(user_passes_test_decorators, name='dispatch')
class CreateGroupView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Group
    template_name = 'admin/create_group.html'
    context_object_name = 'groups'
    form_class = CreateGroupForm

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_queryset(self):
        return Group.objects.all()

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created successfully")
            return redirect('create-group')
        return render(request, self.template_name, {'form': form})


"""@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})"""

@method_decorator(user_passes_test_decorators, name='dispatch')
class GroupListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Group
    template_name = 'admin/group_list.html'
    context_object_name = 'groups'

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_queryset(self):
        return Group.objects.prefetch_related('permissions').all()
 

class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['phone_number'] = user.phone_number
        context['profile_image'] = user.profile_image
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        return context
    


class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect('profile')


def is_admin(user):
    return user.groups.filter(name='Admin').exists()

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'registration/reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        print(context)
        return context

    def form_valid(self, form):
        messages.success(
            self.request, 'A Reset email sent. Please check your email')
        return super().form_valid(form)

class ChangePassword(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm

    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully')
        return super().form_valid(form)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(
            self.request, 'Password reset successfully')
        return super().form_valid(form)
