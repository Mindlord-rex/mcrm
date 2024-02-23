from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record



# Create your views here.
def home(request):
    records = Record.objects.all()
    
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username= username, password= password)
        if user is not None:
            login(request,user)
            messages.success(request, "You Have Been Logged In")
            return redirect('home')
        else:
            messages.error(request, "There was an error logging In")
            return redirect('home')
        
    return render(request, "manager/home.html", {"records":records})

    

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out")
    return redirect('home')



def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered ")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, "manager/register.html", {'form':form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        
        customer_record = Record.objects.get(id=pk)
        return render(request, "manager/record.html", {"customer_record":customer_record})
    else:
        messages.error(request, "You must be logged in to view this page")
        return redirect('home')
    

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully.")
        return redirect('home')
    else:
        messages.success(request, "You have to be Logged in.")
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
                
        return render(request, "manager/add_record.html", {'form':form})
    else:
        messages.error(request, "You must be logged in to view this page")
        return redirect('home')
    

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has been Updated!")
            return redirect('home')
        return render(request, 'manager/update_record.html',{'form': form})
    else:
        messages.error(request, "You must be logged in to view this page")
        return redirect('home')