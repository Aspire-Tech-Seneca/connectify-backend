from django import forms
from .models import CustomUser, Review
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# form front kar hast

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['person_name', 'comment', 'rating']
        widgets = {
            'person_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your review here...', 'rows': 4}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'person_name': 'Name',
            'comment': 'Review',
            'rating': 'Rating (1-5 stars)',
        }

#--------------------------------------------------------------------------    
class UserCreationForm(forms.ModelForm):                    
    password1=forms.CharField(label="Password",widget=forms.PasswordInput)
    password2=forms.CharField(label="RePassword",widget=forms.PasswordInput)
    
    class Meta:                                            
        model=CustomUser
        fields=["mobile_number","email","name","family","gender"]

    def clean_password2(self):                             
        pass1=self.cleaned_data["password1"]
        pass2=self.cleaned_data["password2"]
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("Passwords are not matched")
        return True
    
    def save(self,commit=True):                            
        user=super().save(commit=False)                    
        user.set_password(self.cleaned_data["password1"])   
        user.save()                                        
        return user
    
#--------------------------------------------------------------------------    
class UserChangeForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField(help_text="For changing the Password <a href='../password'>click</a> here")            
    
    class Meta:
        model=CustomUser
        fields=["mobile_number","password","email","name","family","gender","is_active","is_admin"]

#--------------------------------------------------------------------------    
class RegisterUserForm(forms.ModelForm):
    class Meta:
        model=CustomUser            
        fields=["mobile_number","name","family","email"]                        
        widgets={                                                   
            "mobile_number":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Mobile Number"}),
            "name":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Your Name"}),
            "family":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Your Family"}),
            "email":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Your Email"})
        }    
    password1=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter your Password"}))
    password2=forms.CharField(label="Repeat Password",widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter your Repeat Password"}))
    
    def clean_password2(self):                            
        pass1=self.cleaned_data["password1"]
        pass2=self.cleaned_data["password2"]
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("Passwords are not matched")
        return True

#--------------------------------------------------------------------------    
class VerifyRegisterForm(forms.Form):
    active_code=forms.CharField(label="",
                                error_messages={"required":"this field can not left empty"},
                                widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter activation code"})        
                                )

#==========================================================================================
# Login
class LoginUserForm(forms.Form):
    mobile_number=forms.CharField(label="Mobile Number",
                                  error_messages={"required":"this field can not left empty"},
                                  widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Mobile"}))
    password=forms.CharField(label="Password",
                                error_messages={"required":"this field can not left empty"},
                                widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter password"})        
                                )

#=====================================================================================
# Forget Password
class ChangePasswordForm(forms.Form):
    password1=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter your Password"}))
    password2=forms.CharField(label="Repeat Password",widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter your Repeat Password"}))

    def clean_password2(self):                            
        pass1=self.cleaned_data["password1"]
        pass2=self.cleaned_data["password2"]
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("Passwords are not matched")
        return True
    
    
class SendCodeForm(forms.Form):
    mobile_number=forms.CharField(label="Mobile Number",
                                  error_messages={"required":"this field can not left empty"},
                                  widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Mobile"}))
    
class AuthCodeForm(forms.Form):
    active_code=forms.CharField(label="Active Code",
                                  error_messages={"required":"this field can not left empty"},
                                  widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter active code"}))

#=====================================================================================
class UpdateProfileForm(forms.Form):
    mobile_number=forms.CharField(label="",
                                  widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Mobile","readonly":"readonly"}))        # readonly bashe
    
    name=forms.CharField(label="",
                                  error_messages={'required':"this field can not be empty"},
                                  widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Name"}))
    
    family=forms.CharField(label="",
                                  error_messages={'required':"this field can not be empty"},
                                  widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Family"}))
    
    email=forms.CharField(label="",
                                  error_messages={'required':"this field can not be empty"},
                                  widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"Enter Email"}))
    
    phone_number=forms.CharField(label="",
                                  error_messages={'required':"this field can not be empty"},
                                  widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Phone Number"}))
    
    address=forms.CharField(label="",
                                  error_messages={'required':"this field can not be empty"},
                                  widget=forms.Textarea(attrs={"class":"form-control","placeholder":"Enter Address"}))
    
    image=forms.ImageField(required=False)
    