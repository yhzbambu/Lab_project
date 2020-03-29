from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
class LoginForm(forms.Form):
    username=forms.CharField(label="用戶名",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'請輸入用戶名'}))
    password=forms.CharField(label="密碼",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'請輸入密碼'}))

    def clean(self):
        username=self.cleaned_data['username']
        password=self.cleaned_data['password']
        user=auth.authenticate(username=username,password=password)
        if user is None:
            raise forms.ValidationError('用戶名或密碼不正確')
        else:
            self.cleaned_data['user']=user
        return self.cleaned_data    
class RegForm(forms.Form):
    username= forms.CharField(label='用戶名',
                                max_length=30,
                                min_length=3,
                                widget=forms.TextInput(
                                    attrs={'class':'form-control','placeholder':'請輸入3~30位用戶名'}
                                ))
    email= forms.CharField(label='郵件',
                                widget=forms.EmailInput(
                                    attrs={'class':'form-control','placeholder':'請輸入郵件'}
                                ))
    password = forms.CharField(label='密碼',
                                max_length=16,
                                min_length=8,
                                widget=forms.PasswordInput(
                                    attrs={'class':'form-control','placeholder':'請輸入8~16位密碼'}
                                ))
    password_again= forms.CharField(label='再輸入一次密碼',
                                max_length=16,
                                min_length=8,
                                widget=forms.PasswordInput(
                                    attrs={'class':'form-control','placeholder':'請再輸入一次密碼'}
                                ))
    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用戶名已存在')
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('用郵件已使用過')
    
    def clean_password_again(self):
        password=self.cleaned_data['password']
        password_again=self.cleaned_data['password_again']
        if password !=password_again:
            raise forms.ValidationError('輸入的密碼不一致')  
        return password_again  