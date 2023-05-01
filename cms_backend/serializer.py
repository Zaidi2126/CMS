from rest_framework import serializers
from .models import ticket,key_generator
from rest_framework import serializers
from cryptography.fernet import Fernet

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model=ticket
        fields=['name','address','phone_no','email','description','automatic_generated_ticket_number','notes','img']
        extra_kwargs = {
            'name': {'required': True},
            'phone_no': {'required': False},
            'address': {'required': False},
            'email': {'required': False},
            'description': {'required': False},
            'notes': {'required': False},
        }
    def create(self, validated_data):
        print(validated_data['img'])
        validated_data['automatic_generated_ticket_number']=key_generator()
        instance= self.Meta.model(**validated_data)
        instance.save()
        return instance
    


