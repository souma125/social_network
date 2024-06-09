from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User,related_name='sent_requests',on_delete=models.CASCADE)
    to_user = models.ForeignKey(User,related_name='received_reqests',on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('from_user','to_user')