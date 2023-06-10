import pytest
from django.shortcuts import reverse

@pytest.mark.django_db
def test_play_not_logged_in_redirect(client):
    response = client.get(reverse('game'))
    assert response.status_code == 302 and response.url == reverse('login')

@pytest.mark.django_db
def test_play_logged_in_render(client, user):
    client.force_login(user)
    response = client.get(reverse('game'))
    assert response.status_code == 200 and response.context['content'] == "game"

@pytest.mark.django_db
def test_play_logged_in_context_has_characters_list(client, user, character):
    client.force_login(user)
    response = client.get(reverse('game'))
    assert 'characters' in response.context

@pytest.mark.django_db
def test_play_logged_in_context_has_no_characters(client, user):
    client.force_login(user)
    response = client.get(reverse('game'))
    assert 'characters' not in response.context
