from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from .models import Staff,Users,post,files,liked,disliked
from . import models
from  django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import os
from django.http import JsonResponse
from django.contrib.auth import get_user_model

# Create your views here.
def login(request):
    return render(request,'login.html')
def signup(request):
    
    return render(request, 'signup.html')



@login_required(login_url='login')
def home(request):
    ids=request.user.id
    filt=Users.objects.get(id=ids)
    
    return render(request, 'home.html',{'filt':filt})

@login_required(login_url='login')
def home_user(request):
    ids=request.user.id
    filt=Users.objects.get(id=ids)
    return render(request,'home__user.html',{'filt':filt})

def usercreate(request):
    if request.method=="POST":
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        username=request.POST['username']
        password=request.POST['password']
        cpass=request.POST['cpassword']
        email=request.POST['email']
        role=request.POST['role']
        
        if request.FILES.get('file') is not None:
            image=request.FILES.get('file')
        else:
            image = "static/image/icon.png"
       
        if role=="Staff":
         
            if password==cpass:
                if Staff.objects.filter(username=username).exists():
                    messages.info(request, 'This Username Is Already Exists!!!!!')
                    return redirect('signup')
                else:
                    user=Staff.objects.create_user(
                        first_name=fname,
                        last_name=lname,
                        username=username,
                        password=password,
                        email=email,
                        image=image,
                    )
                    user.save()
            else:
                messages.info(request, 'Password doesnot match!!!!!')
                return redirect('signup')
        else:
            if password==cpass:
                if Users.objects.filter(username=username).exists():
                    messages.info(request, 'This Username Is Already Exists!!!!!')
                    return redirect('signup')
                else:
                    user=Users.objects.create_user(
                        first_name=fname,
                        last_name=lname,
                        username=username,
                        password=password,
                        email=email,
                        image=image,
                    )
                    user.save()
            else:
                messages.info(request, 'Password doesnot match!!!!!')
                return redirect('signup')

        return redirect('login')
    else:
        return redirect('signup')


def adminlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        
        user = authenticate(username=username,password=password)
        
        if user is not None:
            if user.is_active:
                auth.login(request,user) 
                if Users.objects.filter(username=username,role="USERS").exists():
                    return redirect('home_user')
                else:
                    return redirect('home')
        else:
            messages.info(request, 'invalid username and password, try again')
            return redirect('login')
    else:
        return redirect('login')

@login_required(login_url='login')
def user_management(request):
    ids=request.user.id
    role=request.user.role
    
    if role=="USER":
    
        filt=Users.objects.get(id=ids)
    else:
        filt=Staff.objects.get(id=ids)
    dats=Users.objects.filter(role="USERS")


    
    file="/static/image/icon.png"
    stf="STAFF"
    adm="ADMIN"
  
    return render(request, 'usermanagement.html',{'filt':filt,"stf":stf,"adm":adm,"dats":dats,"file":file})

@login_required(login_url='login')
def profile_user(request):
    ids=request.user.id
    role=request.user.role
    
    if role=="USER":
    
        filt=Users.objects.get(id=ids)
    else:
        filt=Staff.objects.get(id=ids)
    dats=Users.objects.filter(role="USERS")


    
    file="/static/image/icon.png"
    stf="STAFF"
    adm="ADMIN"
  
    return render(request, 'profile_user.html',{'filt':filt,"stf":stf,"adm":adm,"dats":dats,"file":file})
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def editpro(request,pk):
    
    if request.method=='POST':
       
        role=request.user.role
      
        if role=="STAFF":
            stf = Staff.objects.get(id=request.user.id)
            fname=request.POST['first_name']
            lname=request.POST['last_name']
            username=request.POST['username']
            password=request.POST['password']
            cpass=request.POST['cpassword']
            email=request.POST['email']
            if password==cpass:
                if password=="":
                    created = Staff.objects.filter(id=request.user.id).update(first_name=fname,last_name=lname,username=username,email=email)
                    return redirect('user_management')
                else: 
                    created = Staff.objects.filter(id=request.user.id).update(first_name=fname,last_name=lname,username=username,email=email,password=password)
                    redirect('login')

            else:
                messages.info(request,f"Check Entered Password And Confirm Password")
        else:
            
            stf = Users.objects.get(id=request.user.id)
            
            fname=request.POST.get('first_name')
            lname=request.POST.get('last_name')
            username=request.POST.get('username')
            password=request.POST.get('password')
            cpass=request.POST.get('cpassword')
            email=request.POST.get('email')
           
            if password==cpass:
                if password=="":
                  
                    created = Users.objects.filter(id=request.user.id).update(first_name=fname,last_name=lname,username=username,email=email)
                    
                    return redirect('profile_user')
                else:
                    
                    created = Users.objects.filter(id=request.user.id).update(last_name=lname,username=username,email=email)
                    u = Users.objects.get(id=request.user.id)
                    u.set_password(password)
                    u.save() 
                    return redirect('login')
            else:
                messages.info(request,f"Check Entered Password And Confirm Password")
                return redirect('profile_user')

        
    return redirect('user_management')




