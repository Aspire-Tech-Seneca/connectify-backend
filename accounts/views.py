<<<<<<< HEAD
from django.shortcuts import render,redirect
from django.views import View
from .forms import RegisterUserForm, VerifyRegisterForm, LoginUserForm, ChangePasswordForm, SendCodeForm, AuthCodeForm, UpdateProfileForm
from .models import CustomUser, Customer
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
import utils
from apps.orders.models import Order
from apps.payments.models import Payment
from django.contrib.auth.decorators import login_required

#=====================================================================================
# register
class RegisterUserView(View):
    template_name="accounts_app/register.html"
    
    def dispatch(self, request, *args, **kwargs):                               
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):                    
        form=RegisterUserForm()
        return render(request,self.template_name,{"form":form})
    
    def post(self, request, *args, **kwargs):                   
        form=RegisterUserForm(request.POST)
        
        if form.is_valid():
            data=form.cleaned_data
            active_code= utils.create_random_code(5)
            CustomUser.objects.create_user(
                mobile_number=data["mobile_number"],
                email=data["email"],
                name=data["name"],
                family=data["family"],
                active_code=active_code,
                password=data["password1"],
            )
            
            utils.send_sms(data["mobile_number"],f"{active_code}")          
                                                                            
            request.session["user_session"]={                               
                "active_code":str(active_code),
                "mobile_number":data["mobile_number"],
                "password":data["password1"],
            }
            
            messages.success(request,"Your information is saved. Please enter activation code","success")
            
            return redirect("accounts:verify")                                
        messages.error(request,"Input data is not correct","danger")
        return render(request,self.template_name,{"form":form})

#-------------------------------------------------------------------------------  
class VerifyRegisterCodeView(View):
    template_name="accounts_app/verify_register.html"
    
    def dispatch(self, request, *args, **kwargs):                               
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form=VerifyRegisterForm()
        return render(request,self.template_name,{"form":form})
    
    def post(self, request, *args, **kwargs):
        form=VerifyRegisterForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user_session=request.session["user_session"]                      
            if data["active_code"]==user_session["active_code"]:
                user=CustomUser.objects.get(mobile_number=user_session["mobile_number"]) 
                user.is_active=True
                user.active_code=utils.create_random_code(5)                  
                user.save()
                messages.success(request,"You are registered","success")
                user=authenticate(username=user_session["mobile_number"],password=user_session["password"])
                login(request,user) 
                return redirect("main:index")
            else:
                messages.error(request,"activation code is wrong","danger")
                return render(request,self.template_name,{"form":form})       
        
        messages.error(request,"Data is not valid","success")
        return render(request,self.template_name,{"form":form})   
                
#=====================================================================================
#login

class LoginUserView(View):
    template_name="accounts_app/login.html"
    
    def dispatch(self, request, *args, **kwargs):         
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form=LoginUserForm()
        return render(request,"accounts_app/login.html",{"form":form})

    def post(self, request, *args, **kwargs):
        form=LoginUserForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=authenticate(username=data["mobile_number"],password=data["password"])            
            if user is not None:
                db_user=CustomUser.objects.get(mobile_number=data["mobile_number"])
                if db_user.is_admin==False:
                    messages.success(request,"Login is successfull","success")
                    login(request,user)                                                                  # login
                    next_url=request.GET.get("next")                                                     
                    if next_url is not None:
                        return redirect(next_url)
                    else:
                        return redirect("main:index")
                else:
                    messages.error(request,"admin user can not login from here","danger")
                    return render(request,self.template_name,{"form":form})
            else:
                messages.error(request,"Information is not correct","danger")
                return render(request,self.template_name,{"form":form})
            
        messages.error(request,"Information is not valid","danger")
        return render(request,self.template_name,{"form":form})
        
        
class LogoutUserView(View):
    def dispatch(self, request, *args, **kwargs):                               
        if request.user.is_authenticated==False:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        shop_cart=request.session.get("shop_cart")                            
        logout(request)                                                       
        request.session["shop_cart"]=shop_cart                                
        messages.success(request,"Logout successfully","success")
        return redirect("main:index")
    
#=====================================================================================
# Forget Password
#step2
class ChangePasswordView(View):
    template_name="accounts_app/change_password.html"
    
    def get(self, request, *args, **kwargs):
        type=kwargs['type']                
        if type==1:
            template='user_panel_template.html'
        else: 
            template='main_template.html'
        
        form=ChangePasswordForm()  
        return render(request,self.template_name,{"form":form,'template':template})
    
    def post(self, request, *args, **kwargs):
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            try:                 
                request.session["user_session"]          
                user_session=request.session["user_session"]
                user=CustomUser.objects.get(mobile_number=user_session["mobile_number"])
            except:              
                user=CustomUser.objects.get(id=request.user.id)
            
            user.set_password(data["password1"])
            user.active_code=utils.create_random_code(5)
            user.save()
            messages.success(request,"Password has been changed","success")
            
            try: 
                request.session["user_session"]          
                return redirect("accounts:login")
            except:
                return redirect("accounts:userpanel")
        
        else:
            messages.error(request,"Input is wrong","danger")
            return render(request,self.template_name,{"form":form})
        
