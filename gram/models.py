from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.


class Profile(models.Model):
    Name = models.TextField(default="Anonymous")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)
    profile_picture = models.ImageField(upload_to='users/', default='users/user.png', null=True)
    bio = models.TextField(default="Welcome Me!")



    @classmethod
    def find_profile(cls,name):
        return cls.objects.filter(user__username__icontains = name).all()

    def togglefollow(self, profile):
        if self.following.filter(followee=profile).count() == 0:
            Follows(followee=profile, follower=self).save()
            return True
        else:
            self.following.filter(followee=profile).delete()
            return False

    def like(self, photo):
        if self.mylikes.filter(photo=photo).count() == 0:
            Likes(photo=photo,user=self).save()

    def save_image(self, photo, *args, **kwargs):
        if self.saves.filter(photo=photo).count() == 0:
            Saves(photo=photo,user=self).save()
        else:
            self.saves.filter(photo=photo).delete()

    def unlike(self, photo):
        self.mylikes.filter(photo=photo).all().delete()

    def comment(self, photo, text):
        Comment(text=text, photo=photo, user=self).save()

    def post(self, form):
        image = form.save(commit=False)
        image.user = self
        image.save()

    @property
    def follows(self):
        return [follow.followee for follow in self.following.all()]

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print(instance)
        Profile.objects.create(
            Name=instance.username,
            user = instance
        )

class Post(models.Model):
    image = models.ImageField(upload_to='posts/')
    user = models.ForeignKey(Profile, related_name='posts', on_delete=models.CASCADE)

    @property
    def get_comments(self):
        return self.comments.all()

    @property
    def count_likes(self):
        return self.photolikes.count()

    class Meta:
        ordering = ["-pk"]
class Comment(models.Model):
    text = models.TextField()
    photo = models.ForeignKey(Post, related_name='comments',on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, related_name='comments', on_delete=models.CASCADE)

class Likes(models.Model):
    user = models.ForeignKey(Profile, related_name='mylikes',on_delete=models.CASCADE)
    photo = models.ForeignKey(Post, related_name='photolikes', on_delete=models.CASCADE)

class Save(models.Model):
    user = models.ForeignKey(Profile, related_name='user_save', on_delete=models.CASCADE)
    photo = models.ForeignKey(Post, on_delete=models.CASCADE)
    class Meta:
        ordering = ["-pk"]
class Follows(models.Model):
    follower = models.ForeignKey(Profile, related_name='following', on_delete=models.CASCADE)
    followee = models.ForeignKey(Profile, related_name='followers', on_delete=models.CASCADE)