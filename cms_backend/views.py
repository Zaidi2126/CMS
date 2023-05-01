from django.shortcuts import render
from PIL import Image
import uuid
from django.conf import settings
from rest_framework import status
import os
from .serializer import TicketSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ticket,key_generator
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListAPIView
from django.contrib.auth.models import User
import jwt,datetime
from rest_framework.filters import SearchFilter
from cryptography.fernet import Fernet
# Generate a key for encryption

key = b'8Mw-0li32paztSekJtI9E9Pc55RmKH0sNi4QmryW8-4='
# print(type(key))

import json
import urllib

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages


class Register_ticket_View(APIView):
    def post(self, request):
        print('================================')
        print(request.data)
        print('================================')

        # Get data from the request
        name = request.data.get('names', '')
        phone_no = request.data.get('phone', '')
        address = request.data.get('address', '')
        email = request.data.get('email', '')
        description = request.data.get('description', '')
        notes = request.data.get('notes', '')

        # Encrypt phone number and email
        f = Fernet(key)
        encrypted_phone_no = f.encrypt(phone_no.encode())
        encrypted_email = f.encrypt(email.encode())

        # Check if an image is present in the request data
        image_file = request.FILES.get('img', None)
        if image_file:
            # Open the image and convert the color mode to RGB
            img = Image.open(image_file)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            # Resize the image to a maximum width of 800 pixels
            width = 800
            height = int((width / float(img.size[0])) * float(img.size[1]))
            img = img.resize((width, height), Image.ANTIALIAS)
            image_path = os.path.join(settings.MEDIA_ROOT, 'tickets', str(uuid.uuid4()) + '.jpg')
            img.save(image_path)
        else:
            image_path = ''

        new_recd = ticket(
            name=name,
            phone_no=encrypted_phone_no.decode(),
            address=address,
            email=encrypted_email.decode(),
            description=description,
            notes=notes,
            automatic_generated_ticket_number=key_generator(),
            img=image_path
        )
        new_recd.save()

        return Response({
            'asd': 'asd'
        })



class get_tickets(ListAPIView):
    queryset = ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'email', 'automatic_generated_ticket_number']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Decrypt phone number and email for each ticket object
        f = Fernet(key)
        for ticket_obj in queryset:
            ticket_obj.phone_no = f.decrypt(ticket_obj.phone_no.encode()).decode()
            ticket_obj.email = f.decrypt(ticket_obj.email.encode()).decode()
        return queryset



class sign_in (APIView):
   
    def post(self,request):  
        username=request.data['username']
        password=request.data['password']
        print(request.data['password'])
        if User.objects.filter(username=username).first()==None:
            raise AuthenticationFailed('Wrong username')
        if not User.objects.filter(username=username).first().check_password(password):
            raise AuthenticationFailed('Wrong password')
        superuser=User.objects.filter(username=username).first()
       

        payload={
            'username':superuser.username,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=5),
            'iat':datetime.datetime.utcnow()

        }

        token=jwt.encode(payload,'secret',algorithm='HS256')
        response=Response() 
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data={
            'jwt':token,
            'username':superuser.username
        }
        return response


class FetchRecord(ListAPIView):
    queryset = ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [SearchFilter]
    search_fields = ['automatic_generated_ticket_number']
    def get_queryset(self):
        queryset = super().get_queryset()
        temp=queryset
        # Decrypt phone number and email for each ticket object
        f = Fernet(key)
        for ticket_obj in queryset:
            ticket_obj.phone_no = f.decrypt(ticket_obj.phone_no.encode()).decode()
            ticket_obj.email = f.decrypt(ticket_obj.email.encode()).decode()
    
        
        return queryset





class verify_token(APIView):
    def post(self,request):
    #    JWT AUTHERNTICATION
        token=request.COOKIES.get('jwt')
        print(token)
        if not token:
            raise AuthenticationFailed('NOT AUTHENTICATED')
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('NOT AUTHENTICATED')
        return Response({'Sucess'})
    




class UpdateInfoView(APIView):
    def post(self,request):
        f = Fernet(key)
        tickets=request.data['automatic_generated_ticket_number']
        user=ticket.objects.filter(automatic_generated_ticket_number=tickets).first()
        serializer=TicketSerializer(user, data=request.data)      
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Delete_ticket(APIView):
    def post(self,request):

        invoice=request.data['automatic_generated_ticket_number']
        user=ticket.objects.filter(automatic_generated_ticket_number=invoice).delete()
        return Response({'':''})
        
        


class LogoutView(APIView):
    def post(self,request):
        response=Response()
        response.delete_cookie('jwt')
        response.data={
            'message': 'success'
        }
        return response