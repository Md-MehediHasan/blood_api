from django.shortcuts import render
from .models import Donar,User,Organization
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .serializers import DonarSerializer,AuthenticatedUserSerializer,OrganizationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate



class GetDonar(APIView):
    def get(self,request):
        queryset=[]
        blood_group=str(request.query_params.get('blood_id'))
        district=request.query_params.get('district')
        upazila=request.query_params.get('upazila')
        if request.user.is_authenticated:
            if blood_group is not None and district is not None and upazila is not None:
                donar= Donar.objects.filter(Q(blood_group=blood_group) & Q(district=district) & Q(upazila=upazila) & ~Q(user=request.user))
                queryset.extend(donar)
            elif blood_group is not None and district is not None:
                donar= Donar.objects.filter(Q(blood_group=blood_group) & Q(district=district) & ~Q(user=request.user))
                queryset.extend(donar)
            else:
                donar= Donar.objects.filter(Q(blood_group=blood_group) & ~Q(user=request.user))
                queryset.extend(donar)
        else:
            if blood_group is not None and district is not None and upazila is not None:
                donar= Donar.objects.filter(Q(blood_group=blood_group) & Q(district=district) & Q(upazila=upazila))
                queryset.extend(donar)
            elif blood_group is not None and district is not None:
                donar= Donar.objects.filter(Q(blood_group=blood_group) & Q(district=district))
                queryset.extend(donar)
            else:
                donar= Donar.objects.filter(Q(blood_group=blood_group))
                queryset.extend(donar)
        data=DonarSerializer(queryset,many=True).data
        return Response(data,status=status.HTTP_200_OK)
    

class RegisterDonar(APIView):
   def post(self,request):
       global donar
       name=request.data['name']
       contact_number=request.data['contact_number']
       email=request.data['email']
       password=request.data['password']
       district=request.data['district']
       upazila=request.data['upazila']
       blood_id=request.data['blood_id']
       last_donate=request.data['last_donate']
       try:
        user=User.objects.create_user(name=name,email=email,contact=contact_number,password=password)
        if user:
            donar=Donar.objects.create(user=user,district=district,upazila=upazila,blood_group=blood_id,last_donate=last_donate,contact_number=contact_number,work_for='self_satisfaction')
            return Response({'msg':'Account Created Successfully'},status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':'User creation Failed'},status=status.HTTP_403_FORBIDDEN)
       except:
          return Response({'msg':'User Already Exists.Try with another phone number'},status=status.HTTP_403_FORBIDDEN)
       

# user will try to login using contact number and password
# for successful login user will be provided a token for futher in authentication in multiple view

class AuthView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        contact=request.data.pop('contact',None)
        password=request.data.pop('password',None)
        try:
         user = authenticate(contact=contact,password=password)
         token, created = Token.objects.get_or_create(user=user)
         if token:
          return Response({'token': token.key,'msg':'Login Successfull'},status=status.HTTP_201_CREATED)
        except:
            return Response({'msg':'Credential does not match to any account'},status=status.HTTP_403_FORBIDDEN)
        

# This view will return authenticated user if a valid token is provided
        
class AuthenticatedUser(APIView):
   def get(self,request):
     try:
        user=User.objects.get(contact=request.user.contact)
        data=AuthenticatedUserSerializer(user).data
        return Response(data,status=status.HTTP_200_OK)
     except:
        return Response({'msg:''Credentials not provided'},status=status.HTTP_401_UNAUTHORIZED)

# To update user info ..user must provide old and new password if old password is valid for authentication the data will be updated

class UpdateUserInfo(APIView):
   def post(self,request):
      data=request.data
      try:
        user=authenticate(contact=request.user.contact,password=request.data['old_password'])
        if data['old_password'] !=data['new_password']:
            donar=Donar.objects.get(user=user)
            user.name=data['name']
            user.contact=data['contact']
            user.email=data['email']
            user.set_password(data['new_password'])
            user.save()
            donar.district=data['district']
            donar.upazila=data['upazila']
            donar.last_donate=data['last_donate']
            donar.save()
            return Response({'msg':'Profile Updated Successfully'},status=status.HTTP_200_OK)
        else:
           return Response({'msg':'New password can not be same as previous one'},status=status.HTTP_403_FORBIDDEN)
        
      except:
         return Response({'msg':'Check your old password'},status=status.HTTP_401_UNAUTHORIZED)
      
# New Organization registrations

class RegisterOrganization(APIView):
   def post(self,request):
        user=request.user
        data=request.data
        if user.is_authenticated:
            try:
              organization=Organization.objects.get(organization_name=data['organization_name'])
              return Response({'msg':'Organization already registered'},status=status.HTTP_302_FOUND)
            except:
                organization_data={
                'organization_name':data['organization_name'],
                    'working_area':data['district'],
                    'establishing_year':data['establishing_year'],
                    'logo':data['logo']
                }
                organization=Organization.objects.create(organization_manager=user,**organization_data)
                if organization:
                  return Response({'msg':'Your organization has been saved successfully'},status=status.HTTP_201_CREATED)
                else:
                 return Response({'msg':'Something went wrong while saving'},status=status.HTTP_400_BAD_REQUEST)
        else:
          return Response({'msg':'Authentication required to save organization data'},status=status.HTTP_401_UNAUTHORIZED)
        

# All organization where autheniticated user is a manager will return from this view

class AuthenticatedUsersOrganization(APIView):
   def get(self,request):
      user=request.user
      if user.is_authenticated:
         organizations=Organization.objects.filter(organization_manager=user)
         data=OrganizationSerializer(organizations,many=True).data
         return Response(data,status=status.HTTP_200_OK)
      else:
         return Response({'msg':'Authentication Required to get organizaion belongs to you'},status=status.HTTP_401_UNAUTHORIZED)




   
   


  

