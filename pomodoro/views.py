from users.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse

@login_required
def home(request):
    """
    Function based view for directing to the homepage
    """
    return render(request, 'home.html', {'home': home})

@login_required
def update_coins(request):
    """
    Function based view for increasing/decreasing a user's coin balance
    """
    try:
        user = request.user
    except User.DoesNotExist:
        raise Http404("No user matches the given query.")
    if request.is_ajax() and request.method=='GET':
        return JsonResponse({'coins': user.profile.coins})
    elif request.is_ajax() and request.method=='POST':
        amount = int(request.POST["coins"])
        user.profile.coins += amount
        if amount >= 0:
            user.profile.cycles += 1
        user.save()
        return JsonResponse({'coins': user.profile.coins})
    else:
        raise Http404 

def leaderboard(request):
    """
    Function based view for the leaderboard
    """
    rankings= range(1,11)
    topCoins = zip(User.objects.all().order_by('-profile__coins')[:10], rankings)
    topPomodoros = zip(User.objects.all().order_by('-profile__cycles')[:10], rankings)
    return render(request, 'leaderboard.html', {'topCoins': topCoins, 'topPomodoros': topPomodoros})

