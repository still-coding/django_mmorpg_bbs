from django.contrib.auth.models import User
from django.db import models
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.png', upload_to='profile_avatars')
    mailing_period = models.IntegerField(default=0)
    last_mail = models.DateTimeField(auto_now_add=True)
    otp = models.IntegerField(default=0)

    def __str__(self):
        return f'#{self.pk}, username: {self.user.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.avatar.path)
        if img.height > 150 or img.width > 150:
            output_size = (150, 150)
            img.thumbnail(output_size)
            img.save(self.avatar.path)