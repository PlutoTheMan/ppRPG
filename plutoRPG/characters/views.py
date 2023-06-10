from django.shortcuts import render, redirect
from .forms import *
from django.views import View
from .models import Character, Skills, Equipment, Account, Item
from guilds.models import Guild
from django.shortcuts import reverse
from django.contrib.auth.models import User

def view_character(request, name):
    """
    Handles request to view character with given name.

    :param request: Django request object.
    :param name: (string), name given by user.
    :return: (HttpResponse) character view page with context.
    """
    char = Character.objects.filter(name=name).first()
    ctx = {}
    if char:
        ctx['character'] = char
    return render(request, "character_view.html", ctx)
def view_all_characters(request, page):
    """
    Handles request to view all character.

    :param request: Django request object.
    :param page: (number), number of page (10 characters per page)
    :return: (HttpResponse) All characters list page with context.
    """
    if int(page) < 1:
        return redirect('/characters/all/1')
    limit = int(page)*10
    # chars = Character.objects.all().order_by('level').values().reverse()[limit-10:limit+1]
    chars = Character.objects.all().order_by('level').reverse()[limit-10:limit+1]
    ctx = {'characters': chars, 'page': page}
    return render(request, "character_all_list.html", ctx)
class DeleteCharacterView(View):
    """Handles request to delete character."""

    def get(self, request, name):
        """
        Handles request to delete character with given name, confirmation stage.

        :param request: Django request object.
        :param name: (string), name given by user.
        :return: (HttpResponse) redirect to homepage or character deletion page.
        """
        verify = Character.objects.filter(user=request.user, name=name).first()
        if not verify:
            return redirect('homepage')
        else:
            return render(request, "character_delete_confirm.html", {'name': verify.name})

    def post(self, request, name):
        """
        Handles request to delete character with given name, final stage.

        :param request: Django request object.
        :param name: (string), name given by user.
        :return: (HttpResponse) redirect to character delete confirmation page / character manager / homepage.
        """
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

class CharactersManagerView(View):
    """Handles character management"""
    def get(self, request):
        """
        Checks user authentication and returns HttpResponse.

        :param request: Django request object.
        :return: (HttpResponse) redirect to character manager page / homepage.
        """
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
        """
        May create new character, based on request form validation.

        :param request: Django request object.
        :return: (HttpResponse) redirect to character manager page / homepage.
        """
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
    """Handles request to create guild"""
    def get(self, request, name):
        """
        Rendering create guild page or redirecting to homepage if not logged in.

        :param request: Django request object.
        :param name: (string), name of the guild given by user.
        :return: (HttpResponse) redirect to guild creation page / homepage.
        """
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
        """
        Attempting to create new guild.

        :param request: Django request object.
        :param name: (string), name of the guild given by user.
        :return: (HttpResponse) redirect to homepage.
        """
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
            return redirect('homepage')

        form = request.POST
        guild_name = form['name']
        Guild.objects.create(leader=character, name=guild_name)

        return redirect(reverse('character_manager'))
