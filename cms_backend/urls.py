from django.urls import path
from .views import LogoutView,verify_token,FetchRecord,Register_ticket_View,get_tickets,sign_in,UpdateInfoView,Delete_ticket

urlpatterns = [
    path('register_ticket/',Register_ticket_View.as_view()),
    path('update_info/',UpdateInfoView.as_view()),
    path('get_tickets/',get_tickets.as_view()),
    path('FetchRecord/',FetchRecord.as_view()),
    path('delete_ticket/',Delete_ticket.as_view()),
    path('sign_in/',sign_in.as_view()),
    path('verify_token/',verify_token.as_view()),
    path('logout/',LogoutView.as_view()),

]