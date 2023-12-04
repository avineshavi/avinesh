from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.core.files.base import ContentFile

from rest_framework import generics, permissions, status
from rest_framework.response import Response 
from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer, UserLoginSerializer, ShortenedURLSerializer, ShortenedURLEditSerializer
from .models import ShortenedURL
import qrcode

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    

class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exeception = True)
        user = authenticate(
            
            request,
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token':token.key},status=status.HTTP_200_OK)
        
        else:
            return Response({'details':'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            

class ShortenedURLCreateView(generics.CreateAPIView):
    serializer_class = ShortenedURLSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        
        qr = qrcode.QRCode(
            version =1,
            error_correction = qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(instance.original_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black",back_color="white")
        img_bytes = ContentFile()
        img.save(img_bytes, format="PNG")
        instance.qr_code.save(f'qr_code_{instance.shortened_code}.png',img_bytes,save=True)
        
class ShortenedURLDetailView(generics.RetrieveAPIView):
    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLSerializer
    lookup_field = 'shortened_code'
    

class ShortenedURLListView(generics.ListAPIView):
    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLSerializer


class ShortenedURLEditView(generics.UpdateAPIView):
    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLEditSerializer
    permission_classes = [permissions.IsAuthenticated]


class ShortenedURLDeleteView(generics.DestroyAPIView):
    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLSerializer
    permission_classes = [permissions.IsAuthenticated]


class ShortenedURLRedirectView(APIView):
    
    
    def get(self,request,shortened_code, *args, **kwargs):
        shortened_url = generics.get_object_or_404(ShortenedURL, shortened_code=shortened_code)
        shortened_url.visits_count += 1
        shortened_url.save()
        return redirect(shortened_url.original_url)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        request.auth.delete()
        return Response({"detail":"Logout successful"},status=status.HTTP_200_OK)