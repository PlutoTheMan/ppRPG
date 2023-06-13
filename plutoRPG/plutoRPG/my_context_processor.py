from django.utils import timezone
from django.template import loader


def admin_panel(request):
    ctx = {}
    if request.user.is_superuser:
        superuser_panel = loader.get_template('superuser_panel.html').render()
        ctx = {
            "admin_panel": superuser_panel
        }
    return ctx
