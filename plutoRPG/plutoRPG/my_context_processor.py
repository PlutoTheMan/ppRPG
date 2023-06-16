from django.utils import timezone
from django.template import loader
from characters.models import Character


def admin_panel(request):
    ctx = {}
    if request.user.is_superuser:
        superuser_panel = loader.get_template('superuser_panel.html').render()
        ctx = {
            "admin_panel": superuser_panel
        }
    return ctx

def top_5_players(request):
    top_players = Character.objects.all().order_by('-level')[:5]
    ctx = {
        "top_5_players": top_players
    }
    return ctx
