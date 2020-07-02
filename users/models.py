from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    slug = models.SlugField(max_length=100)
    friends = models.ManyToManyField("Profile", blank=True)
    def __str__(self):
        return str(self.user.username)
    def get_absolute_url(self):
        return "/friends/{}".format(self.slug)
    # def save(self, *args, **kwargs):
    #     super(Profile, self).save(*args, **kwargs)

    #     img = Image.open(self.image.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
class Friend(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user', null=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user', null=True)
    # timestamp = models.DateTimeField(auto_now_add=True) # set when created 

    # def __str__(self):
    #     return "From {}, to {}".format(self.from_user.username, self.to_user.username)

    # 