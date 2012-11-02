from eotd.models import Faction

def site_wide_context(request):
    return { 'factions': Faction.objects.all() }