@login_required(login_url='login')
def up_pro(request,id):
    if request.method=="POST":
       
        User = get_user_model()
        pro = User.objects.get(id=id)
        if request.FILES.get('file') is not None:
            image=request.FILES['file']
        else:
            image = "static/image/icon.png"
        # created = User.objects.filter(id=request.user.id).update(image=image)
        os.remove(pro.image.path)
        pro.image=image
        pro.save()
        # created = User.objects.filter(id=id).update(image=image)

        return redirect('user_management')
    else:
        return redirect('user_management')
@login_required(login_url='login')
def feeds(request):
    ids=request.user.id
    filt=Staff.objects.get(id=ids)
    feed=post.objects.filter(user=ids)
    lk = liked.objects.all()
    dk = disliked.objects.all()
    fil=files.objects.filter(user=ids)

    context={
        "filt":filt,
        "feed":feed,
        "files":fil,
        "lk":lk,
        "dk":dk
    }
    return render(request,"feeds.html",context)
@login_required(login_url='login')
def view_like(request,id):
    ids=request.user.id
    filt=Staff.objects.get(id=ids)
    feed=post.objects.get(id=id)
    lk = liked.objects.filter(post=id)
    dk = disliked.objects.filter(post=id)
    fil=files.objects.filter(post=id)

    context={
        "filt":filt,
        "feed":feed,
        "files":fil,
        "lk":lk,
        "dk":dk
    }
    return render(request,"view_like.html",context)
@login_required(login_url='login')
def feeds_user(request):
    ids=request.user.id
    filt=Staff.objects.get(id=ids)
    feed=post.objects.all()
    lk = liked.objects.filter(user=ids)
    dk = disliked.objects.filter(user=ids)
    fil=files.objects.all()
    

    context={
        "filt":filt,
        "feed":feed,
        "files":fil,
        "lk":lk,
        "dk":dk 


    }
    return render(request,"feeds_user.html",context)
@login_required(login_url='login')
def add_lk(request):
    ele = request.GET.get('lks')
    lks = post.objects.get(id=ele)
    ids=request.user.id
    use = Users.objects.get(id=ids)
    lks.like=lks.like+1
    lks.save()
   

    lhj = liked()
    lhj.post=lks
    lhj.user=use
    lhj.name=use.first_name+" "+use.last_name
    lhj.save()


    return JsonResponse({"status":" not"})
@login_required(login_url='login')
def add_dlk(request):
    ele = request.GET.get('lks')
    lks = post.objects.get(id=ele)
    ids=request.user.id
    use = Users.objects.get(id=ids)
    lks.dislike=lks.dislike+1
    lks.save()

    lhj = disliked()
    lhj.post=lks
    lhj.user=use
    lhj.name=use.first_name+" "+use.last_name
    lhj.save()


    return JsonResponse({"status":" not"})

@login_required(login_url='login')
def create_post(request):
    filt=Users.objects.filter(role="USERS")
    context={
        "filt":filt
    }
    return render(request,'create_post.html',context)
@login_required(login_url='login')
def create_posts(request):
    ids=request.user.id
    idr=Staff.objects.get(id=ids)
    posts=post()
    posts.description=request.POST.get('des', None)
    posts.tag=request.POST.get('tag', None)
    posts.user=idr
    
    posts.save()
    
    file = request.FILES.getlist('file[]')

    mappeds = zip(file)
    mappeds=list(mappeds)
    for ele in mappeds:
    
        created = files.objects.get_or_create(profile_pic=ele[0],user=idr,post=posts)
    return redirect('feeds')