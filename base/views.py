from uuid import UUID
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, CreateUserForm

# Create your views here.


def login_page(request: HttpRequest):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
        messages.error(request, "Incorrect Username or password")

    form = AuthenticationForm()
    context: dict[str, object] = {"form": form, "page": page}

    return render(request, "base/login_register.html", context)


def register_page(request: HttpRequest):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration")
    form = CreateUserForm()
    context = {"form": form}
    return render(request, "base/login_register.html", context)


def logout_view(request: HttpRequest):
    logout(request)
    return redirect("home")


@login_required(login_url="login")
def edit_user(request: HttpRequest):
    user = User(request.user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile", user.username)
    form = UserForm(instance=user)
    context = {"form": form}
    return render(request, "base/edit_user.html", context)


def index(request: HttpRequest):
    q = request.GET.get("q", "")

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )

    topics = Topic.objects.all()[:3]
    room_count = rooms.count()
    room_activity = Message.objects.filter(Q(room__topic__name__icontains=q))[:5]

    context: dict[str, object] = {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count,
        "room_activity": room_activity,
    }

    return render(request, "base/home.html", context)


def room(request: HttpRequest, id: UUID):
    room = Room.objects.get(id=id)
    room_messages = room.message_set.all().order_by("created")
    participants = room.participants.all()

    if request.method == "POST":
        Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("room", id=room.id)

    context: dict[str, object] = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "base/room.html", context)


def user_profile(request: HttpRequest, id: UUID):
    user = User.objects.get(id=id)
    rooms = user.room_set.all()
    room_activity = user.message_set.all()
    topics = Topic.objects.all()
    context: dict[str, object] = {
        "user": user,
        "rooms": rooms,
        "room_activity": room_activity,
        "topics": topics,
    }
    return render(request, "base/profile.html", context)


@login_required(login_url="login")
def create_room(request: HttpRequest):
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, _ = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )
        return redirect("home")

    form = RoomForm()
    topics = Topic.objects.all()
    context: dict[str, object] = {"form": form, "topics": topics}
    return render(request, "base/create_room.html", context)


@login_required(login_url="login")
def update_room(request: HttpRequest, id: UUID):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("Not allowed")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, _ = Topic.objects.get_or_create(name=topic_name)
        room.name = str(request.POST.get("name"))
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        return redirect("home")
    context: dict[str, object] = {"form": form, "topics": topics, "room": room}
    return render(request, "base/create_room.html", context)


@login_required(login_url="login")
def delete_room(request: HttpRequest, id: UUID):
    room = Room.objects.get(id=id)
    if request.user != room.host:
        return HttpResponse("Not allowed")
    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"object": room})


@login_required(login_url="/login")
def delete_message(request: HttpRequest, id: UUID):
    message = Message.objects.get(id=id)
    if request.user != message.user:
        return HttpResponse("Not allowed")
    if request.method == "POST":
        message.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"object": message})


def browse_topics(request: HttpRequest):
    q = request.GET.get("q", "")
    topics = Topic.objects.filter(name__icontains=q)
    context = {"topics": topics}
    return render(request, "base/topics.html", context)


def browse_activity(request: HttpRequest):
    activity = Message.objects.filter()
    context = {"activity": activity}

    return render(request, "base/activity.html", context)
