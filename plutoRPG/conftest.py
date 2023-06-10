import pytest
from django.contrib.auth.models import User
from django.test import Client
from characters.models import Character, Account, Skills, Item, Equipment
from guilds.models import Guild

test_guild_name = "test_guild_123"
@pytest.fixture
def notes_correct_form_data():
    return {
        'content': 'test_note_description',
    }

@pytest.fixture
def guild_create_form_data():
    return {
        'name': 'Test_guild',
    }

@pytest.fixture
def login_form_fake_data():
    return {
        'username': 'fake_login_01',
        'password': 'fake_login_02',
    }

@pytest.fixture
def register_form_incorrect_user_password():
    return {
        'username': '1',
        'password1': '3',
        'password2': '3',
    }

@pytest.fixture
def register_form_empty_user_name():
    return {
        'username': '',
        'password1': 'RandomTest',
        'password2': 'RandomTest',
    }

@pytest.fixture
def register_form_correct_user_data():
    return {
        'username': '1',
        'password1': 'RandomTest!552',
        'password2': 'RandomTest!552',
    }

@pytest.fixture
def register_form_real_data():
    return {
        'username': '1',
        'password': '123',
    }

@pytest.fixture
def login_form_real_data():
    return {
        'username': '1',
        'password': '123',
    }
#
# @pytest.fixture
# def character_form_new_real_data():
#     return {
#         'name': '1',
#         'password': '123',
#     }

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user():
    return User.objects.create_user(username="1", password="123")

@pytest.fixture
def user2():
    return User.objects.create_user(username="2", password="123")

@pytest.fixture
def character():
    user = User.objects.filter(username="1").first()
    if user is None:
        user = User.objects.create_user(username="1", password="123")

    character = Character.objects.create(user=user, name="Test")
    skills = Skills.objects.create(character=character)
    item = Item.objects.create(game_id=1)
    equipment = Equipment.objects.create(character=character, bag_0=item)
    return character

@pytest.fixture
def character2():
    user = User.objects.filter(username="2").first()
    if user is None:
        user = User.objects.create_user(username="2", password="123")
    return Character.objects.create(user=user, name="Test2")

@pytest.fixture
def account_character():
    user = User.objects.create_user(username="1", password="123")
    char = Character.objects.create(user=user, name="Test")
    return {'user': user, 'character': char}

@pytest.fixture
def guild():
    user = User.objects.all().first()
    if user is None:
        user = User.objects.create_user(username="1", password="123")

    character = Character.objects.all().first()
    if character is None:
        character = Character.objects.create(user=user, name="Test")

    guild = Guild.objects.create(
        leader=character,
        name=test_guild_name
    )

    return guild