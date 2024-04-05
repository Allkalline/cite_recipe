from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    image = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return f'О себе: {self.bio} Номер телефона: {self.phone} E-mail: {self.email}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            fs = FileSystemStorage()
            filename = fs.save(self.image.name, self.image)
            self.image = fs.url(filename)
            super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    steps = models.TextField()
    time = models.IntegerField()
    image = models.ImageField(upload_to='recipes/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', through='RecipeCategory')

    def __str__(self):
        return (f'Название: {self.title},'
                f'Описание: {self.description},'
                f'Время приготовления: {self.time} минут,'
                f'Шаги приготовления: {self.steps},'
                f'Категория: {self.categories},'
                f'Автор: {self.author}')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            fs = FileSystemStorage()
            filename = fs.save(self.image.name, self.image)
            self.image = fs.url(filename)
            super().save(*args, **kwargs)




class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
