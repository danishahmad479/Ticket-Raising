from django import forms
from home.models import CustomUser , Ticket ,SendTicketTo

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','email' , 'password' , 'roles' , 'department']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-controld'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(),
            'roles': forms.Select(attrs={'class': 'form-select form-select-lg mb-3'}),
            'department': forms.Select(attrs={'class': 'form-select form-select-lg mb-3'}),
        }
        

class CustomTicketForm(forms.ModelForm):
    class Meta:
        model =  Ticket
        fields = ['title', 'description' , 'assignedto','priority']

        widgets = {

            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class' :'form-control'}),
            'assignedto' : forms.Select(attrs={'class': 'form-select form-select-lg mb-3'}),
            'priority': forms.Select(attrs={'class': 'form-select form-select-lg mb-3'}),
            
        }

class SuperUserTicketForm(forms.ModelForm):
    class Meta:
        model =  Ticket
        fields = "__all__"


    def __init__(self, *args, **kwargs):
        super(SuperUserTicketForm, self).__init__(*args, **kwargs)
        if not self.instance.username.is_superuser:
            self.fields.pop('username')
            self.fields.pop('isapproved')

        if not self.instance.username.is_superuser or not self.instance.pk:
            self.fields.pop('is_approved')


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'assignedto', 'priority']

        widgets = {

            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class' :'form-control'}),
            'assignedto' : forms.Select(attrs={'class': 'form-select form-select-lg mb-3'}),
            'priority': forms.Select(attrs={'class': 'form-select form-select-lg mb-3'}),
            
        }



class send_ticket(forms.ModelForm):
    class Meta:
        model = SendTicketTo
        fields = ['assigned_to', 'ticket', 'note', 'priority', 'status']

        widgets = {

            'assigned_to': forms.Select(attrs={'class': 'form-select form-select-lg mb-3'}),
            'ticket': forms.Select(attrs={'class': 'form-select form-select-lg mb-3'}),
            'note': forms.Textarea(attrs={'class' :'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-select form-select-lg mb-3'}),
            'status': forms.Select(attrs={'class': 'form-select form-select-lg mb-3'}),
        }

    def __init__(self, ticket_id, *args, **kwargs):
        super(send_ticket, self).__init__(*args, **kwargs)
        self.fields['ticket'].queryset = Ticket.objects.filter(id=ticket_id)