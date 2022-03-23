from .models import Post

class LikeUnlikeMixin:
    model = None
    def like(self, user, id):
        instance = self.model.objects.get(id=id)
        if instance != None:
            return instance.like(user)
        return False
    
    def unlike(self, user, id):
        instance = self.model.objects.get(id=id)
        if instance != None:
            return instance.unlike(user)
        return False