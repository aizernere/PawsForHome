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
def view_conversation(request, receiver_id=None):
    conversation_partners = Account.objects.filter(
        id__in=set(
            Message.objects.filter(sender=request.user).values_list('receiver_id', flat=True)
            .union(Message.objects.filter(receiver=request.user).values_list('sender_id', flat=True))
        )
    )
    
    receiver = Account.objects.get(id=receiver_id) if receiver_id else None
    messages = Message.objects.filter(
        (models.Q(sender=request.user) & models.Q(receiver=receiver)) |
        (models.Q(sender=receiver) & models.Q(receiver=request.user))
    ).order_by('timestamp') if receiver else []
    
    if request.method == 'POST' and receiver:
        content = request.POST.get('content')
        Message.objects.create(sender=request.user, receiver=receiver, content=content)
        return redirect('view_conversation', receiver_id=receiver.id)

    return render(request, 'navbar/message.html', {
        'conversation_partners': conversation_partners,
        'receiver': receiver,
        'messages': messages
    })


@login_required
def conversations_list(request):
    sent_messages = Message.objects.filter(sender=request.user).values_list('receiver_id', flat=True)
    received_messages = Message.objects.filter(receiver=request.user).values_list('sender_id', flat=True)
    
    conversation_ids = set(sent_messages).union(set(received_messages))
    conversation_partners = Account.objects.filter(id__in=conversation_ids)
    
    return render(request, 'navbar/message.html', {'conversation_partners': conversation_partners})
    #return redirect(request, 'main:message', {'conversation_partners': conversation_partners})

#For demonstration only
def list_accounts(request):
    accounts = Account.objects.all()
    return render(request, 'pmessages/account_list.html', {'accounts': accounts})
