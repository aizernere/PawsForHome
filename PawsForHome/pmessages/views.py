from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth import get_user_model
from django.db import models

# Create your views here.

Account = get_user_model()

@login_required
def send_message(request, receiver_id):
    receiver = Account.objects.get(id=receiver_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(sender=request.user, receiver=receiver, content=content)
        return redirect('view_conversation', receiver_id=receiver.id)
    return render(request, 'pmessages/send_message.html', {'receiver': receiver})

@login_required
def view_conversation(request, receiver_id):
    receiver = Account.objects.get(id=receiver_id)
    messages = Message.objects.filter(
        (models.Q(sender=request.user) & models.Q(receiver=receiver)) |
        (models.Q(sender=receiver) & models.Q(receiver=request.user))
    ).order_by('timestamp')
    
    for message in messages:
        if message.receiver == request.user:
            message.read = True
            message.save()
    
    return render(request, 'pmessages/conversation.html', {'receiver': receiver, 'messages': messages})


#For demonstration only
def list_accounts(request):
    accounts = Account.objects.all()
    return render(request, 'pmessages/account_list.html', {'accounts': accounts})
