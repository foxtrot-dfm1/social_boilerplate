from django.db import models
from user.models import User

class Post(models.Model): #todo : implement title slugifying
    title = models.CharField(max_length = 100)
    body = models.TextField(blank = True)
    date_pub = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "User")
    likes = models.ManyToManyField(User, blank = True, related_name = "likes")
    likes_num = models.IntegerField(default=0)

    def like(self, user):
        if user and not user in self.likes.all():
            self.likes.add(user)
            self.likes_num += 1
            self.save()
            return self
        return False
    
    def unlike(self, user):
        if user and user in self.likes.all():
            self.likes.remove(user)
            self.likes_num -= 1
            self.save()
            return self
        return False

    def __str__(self):
        return self.title

    
    class Meta:
        ordering = ['-date_pub']
