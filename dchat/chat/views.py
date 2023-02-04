from django.shortcuts import render,redirect
from chat.models import Room,Message
from django.http import HttpResponse,JsonResponse

def home(request):
    return render(request,'home.html',{})

def room(request,room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })


def checkview(request):
    username= request.POST['username']
    room_name= request.POST['room_name']
    if Room.objects.filter(name=room_name).exists():
        return redirect('/'+room_name+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room_name)
        new_room.save()
        return redirect('/'+room_name+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})