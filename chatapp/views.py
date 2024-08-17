from django.shortcuts import render
from .models import ChatMessage
def index(request):
    return render(request, 'chatapp/index.html', {})

def chat_room(request, room_name):
    username = request.user.username
    messages = ChatMessage.objects.filter(room=room_name)
    users = ChatMessage.objects.filter(room=room_name).values('user').distinct()    
    if username:
        return render(request, 'chatapp/room.html', {
        'room_name': room_name,
        'username':username,
        'messages':messages,
        'users':users
    })
    else:
        return render(request, 'chatapp/room.html', {
        'room_name': room_name,
        'username':"Unknown"
    })  


def video_chat(request, room_name):
    username = request.user.username
    messages = ChatMessage.objects.filter(room=room_name)
    users = ChatMessage.objects.filter(room=room_name).values('user').distinct() 
    if username:
        return render(request, 'chatapp/videocall.html', {
        'room_name': room_name,
        'username':username,
        'messages':messages,
        'users':users
    })
    else:
        return render(request, 'chatapp/videocall.html', {
        'room_name': room_name,
        'username':"Unknown"
    }) 
    