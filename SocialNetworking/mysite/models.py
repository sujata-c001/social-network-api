from datetime import datetime, timezone
import logging
from django.db import models
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    email = forms.CharField(max_length=20, widget=forms.EmailInput)

class RequestStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    ACCEPTED = 'ACCEPTED', 'Accepted'
    REJECTED = 'REJECTED', 'Rejected'
    BLOCKED = 'BLOCKED', 'Blocked'

class User(models.Model):
    name = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)    

    @classmethod
    def search_user(cls, **kwargs):
        user_list = []
        email = kwargs.get('email', None)
        name = kwargs.get('name', None)
        all_users = cls.objects.filter(cls.email==email | cls.name==name).all()
        for u in all_users:
            user_list.append((u.name, u.email))
        return user_list


class FriendRequestsManagement(models.Model):
    sender =  models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, related_name="reciever", on_delete=models.CASCADE)
    status = models.CharField(default=None, max_length=20)
    created_on = models.DateTimeField(default=datetime.utcnow())

    @classmethod
    def send_request(cls, sender, reciever):
        existing_req = cls.objects.filter(sender=sender, reciever=reciever).first()
        if existing_req:
            return existing_req
        try:
            friend_req = cls.objects.create(sender=sender, reciever=reciever, status=RequestStatus.PENDING, created_on=datetime.utcnow())
            return friend_req
        except Exception as e:
            logging.error(f'Failed to send friend request: {e}')
            return None
        
    def accept_request(self):
        self.status = RequestStatus.ACCEPTED
        self.save()
        Friends.create_friends(user1=self.sender, user2=self.reciever)

    def reject_request(self):
        self.status = RequestStatus.REJECTED
        self.save()


class Friends(models.Model):
    user1 = models.ForeignKey(User, related_name='friendships_initiated', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friendships_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.utcnow())

    @classmethod
    def create_friendship(cls, user1, user2):
        friendship, created = cls.objects.get_or_create(user1=user1, user2=user2)
        return friendship