#-----------------------------------------------------------------------------------
#step1
class SendCodeView(View):
    template_name="accounts_app/SendCode.html"
    
    def get(self, request, *args, **kwargs):
        form=SendCodeForm()
        return render(request,self.template_name,{"form":form})
    
    def post(self, request, *args, **kwargs):
        form=SendCodeForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            try:
                user=CustomUser.objects.get(mobile_number=data["mobile_number"])                    
                active_code=utils.create_random_code(5)
                user.active_code=active_code
                user.save()
                utils.send_sms(data["mobile_number"],f"your activation code is {active_code}")
            
                request.session["user_session"]={                                   
                "active_code":str(active_code),
                "mobile_number":data["mobile_number"]
                }
                messages.success(request,"Enter your code here","success")
                return redirect("accounts:AuthCode")
            
            except:
                messages.error(request,"This mobile number is not exists","danger")
                return render(request,self.template_name,{"form":form})
        
class AuthCodeView(View):
    template_name="accounts_app/AuthCode.html"
    
    def get(self, request, *args, **kwargs):
        form=AuthCodeForm()
        return render (request,self.template_name,{"form":form})
    
    def post(self, request, *args, **kwargs):
        form=AuthCodeForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user_session=request.session["user_session"]                           
            if data["active_code"]==user_session["active_code"]:
                return redirect("accounts:change_password", "0")                   
        
            messages.error(request,"Code is wrong","danger")
            form=AuthCodeForm()                                                    
            return render(request,self.template_name,{"form":form})


#=====================================================================================
class UserPanelView(LoginRequiredMixin,View):                                   
    def get(self,request):
        user=request.user
        try:
            customer=Customer.objects.get(user=request.user)                    
            user_info={
                "name":user.name,
                "family":user.family,
                "email":user.email,
                "phone_number":user.mobile_number,
                "address":customer.address,
                "image":customer.image_name,
            }
        except:
            user_info={                                                         
                "name":user.name,
                "family":user.family,
                "email":user.email,
                "phone_number":user.mobile_number,
            }
        return render(request,"accounts_app/userpanel.html", {"user_info":user_info})

#-----------------------------------------------------------------------------------
@login_required                                                                
def show_last_orders(request):
    orders=Order.objects.filter(customer=request.user.id).order_by("-register_date")[:4]
    return render(request,"accounts_app/partials/show_last_orders.html", {"orders":orders})
    
#-----------------------------------------------------------------------------------
class UpdateProfileView(LoginRequiredMixin,View):
    def get(self,request):
        user=request.user
        try:
            customer=Customer.objects.get(user=request.user)                        
            user_info={
                "mobile_number":user.mobile_number,
                "name":user.name,
                "family":user.family,
                "email":user.email,
                "address":customer.address,
            }
        except:
            user_info={                                                         
                "mobile_number":user.mobile_number,
                "name":user.name,
                "family":user.family,
                "email":user.email,
            }
        
        form=UpdateProfileForm(initial=user_info)                              
        return render(request,"accounts_app/update_profile.html",{"form":form,"image_url":customer.image_name})
    
    def post(self,request):    
        form=UpdateProfileForm(request.POST,request.FILES)
        
        if form.is_valid():
            cd=form.cleaned_data
            user=request.user
            user.name=cd['name']
            user.family=cd['family']
            user.email=cd['email']
            user.save()
            try:
                customer=Customer.objects.get(user=request.user)
                customer.phone_number=cd['phone_number']
                customer.address=cd['address']
                print("ssss",cd['image'])
                if cd['image']:
                    customer.image_name=cd['image']
                customer.save()
            except Exception:
                Customer.objects.create(
                    user=request.user,
                    phone_number=cd['phone_number'],
                    address=cd['address'],
                    image_name=cd['image']
                )    
            messages.success(request,'edit is done','success')
            return redirect("accounts:userpanel")
        
        else:
            
            messages.error(request,'data is not valid','danger')
            return render("accounts_app/update_profile.html",{'form':form})
            
#-----------------------------------------------------------------------------------
@login_required
def show_user_payments(request):
    payments=Payment.objects.filter(customer_id=request.user.id).order_by('-register_date')
    return render(request,"accounts_app/show_user_payments.html", {"payments":payments})
        
=======
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

from mongoengine import connect
import datetime

from accounts.models import UserProfile


# Create a new user profile
@api_view(['POST'])
def create_user_profile(request):

    if request.method == 'POST':
        # Initialize the user_profile with the data received in the request
        user_profile = UserProfile(
            username=request.data.get('username'),
            email=request.data.get('email'),
            password=request.data.get('password'),
            first_name=request.data.get('first_name'),
            last_name=request.data.get('last_name')
            # profile_picture='default.jpg',
            # date_of_birth='1990-01-01',
            # age=(datetime.date.today() - dob).days // 365,
            # gender=gender,
            # location=location,
            # interests=interests,
            # bio='This is my bio',
            # age_range=(20, 30),
            # preferred_genders=['Male', 'Female'],
            # matched_users=[],
            # pending_requests=[],
            # blocked_users=[],
            # last_active=datetime.datetime.now(),
            # language_prefer='English',
            # created_at=datetime.datetime.now()
        )

        # Set the password
        user_profile.set_password(request.data.get('password'))
        # Save the user profile to the database
        user_profile.save()
        return Response({
            'message': 'User created successfully',
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user_profile = UserProfile.objects.get(username=username)
            if user_profile.verify_password(password):
                # request.session['user_id'] = str(user_profile.id)
                return Response({
                    'success': True,
                    'message': 'Login successful',
                    'user_id': str(user_profile.id)
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': 'Invalid password'
                }, status=status.HTTP_401_UNAUTHORIZED)
        except UserProfile.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
>>>>>>> ab69b4de2628a2186cfeed78759cbf9b2b373c51
