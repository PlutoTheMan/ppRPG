import pytest
from django.shortcuts import reverse
import json
@pytest.mark.django_db
def test_select_character_logged_out_empty_response(client):
    response = client.get(reverse('select_character', args=['1']))
    assert len(response.content) == 0

@pytest.mark.django_db
def test_select_character_not_the_owner_rejected(client, user, user2, character, character2):
    client.force_login(user)
    response = client.get(reverse('select_character', args=[character2.name]))
    content = json.loads(response.content.decode('utf-8'))
    assert content['accepted'] is False
