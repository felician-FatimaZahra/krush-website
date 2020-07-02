from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import Friend, Profile

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'users/view_profile.html', args)

def friends(request):
    users = Profile.objects.exclude(user=request.user)
    context = {
        'users': users
    }
    for user in users:
        print("here")
        print(user.user)
    return render(request, "users/friends.html", context)

def send_friend_request(request, id):
    if request.user.is_authenticated():
        user = get_object_or_404(User, id=id)
        frequest, created = Friend.objects.get_or_create(
            from_user=request.user,
            to_user=user)
        return HttpResponseRedirect('/friends')

def cancel_friend_request(request, id):
    if request.user.is_authenticated():
        user = get_object_or_404(User, id=id)
        frequest = Friend.objects.filter(
            from_user=request.user,
            to_user=user).first()
        frequest.delete()
        return HttpResponseRedirect('/friends')

def accept_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = Friend.objects.filter(from_user=from_user, to_user=request.user).first()
    user1 = frequest.to_user
    user2 = from_user
    user1.profile.friends.add(user2.profile)
    user2.profile.friends.add(user1.profile)
    frequest.delete()
    return HttpResponseRedirect('/{}'.format(request.user.profile.slug))

def delete_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = Friend.objects.filter(from_user=from_user, to_user=request.user).first()
    frequest.delete()
    return HttpResponseRedirect('/{}'.format(request.user.profile.pk))

def profile_view(request, slug):
    user = User.objects.filter(pk=slug).first()
    profile = Profile.objects.filter(user=user).first()
    sent_friend_requests = Friend.objects.filter(from_user=user)
    rec_friend_requests = Friend.objects.filter(to_user=user)

    # friends = profile.friends.all()

    # is this user our friend
    button_status = 'none'
    if user not in request.user.profile.friends.all():
        button_status = 'not_friend'

        # if we have sent him a friend request
        if len(Friend.objects.filter(
            from_user=request.user).filter(to_user=user)) == 1:
                button_status = 'friend_request_sent'

    context = {
        'user': user,
        'button_status': button_status,
        # 'friends_list': friends,
        'sent_friend_requests': sent_friend_requests,
        'rec_friend_requests': rec_friend_requests
    }

    return render(request, "users/view_profile.html", context)

