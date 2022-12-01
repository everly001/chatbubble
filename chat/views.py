from asyncio.windows_events import NULL
from django.views import View
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import UserSignUpForm, UserUpdateForm, ProfileUpdateForm, NewChatForm
from django.contrib.auth import get_user_model
from .models import Conversations, Message, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q 

User = get_user_model()

# Functions

def WhichParticipant(request, chat):
        if chat.participant_1 == request:
            return chat.participant_2
        else:
            return chat.participant_1

def GetContact(request):

    chat_list = list(Conversations.objects.filter(Q(participant_1=request) | Q(participant_2=request)))
    contacts = []
    
    for chat in chat_list:
        new_contact = WhichParticipant(request, chat)
        contacts.append(new_contact)
    
    return contacts


def GetLastMessages(request, chats):

    last_messages = []

    for contact in chats:
        last_message = Message.objects.filter(
            Q(sender=request.user) & Q(receiver=contact) | Q(sender=contact) & Q(receiver=request.user)
        ).order_by('-timestamp')[:1]

        if len(last_message) > 0:
            last_message = last_message.get()
            last_messages.append(last_message)
        else:
            last_message = ''

    return last_messages

def GetUnreadMessages(request, chats):
    unread_number = []

    for contact in chats:
        unread_messages = Message.objects.filter(sender=contact,receiver=request.user, is_unread=True)
        unread_messages_count = unread_messages.count()
        unread_number.append(unread_messages_count)

    return unread_number

# Views

def index(self, request, *args, **kwargs):
    if request.user.is_authenticated():
        return HttpResponseRedirect('app')
    return super(LoginView, self).get(request, *args, **kwargs)


def SignUpView(request):
    form = UserSignUpForm()

    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')

    context = {'form': form}
    return render(request, 'registration/signup.html', context)


class AppView(View):
    @method_decorator(login_required)
    def get(self, request, username=None):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm()
        new_chat_form = NewChatForm()
        conversation_chosen = False
        chats = GetContact(request.user)
        last_messages = GetLastMessages(request, chats)
        unread_messages = GetUnreadMessages(request, chats)
        conversations = zip(chats, last_messages, unread_messages)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'new_chat_form': new_chat_form,
            'conversations': conversations,
            'conversation_chosen': conversation_chosen,
        }

        if username is None:
            return render(request, 'chat/app.html', context)
        else:
            user_obj = User.objects.get(username=username)
            chats = GetContact(request.user)
            last_messages = GetLastMessages(request, chats)
            conversation_chosen = True

            messages = Message.objects.filter(
            Q(sender=request.user) & Q(receiver=user_obj) | Q(sender=user_obj) & Q(receiver=request.user))

            for message in messages:
                if message.receiver == request.user and message.is_unread == True:
                    message.is_unread = False
                    message.save()

            unread_messages = GetUnreadMessages(request, chats)
            conversations = zip(chats, last_messages, unread_messages)

            media_messages = Message.objects.filter(
                Q(sender=request.user) & Q(receiver=user_obj) | Q(sender=user_obj) & Q(receiver=request.user)
            ).exclude(media='')

            if request.user.id > user_obj.id:
                thread_name = f'chat_{request.user.id}-{user_obj.id}'
            else:
                thread_name = f'chat_{user_obj.id}-{request.user.id}'

            message_objs = Conversations.objects.filter(thread_name=thread_name)

            context.update(dict(user=user_obj, messages=messages, media_messages=media_messages, message_objs=message_objs, conversation_chosen=conversation_chosen))
            return render(request, 'chat/chat.html', context)

    def post(self, request, username):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile or None)
        new_chat_form = NewChatForm(request.POST)

        if new_chat_form.is_valid():
            conversation = new_chat_form.save(False)
            participant_1 = request.user
            participant_2 = new_chat_form.cleaned_data['participant_2']

            try:
                participant_2 = User.objects.get(username=participant_2)
            except User.DoesNotExist:
                error = 'User not found!'
                sub_error = 'No user exists with this username, please check the username and try again.'
                return Error(request, error, sub_error)

            conversation.participant_1 = participant_1
            conversation.participant_2 = participant_2
            thread_name = ''

            if request.user.id > participant_2.id:
                thread_name = f'chat_{request.user.id}-{participant_2.id}'
            else:
                thread_name = f'chat_{participant_2.id}-{request.user.id}'

            conversation.thread_name = thread_name
            
            try:
                if Conversations.objects.get(thread_name=thread_name):
                    return redirect(f'/{participant_2}')
            except Conversations.DoesNotExist:
                conversation.save()
                return redirect(f'/{participant_2}')
                
        if user_form.is_valid():
            user_form.save()

        if profile_form.is_valid():
            profile_form.save()

            return redirect('app')
        

def Error(request, error, sub_error):
    context = {
        'error_message': error,
        'sub_error': sub_error,
    }
    return render(request, 'chat/error.html', context)