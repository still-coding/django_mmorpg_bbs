from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Profile


class ProfileOtpCheckForm(forms.ModelForm):
   class Meta:
      model = Profile
      fields = ('otp',)


class ProfileUpdateForm(PermissionRequiredMixin, forms.ModelForm):
    permission_required = ('user_profiles.change_profile', )
    class Meta:
        model = Profile
        fields = ('mailing_period', 'avatar',)


class UserSignInForm(AuthenticationForm): 
    class Meta:
        model = User
        fields = ('username', 'password')



class UserSignUpForm(UserCreationForm):
    email = forms.EmailField()
   
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, **kwargs):
        user = super(UserSignUpForm, self).save()
        common_group = Group.objects.get_or_create(name='common')[0]
        common_group.user_set.add(user)
        return user


class UserUpdateForm(LoginRequiredMixin, forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', )
