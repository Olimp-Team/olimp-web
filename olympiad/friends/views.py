from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic.base import View
from friendship.exceptions import AlreadyExistsError
from friendship.models import Friend, FriendshipRequest
from users.models import User
from django.contrib import messages
from django.core.files.base import ContentFile
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.forms import UserProfileForm


@login_required
def add_friend(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    existing_request = FriendshipRequest.objects.filter(from_user=request.user, to_user=other_user).first()

    if existing_request:
        # Обработать случай, когда запрос уже существует
        messages.warning(request, 'Вы уже отправили запрос на добавление в друзья этому пользователю.')
        return redirect('users:profile', user_id=user_id)

    try:
        Friend.objects.add_friend(
            request.user,  # Отправитель запроса
            other_user,  # Получатель запроса
            message='Привет! Давай дружить!'
        )
        messages.success(request, 'Запрос на добавление в друзья отправлен.')
    except AlreadyExistsError:
        messages.warning(request, 'Вы уже отправили запрос на добавление в друзья этому пользователю.')

    return redirect('users:profile', user_id=user_id)


@login_required
def accept_friend_request(request, request_id):
    """Принятие запроса на добавление в друзья"""
    friend_request = FriendshipRequest.objects.get(id=request_id)
    friend_request.accept()
    return redirect('friends:view_friend_requests')


@login_required
def reject_friend_request(request, request_id):
    """Отклонение запроса на добавление в друзья"""
    friend_request = FriendshipRequest.objects.get(id=request_id)
    friend_request.reject()
    return redirect('friends:friend_requests')


@login_required
def view_friends(request):
    """Просмотр списка друзей"""
    friends = Friend.objects.friends(request.user)
    context = {'friends': friends}
    return render(request, 'friends_list.html', context)


@login_required
def view_friend_requests(request):
    """Просмотр списка входящих запросов в друзья"""
    friend_requests = FriendshipRequest.objects.filter(to_user=request.user)
    context = {'friend_requests': friend_requests}
    return render(request, 'friend_requests.html', context)


@login_required
def search_friends(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query).exclude(id=request.user.id)
    friends = Friend.objects.friends(request.user)
    pending_requests = Friend.objects.unrejected_requests(user=request.user)
    friend_requests = [req.to_user for req in pending_requests]
    context = {
        'users': users,
        'friends': friends,
        'friend_requests': friend_requests,
        'query': query,
    }
    return render(request, 'search_friends.html', context)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = UserProfileForm(instance=user) if request.user == user else None
        context = {'form': form, 'user': user, 'is_owner': request.user == user}
        return render(request, 'profile.html', context)

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user != user:
            return redirect(reverse('profile', kwargs={'user_id': user.id}))

        form = UserProfileForm(instance=user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('users:profile', kwargs={'user_id': user.id}))
        context = {'form': form, 'user': user, 'is_owner': True}
        return render(request, 'profile.html', context)


@csrf_exempt
def save_cropped_image(request):
    if request.method == 'POST' and request.user.is_authenticated:
        image_data = request.POST.get('image')
        if image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{request.user.username}_avatar.{ext}')

            user = get_object_or_404(User, id=request.user.id)
            user.image.save(data.name, data)
            user.save()

            return JsonResponse({'status': 'success', 'url': user.image.url})
        else:
            return JsonResponse({'status': 'error', 'message': 'No image data found.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
