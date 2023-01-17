from django.shortcuts import render,redirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout,login

from LibraryApp.models import Books, Course, Issue_book, Student

from django.views.decorators.cache import  cache_control
from django.contrib.auth.decorators import login_required

from django.db.models import Q

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_fun(request):
    if request.method == 'POST':
        userName = request.POST['userName']
        userPassword = request.POST['userPassword']
        user = authenticate(username=userName,password=userPassword)
        if user is not None:
            if user.is_superuser:
                login(request,user)
                request.session['uid'] = request.POST['userName']
                return redirect('home')
            else:
                return render(request,'login.html',{'data':'invalid credentials'})
    else:
        return render(request,'login.html',{'data':''})

#--------------------------------------------------------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
def reg_fun(request):
    if request.method == 'POST':
        username = request.POST['txtUserName']
        password = request.POST['txtPswd']
        email = request.POST['txtEmail']
        if User.objects.filter(Q(username=username) | Q(email=email)).exists():            
                return render(request,'register.html',{'data':'invalid creddentials'})             
        else:
            u1 = User.objects.create_superuser(username=username,password=password,email=email)
            u1.save() 
            return render(request,'login.html',{'data':''})
    else:
        return render(request,'register.html',{'data':''})
    
#----------------------------------------------------------------------------------------------
@login_required
def home_fun(request):
    return render(request,'books_template/home.html') 

#------------------------------------------------------------------------------------------
@login_required
def addbook_func(request):
    if request.method == 'POST':
        c1 = Course.objects.all()
        b1 = Books()
        b1.book_name  =request.POST['txtBookName']
        b1.author_name = request.POST['txtAuthorName']
        b1.course_name = Course.objects.get(course_name = request.POST['ddlCourseName'])
        b1.save()
        return render(request,'books_template/add_book.html',{'course':c1})
    else:
        c1 = Course.objects.all()
        return render(request,'books_template/add_book.html',{'course':c1})
    
#---------------------------------------------------------------------------------------
@login_required
def displaybook_func(request):
    books = Books.objects.all()
    return render(request,'books_template/display_book.html',{'books':books})
        
#----------------------------------------------------------------------------------
@login_required
def update_book_fun(request,id):
    book = Books.objects.get(id=id)
    c1 = Course.objects.all()
    if request.method == 'POST':        
        book.book_name  =request.POST['txtBookName']
        book.author_name = request.POST['txtAuthorName']
        book.course_name = Course.objects.get(course_name = request.POST['ddlCourseName'])
        book.save()
        return redirect('displaybook')
    return render(request,'books_template/update_book.html',{'books':book,'course':c1})

#------------------------------------------------------------------------------------
@login_required
def delete_book_fun(request,id):
    book = Books.objects.get(id=id)
    book.delete()
    return redirect('displaybook')

#------------------------------------------------------------------------------------
@login_required
def add_stud_fun(request):
    c1 = Course.objects.all()
    if request.method == 'POST':
        s1 = Student()
        s1.stud_name = request.POST['txtName']
        s1.stud_course =Course.objects.get(course_name = request.POST['ddlCourse']) 
        s1.stud_phno = request.POST['txtPhno']
        s1.stud_semester = request.POST['txtSem']
        s1.save()
        return render(request,'student_template/add_student.html',{'course':c1})
    return render(request,'student_template/add_student.html',{'course':c1}) 
#--------------------------------------------------------------------------------
@login_required
def assignbook_fun(request):
    books = Books.objects.all()
    if request.method =='POST':
        i1 = Issue_book()
        i1.stud_name = Student.objects.get(stud_name=request.POST['txtName'])
        i1.book_name = Books.objects.get(book_name=request.POST['ddlBookName'])
        i1.start_date = request.POST['txtStartDate']
        i1.end_date = request.POST['txtEndDate']
        i1.save()
        return render(request,'books_template/assign_book.html',{'Book':books})
    return render(request,'books_template/assign_book.html',{'Book':books})
                
#-----------------------------------------------------------------------------------
@login_required
def display_assign_fun(request):
    i1 = Issue_book.objects.all()
    return render(request,'books_template/display_assign.html',{'issue':i1})

#-----------------------------------------------------------------------------------
@login_required
def delete_issue_fun(request,id):
    i1 = Issue_book.objects.get(id=id)
    i1.delete()
    return redirect('displayassign')

#-------------------------------------------------------------------------------------
@login_required
def updt_issue_fun(request,id):
    i1 = Issue_book.objects.get(id=id)
    s1 = Student.objects.get(id=i1.stud_name_id)
    books = Books.objects.all()
    print(i1.start_date)
    if request.method == 'POST':
        i1.stud_name = Student.objects.get(stud_name=request.POST['txtName'])
        i1.book_name = Books.objects.get(book_name=request.POST['ddlBookName'])
        i1.start_date = request.POST['txtStartDate']
        i1.end_date = request.POST['txtEndDate']
        i1.save()
        return redirect('displayassign')
    return render(request,'books_template/updt_issue.html',{'Issue':i1,'Stud':s1,'Book':books})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def log_out_fun(request):
    logout(request)    
    return redirect('log')
    