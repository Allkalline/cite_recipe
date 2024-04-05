from django import forms
from django.contrib.auth.models import User


from .models import Recipe, Category, UserProfile



class RecipeForm(forms.Form):
    title = forms.CharField(max_length=200, label="Название рецепта")
    description = forms.CharField(widget=forms.Textarea, label="Описание и ингредиенты")
    steps = forms.CharField(widget=forms.Textarea, label="Шаги приготовления")
    time = forms.IntegerField(label="Время приготовления (в минутах)")
    image = forms.ImageField(label="Изображение готового блюда")
    categories = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'phone', 'email', 'image']
