from django.shortcuts import render, redirect
from .forms import *
from django.views import View
from .models import Character, Skills, Equipment, Account, Item
from guilds.models import Guild
from django.contrib.auth.models import User

# Create your views here.
def view_character(request, name):
    char = Character.objects.filter(name=name).first()
    ctx = {'character': char}
    return render(request, "character_view.html", ctx)

def view_all_characters(request, page):
    if int(page) < 1:
        return redirect('/characters/all/1')
    limit = int(page)*10
    # chars = Character.objects.all().order_by('level').values().reverse()[limit-10:limit+1]
    chars = Character.objects.all().order_by('level').reverse()[limit-10:limit+1]
    ctx = {'characters': chars, 'page': page}
    return render(request, "character_all_list.html", ctx)

class DeleteCharacterView(View):
    def get(self, request, name):
        verify = Character.objects.filter(user=request.user, name=name).first()
        if not verify:
            return redirect('homepage')
        else:
            return render(request, "character_delete_confirm.html", {'name': verify.name})

    def post(self, request, name):
        account = Account.get_from_user(request.user)
        if account is not None:
            character = account.get_character(name)
            if character is not None:
                # If character is guild leader
                if character.is_guild_leader():
                    # if is the only member - allow deletion
                    members_count = character.guild.members.count()
                    if members_count == 0:
                        character.guild.delete()
                        character.delete()
                    else:
                        ctx = {'name': character.name,
                               'err_msg': 'Pass guild leadership to someone else first.'
                               }
                        return render(request, "character_delete_confirm.html", ctx)
                else:
                    character.delete()
                return redirect('character_manager')
            else:
                return redirect('homepage')
        return redirect('character_manager')
class CharacterManagerView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = NewCharacterForm()
            char_list = Character.objects.filter(user=request.user)
            ctx = {
                'form': form,
                'char_list': char_list,
               }
            return render(request, "character_manager.html", ctx)
        else:
            return redirect('homepage')
    def post(self, request):
        if request.user.is_authenticated:
            form = NewCharacterForm(request.POST)
            char_list = Character.objects.filter(user=request.user)
            if form.is_valid():
                user = request.user
                name = form.cleaned_data['name']
                new_character = Character.objects.create(user=user, name=name)
                skills = Skills.objects.create(character=new_character)
                item = Item.objects.create(game_id=1)
                equipment = Equipment.objects.create(character=new_character, bag_0=item)

                ctx = {
                    'form': form,
                    'msg_success': 'Characted created successfully',
                    'char_list': char_list,
                }
                return render(request, "character_manager.html", ctx)
            else:
                ctx = {
                    'form': form,
                    'msg_fail': 'Something went wrong. Try again.',
                    'char_list': char_list,
                }
                return render(request, "character_manager.html", ctx)
        else:
            return redirect('homepage')

class GuildCreateView(View):
    def get(self, request, name):
        if request.user.is_authenticated:
            account = Account.get_from_user(request.user)
            if account is None:
                return redirect('homepage')
            if account.owns_character(name):
                form = FormGuildCreate()
                ctx = {'form': form}
                return render(request, "guilds/create.html", ctx)
            return redirect('homepage')
        return redirect('homepage')
    def post(self, request, name):
        # Attempt Guild Create
        # Does player belong to account - repeat
        account = Account.get_from_user(request.user)
        if account is None:
            return redirect('homepage')
        if not account.owns_character(name):
            return redirect('homepage')

        # Does player have guild already?
        character = account.get_character(name)
        if character.has_guild():
            print("HAS GUILD")
            return redirect('homepage')

        form = request.POST
        guild_name = form['name']
        Guild.objects.create(leader=character, name=guild_name)

        return redirect('homepage')
