import pytest
from django.shortcuts import reverse
import json

@pytest.mark.django_db
def test_get_characters_not_logged_empty_list(client):
    response = client.get(reverse('get_characters'))
    assert len(response.content) == 0

@pytest.mark.django_db
def test_get_characters_logged_in_no_characters(client, user):
    client.force_login(user)
    response = client.get(reverse('get_characters'))
    assert len(response.content) == 0

@pytest.mark.django_db
def test_get_characters_logged_in_has_character(client, user, character):
    client.force_login(user)
    response = client.get(reverse('get_characters'))
    assert len(response.content) > 0

@pytest.mark.django_db
def test_get_characters_logged_in_has_character_correct_list(client, user, character):
    client.force_login(user)
    response = client.get(reverse('get_characters'))
    content_parsed = json.loads(response.content.decode('utf-8'))
    check_name = character.name == content_parsed[0][0]
    check_level = character.level == content_parsed[0][1]
    assert check_name and check_level