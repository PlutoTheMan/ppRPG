from django.shortcuts import render, redirect
from .models import Guild
from characters.models import Account, Character
from django.views import View

# Create your views here.
def view_guild(request, name):
    guild = Guild.objects.filter(name=name).first()
    if not guild:
        return redirect("homepage")
    ctx = {'guild': guild}
    if request.user.is_authenticated:
        account = Account.get_from_user(request.user)
        if account.owns_character(guild.leader.name):
            ctx["leader"] = True
    return render(request, "guilds/view_one.html", ctx)

def view_all_guilds(request, page):
    if int(page) < 1:
        return redirect('/characters/all/1')
    limit = int(page)*10
    guilds = Guild.objects.all().order_by('date_created').reverse()[limit-10:limit+1]
    ctx = {'guilds': guilds, 'page': page}
    return render(request, "guilds/list_page.html", ctx)

def view_guild_members(request, name):
    guild = Guild.objects.filter(name=name).first()
    if not guild:
        return redirect("homepage")

    members = guild.members.all()
    leader = guild.leader
    name = guild.name

    ctx = {'name': name,
           'members': members,
           'leader': leader
           }
    return render(request, "guilds/members.html", ctx)

class ManageGuildView(View):
    def get(self, request, name):
        if not request.user.is_authenticated:
            return redirect("homepage")

        account = Account.get_from_user(request.user)
        guild = Guild.objects.filter(name=name).first()

        if account.owns_character(guild.leader.name):
            members = guild.members.all()

            ctx = {'guild': guild,
                   'members': members,
                   }
            return render(request, "guilds/manage.html", ctx)
        else:
            return redirect("homepage")

    def post(self, request, name):
        # Should be safe, since tepmlates use autoescape?
        player = request.POST.get('name', '')
        # is player at all?
        player = Character.objects.filter(name=player).first()

        guild = Guild.objects.filter(name=name).first()
        members = guild.members.all()
        leader = guild.leader

        ctx = {'guild': guild,
               'members': members,
               'leader': leader
               }

        if player:
            # Decline when has guild
            if player.has_guild():
                ctx["msg_err"] = "Player already has guild."
                return render(request, "guilds/manage.html", ctx)
            if guild.pending_invites.all().filter(name=player.name).first():
                ctx["msg_err"] = "Player is already invited."
                return render(request, "guilds/manage.html", ctx)
            ctx["msg_success"] = "Player has been invited."
            guild.pending_invites.add(player)
            return render(request, "guilds/manage.html", ctx)
        else:
            ctx["msg_err"] = "Couldn't find a player with this nickname."
        return render(request, "guilds/manage.html", ctx)


