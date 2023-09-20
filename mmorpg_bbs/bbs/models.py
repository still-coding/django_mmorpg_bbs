from django.contrib.auth.models import User
from django.db import models
from PIL import Image


class Ad(models.Model):

    class Category(models.TextChoices):
        TANK = 'TK', 'Tanks'
        HEAL = 'HL', 'Heals'
        DD = 'DD', 'Damagedealers'
        MERCHANT = 'MR', 'Merchants'
        GUILDMASTER = 'GM', 'Guildmasters'
        QUESTGIVER = 'QG', 'Questgivers' 
        BLACKSMITH = 'BS', 'Blacksmiths'
        LEATHERMAN = 'LM', 'Leathermans'
        POTIONMASTER = 'PM', 'Potionmasters'
        SPELLMASTER = 'SM', 'Spellmasters'

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=2, choices=Category.choices, default=Category.TANK)

    def __str__(self):
        return f'#{self.pk}, title: {self.title}, category: {self.get_category_display()}, user: {self.user.username},'

    def get_absolute_url(self):
        return f'/{self.id}'

class Response(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'#{self.pk}, ad: {self.ad.pk}, user: {self.user.username}, text: {self.text[:5]}..., accepted: {self.accepted}'


class Picture(models.Model):
    image = models.ImageField(upload_to='ads_pictures')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        output_size = (800, 500)
        img = img.resize(output_size)
        img.save(self.image.path)
