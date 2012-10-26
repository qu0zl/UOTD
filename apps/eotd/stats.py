from eotd.models import Game

def recentGames():
    return Game.objects.exclude(gameteam_set__freezeTime=None).order_by("-date")[:3]
