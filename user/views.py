from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from .forms import UserForm


# Create your views here.
@api_view(["GET"])
def get_user(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many = True)
    return Response(serializer.data)

@api_view(["POST"])
def create_user(request):
    body = request.data
    serializer = UserSerializer(data=body)
    if serializer.is_valid():
        serializer.save() # INSERT 
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
def update_user(request, pk) :
    body = request.data
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserSerializer(user, data=body)
    if serializer.is_valid():
        serializer.save() # UPDATE
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

def create_user_template(request):
    # check if request from submit form
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully") # messages = []
            return redirect("create_user_template")
            
    # GET
    return render(request, "user/create-user.html")

def search_user_template(request):
    username = request.GET.get("username")
    if username == None or username == "":
        users = User.objects.all()
    else:
        users = User.objects.filter(username__contains=username)
        
    return render(request, "user/search-user.html", {"users": users} )

def delete_user_template(request):
    pk = request.GET.get("id")
    try:
        users = User.objects.get(pk=pk)
        users.delete()
        messages.success(request, "User deleted successfully")
        
    except User.DoesNotExist:
        print(f"User id:{pk} does not exist")
        messages.error(request,"User cannot be deleted because this user does not exist")
        
    return redirect("search_user")

def update_user_template(request):
    pk = request.GET.get("id")
    old_user = get_object_or_404(User, id=pk)
    if request.method == "POST":
        form = UserForm(request.POST, instance=old_user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully") # messages = []
            return redirect("search_user")
        else:
            messages.error(request, "User the input information was not complete") # messages = []
            return redirect("search_user")
        
    #GET
    return render(request, "user/update-user.html", {"user": old_user})
    