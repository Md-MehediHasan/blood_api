from rest_framework import serializers
from .models import Donar,User,Organization


class DonarSerializer(serializers.ModelSerializer):
    is_capable=serializers.BooleanField(read_only=True)
    class Meta:
        model=Donar
        fields=['name','district','upazila','is_capable','last_donate','district','phone_number','group']
class DonarRegistrationSerializer(serializers.Serializer):
    name=serializers.CharField()
    contact_number=serializers.CharField()
class TokenSerializer(serializers.Serializer):
    contact=serializers.IntegerField()
    password=serializers.CharField()
    model=User
    fields=['contact','password']

class AuthenticatedUserSerializer(serializers.ModelSerializer):
    donar_info=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=['name','email','contact','donar_info']
    def get_donar_info(self,obj):
        donar=Donar.objects.filter(user=obj).first()
        return DonarSerializer(donar).data
    
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Organization
        fields='__all__'

       