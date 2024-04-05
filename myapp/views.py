from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from django.contrib.auth.models import User

from .models import Recipe, UserProfile, RecipeCategory, Category
from .forms import RecipeForm, UserProfileForm


# Create your views here.

def search(request):
    query = request.GET.get('q', '')
    recipes = Recipe.objects.all()
    if query:
        recipes = recipes.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(steps__icontains=query) |
            Q(author__username__icontains=query)
        )

    return render(request, 'myapp/search_results.html', {'recipes': recipes, 'query': query})


@login_required
def edit_profile(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'myapp/edit_profile.html', {'form': form})


@login_required
def profile(request):
    # superuser = User.objects.get(username='admin')
    # userprofile = UserProfile.objects.create(user=superuser)
    # superuser.save()
    # userprofile.save()
    user_profile = request.user.userprofile
    user_form = UserProfile.objects.get(user=request.user)
    context = {
        'user_profile': user_profile,
        'user_form': user_form

    }
    return render(request, 'myapp/profile.html', context)


def index(request):
    recipes = Recipe.objects.all().order_by('?')[:5]
    context = {
        'recipes': recipes
    }
    return render(request, 'myapp/index.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'myapp/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'myapp/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            steps = form.cleaned_data['steps']
            time = form.cleaned_data['time']
            image = request.FILES['image']
            category = form.cleaned_data['categories']
            author = request.user

            recipe = Recipe(title=title,
                            description=description,
                            steps=steps,
                            time=time,
                            image=image,
                            author=author)
            recipe.save()

            categ = Category.objects.get(name=category)
            RecipeCategory.objects.create(recipe=recipe, category=categ)

            messages.success(request, 'Рецепт успешно добавлен')
            return render(request, 'myapp/add_recipe.html', {'recipe': recipe})
    else:
        form = RecipeForm()

    recipes = Recipe.objects.all()

    context = {
        'form': form,
        'recipes': recipes,
        'title': 'Добавление рецепта',


    }

    return render(request, 'myapp/add_recipe.html', context)


def read_all_recipes(request):
    recipes = Recipe.objects.all()

    context = {
        'recipes': recipes,
        'title': 'Все рецепты',
    }
    return render(request, 'myapp/all_recipe.html', context)


def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            steps = form.cleaned_data['steps']
            time = form.cleaned_data['time']
            image = request.FILES['image']
            author = form.cleaned_data['author']

            recipe.title = title
            recipe.description = description
            recipe.steps = steps
            recipe.time = time
            recipe.image = image
            recipe.author = author
            recipe.save()

            messages.success(request, 'Продукт успешно отредактирован')
            return render(request, 'myapp/recipe_detail.html', {'recipe': recipe})
    else:
        form = RecipeForm()
    recipes = Recipe.objects.all()

    context = {
        'form': form,
        'recipes': recipes,
        'title': 'Редактирование рецепта',
        'recipe': recipe

    }

    return render(request, 'myapp/edit_recipe.html', context)


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    category = RecipeCategory.objects.filter(recipe=recipe).first()
    categ = Category.objects.get(id=category.category.id)
    context = {
        'recipe': recipe,
        'categ': categ
    }
    return render(request, 'myapp/recipe_detail.html', context)
