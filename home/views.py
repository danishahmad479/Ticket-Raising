from django.shortcuts import render , HttpResponse , redirect , get_object_or_404
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from home.forms import *
from django.contrib.auth.hashers import make_password
from home.models import Ticket , SendTicketTo, Department
from home.forms import TicketForm  , send_ticket
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages



# Create your views here.

def index(request):
    return render(request,'base.html')

# original working

@login_required
def ticket_raise(request):
    ticketform = CustomTicketForm()
    if request.method == "POST":
        if request.user.is_superuser:
            print(request.POST.get('approve_button'))
            ticket_id = request.POST.get('approve_button')
            ticket = Ticket.objects.get(id=ticket_id)
            is_approved = request.POST.get('is_approved_' + ticket_id) == 'on'
            ticket.isapproved = is_approved
            ticket.save()
            return redirect(f'send_ticket_to/{ticket_id}')
        else:
            ticketform = CustomTicketForm(request.POST)
            if ticketform.is_valid():
                ticket = ticketform.save(commit=False)
                ticket.username = request.user
                ticket.save()
                return redirect('dashboard')
            else:
                ticketform = CustomTicketForm()
    return render(request, "ticket.html", {'form': ticketform})

@login_required
def dashboard(request):
    if request.user.is_superuser:
        tickets = Ticket.objects.filter(assignedto_id=request.user.department.id)
    else:
        tickets = Ticket.objects.filter(username=request.user,assignedto_id=request.user.department.id)
    return render(request , "dashboard.html" , {'tickets' : tickets})

def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'updateticket.html', {'form': form, 'ticket': ticket})

@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    ticket.delete()
    return redirect('dashboard')  


def login_user(request):

    if request.method =="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        remember_me = request.POST.get("remember_me")
        user = authenticate(request, username=username, password = password)
        if user is not None:
                login(request, user)
                return redirect('dashboard')
        else:
            # User login failed, add a message to the request
            messages.warning(request, "Invalid username or password. Please register if you don't have an account.")
            return redirect('login')
   
    else:
        return render(request , 'authentication/login.html' , {})

# def login_user(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         remember_me = request.POST.get('remember_me')  # Get the value of the "Remember Me" checkbox

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('dashboard')  
#         else:
#             messages.warning(request, 'Invalid username or password.')

#     return render(request, 'authentication/login.html')



def logout_view(request):
    logout(request)
    return redirect('login')



def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()# Save the form data to the databas
            return redirect('login')  
    else:
        form = CustomUserForm()
    
    return render(request, 'register.html', {'form': form})

@login_required
def send_ticket_to(request , ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    
    if request.method == "POST":
        form = send_ticket(ticket_id, request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.assigned_by = request.user
            print(ticket.assigned_by)
            ticket.save() 
            return HttpResponse('Ticket has been sent')
    else:
        form = send_ticket(ticket_id)
        
    return render(request, "send_ticket_to_form.html", {'form': form, 'ticket': ticket })


@login_required
def view_ticket(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    return render(request, 'view_ticket.html', {'ticket': ticket})





# original
# def send_ticket_to(request):
#     if request.method == "POST":
#         form = send_ticket(request.user.department.id,request.POST)
#         if form.is_valid():
#             ticket = form.save(commit=False)
#             ticket.assigned_by = request.user
#             print(ticket.assigned_by)
#             ticket.save() 
#             return HttpResponse('Ticket has beed sent')
#     else:
#         form = send_ticket(request.user.department.id)
        
#     user_email = request.user
#     user_dept = CustomUser.objects.get(email=user_email)
#     user_department_id = user_dept.department.id
#     tickets_with_same_department = SendTicketTo.objects.filter(assigned_to__department_id=user_department_id).values('ticket__title', 'ticket__description', 'assigned_to__department__department')
#     print(tickets_with_same_department)
#     return render(request, "send_ticket_to_form.html", {'form': form , tickets_with_same_department:'tickets_with_same_department'})
