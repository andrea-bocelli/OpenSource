from django.db import transaction
from django.contrib.auth import login, logout, authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer

# Create your views here.
class SignupView(APIView):
    @transaction.atomic 
    def post(self, request):
        serializer = UserSerializer(date=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Signup successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    @transaction.atomic
    def post(self, request):
        if request.user.is_authenticated:
            return Response({"error":"User is already logged-in"}, status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'POST':
            username = request.data.get("username")
            password = request.data.get("password")

            user = authenticate(username=username, password=password)
        if not user:
                return Response({"error":"error!"}, status=status.HTTP_400_BAD_REQUEST)
        login(request=request, user=user)

        return Response({"message":"login successful"}, status=status.HTTP_200_OK)
    
    
class LogoutView(APIView):
    @transaction.atomic
    def post(self, request):
        logout(request=request)
        return Response({"message":"logout successful"}, status=status.HTTP_200_OK)
