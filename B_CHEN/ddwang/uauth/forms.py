from django import forms
from .models import Customer

class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=25, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username",'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "Password"}))
    class Meta:
        model = Customer
        field = ('cname')

class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ctel = forms.CharField(label='手机号码', max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ChangepasswordForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    oldpassword = forms.CharField(label="旧密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    newpassword1 = forms.CharField(label="新密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    newpassword2 = forms.CharField(label="确认新密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# class shopping_cart(forms.Form):
#    books = forms.ModelChoiceField(queryset=books.objects.all(), required=False, help_text="Books")