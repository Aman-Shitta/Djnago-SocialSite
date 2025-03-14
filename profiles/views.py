from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Relationship
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
# Create your views here.

def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    user_context = {
        'my_profile' : profile
    }
    return render(request, 'profiles/profile.html', user_context)

def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)
    context = {'qs':qs}

    return render(request, 'profiles/profile_list.html', context)

def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs  = Relationship.objects.invitaions_receieved(profile)
    result = list(map(lambda x: x.sender, qs))

    is_empty  = False

    if len(result) == 0:
        is_empty = True

    context ={
        'qs':result,
        'is_empty':is_empty
    }

    return render(request, 'profiles/my_invites.html', context)

def accept_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)

        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == "send":
            rel.status = "accepted"
            rel.save()
    return redirect('profiles:my_invite_view')

def reject_invitation(request):
    if request.method == "POST":
        pk = request.POST.get("profile_pk")
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my_invite_view')


def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)
    context = {'qs':qs}
    print(qs)

    return render(request, 'profiles/to_invite_list.html', context)


def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)
    context = {'qs':qs}

    return render(request, 'profiles/profile_list.html', context)

class ProfileDetailView(DetailView):
    model = Profile
    template_name = "profiles/detail.html"

    # Overridden get_object method
    def get_object(self, slug=None):
        slug=self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []

        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False
               
        return context

class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles.profile_list.html'
    # context_object_name = 'qs'
    
    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []

        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context["is_empty"] = False
        if (len(self.get_queryset())==0):
            context["is_empty"] = True
        return context
    
def send_invitation(request):
    if request.method == "POST":
        pk = request.POST.get("profile_pk")
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender,receiver=receiver, status="send")

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('profiles:my_profile_view')

def remove_from_friends(request):
    if request.method == "POST":
        pk = request.POST.get("profile_pk")
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )

        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my_profile_view')