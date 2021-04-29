from django.db import models
from django.contrib.auth.models import User  # to get User for the profile page
from .util import get_random_id
from django.template.defaultfilters import slugify
from django.shortcuts import reverse
from django.db.models import Q

# Create your models here.

class ProfileManager(models.Manager):
    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        my_profile = Profile.objects.get(user=sender)

        qs = Relationship.objects.filter(Q(sender=my_profile) | Q(receiver=my_profile))
        
        accepted = set([])

        for rel in qs:
            if(rel.status == "accepted"):
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        
        available = [profile for profile in profiles if profile not in accepted]

        return available


class Profile(models.Model):
    first_name  = models.CharField(max_length=80,blank=True)
    last_name  = models.CharField(max_length=80, blank = True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # using User from the django.contrib.auth.models import User
    bio = models.TextField(max_length=300, default = "No Bio...")
    email = models.EmailField(max_length=254, blank = True)
    country  =  models.CharField(blank = True, max_length=50)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    friends = models.ManyToManyField(User, blank = True, related_name = 'friends') 
    slug = models.SlugField(unique = True, blank = True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}--{self.created.strftime('%d-%m-%Y')}"

    def get_absolute_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"slug": self.slug})
    
    def get_friends(self):
        return self.friends.all()

    def get_friends_count(self):
        return self.friends.all().count()

    def get_posts_num(self):
        return self.posts.all().count()

    def get_all_authors_posts(self):
        return self.posts.all()  # author field in posts.models with related_name posts

    # get all the like-posts count.
    def get_likes_given(self): 
        likes =  self.like_set.all()    # like Model in posts foreign_key relation and no related name so 
                                        # "<model_name>_set" else give related_name
                                    
        # print("Likes:  ",likes)
        total_liked = 0
        for  like_status in likes:  
            if (like_status.value  == 'Like'):
                total_liked += 1
        return total_liked

    # get all the likes from all posts of self
    def get_likes_received(self):  
        posts = self.posts.all()
        # print(posts)
        total_liked = 0
        for post in posts:
            total_liked += post.liked.all().count()

        # print(total_liked)
        return total_liked


    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if(self.first_name != self.__initial_first_name and self.last_name != self.__initial_last_name or self.slug ==""):
            if self.first_name and self.last_name:  
                to_slug = slugify(str(self.first_name)+ " " + str(self.last_name)) 
                ex = Profile.objects.filter(slug=to_slug).exists()    
                while ex:
                    to_slug = slugify(to_slug+ " "+ str(get_random_id))
                    ex = Profile.objects.filter(slug = to_slug).exists()
        else:
            to_slug = str(self.user)

        self.slug = to_slug
        super().save(*args, **kwargs)



STATUS_CHOICES = (
                    ('send', 'send'),
                    ('accepted', 'accepted')
                )

class RelationshipManager(models.Manager):
    def invitaions_receieved(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs




class Relationship(models.Model):
    sender = models.ForeignKey(Profile,  on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile,  on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=12, choices = STATUS_CHOICES)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    objects = RelationshipManager()

    def __str__(self):
        return f'{self.sender}--{self.receiver}--{self.status}'

