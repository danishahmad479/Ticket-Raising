from django.urls import path 
from home.views import index , register ,login_user , ticket_raise ,dashboard ,update_ticket , delete_ticket,logout_view,send_ticket_to ,view_ticket


urlpatterns = [

    path("",index),
    path('register/' , register , name="register"),
    path('login/' , login_user , name='login'),
    path("ticket/", ticket_raise , name = 'ticket'),
    path("dashboard/" , dashboard, name = 'dashboard'),
    path('view_ticket/<int:ticket_id>/',view_ticket, name='view_ticket'),
    path('update_ticket/<int:ticket_id>/',update_ticket, name='update_ticket'),
    path('delete_ticket/<int:ticket_id>/', delete_ticket, name='delete_ticket'),
    path('logout/',logout_view , name ='logout'),
    path('ticket/send_ticket_to/<int:ticket_id>/' , send_ticket_to ,name = "send_ticket_to"),

]
