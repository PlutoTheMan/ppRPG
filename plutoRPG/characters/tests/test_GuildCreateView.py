from django.urls import reverse
import pytest

test_username = "1"

@pytest.mark.django_db
def test_not_logged_in_create_guild_redirect(client, guild_create_form_data):
    response = client.post(reverse('guild_create', args=['1']), guild_create_form_data)
    assert response.status_code == 302 and response.url == reverse('homepage')

@pytest.mark.django_db
def test_doesnt_own_character_create_guild_redirect(client, user):
    client.force_login(user=user)
    response = client.get(reverse('guild_create', args=[test_username]))
    assert response.status_code == 302 and response.url == reverse('homepage')

@pytest.mark.django_db
def test_has_no_guild_create_accept(client, user, character, guild_create_form_data):
    client.force_login(user=user)
    response = client.post(reverse('guild_create', args=[character.name]), guild_create_form_data)
    assert character.has_guild()

@pytest.mark.django_db
def test_has_guild_already_create_decline(client, user, character, guild_create_form_data):
    client.force_login(user=user)
    response = client.post(reverse('guild_create', args=[character.name]), guild_create_form_data)
    check_has_guild_already = character.has_guild()
    # Should get redirected to home if player has guild
    response = client.post(reverse('guild_create', args=[character.name]), guild_create_form_data)
    assert check_has_guild_already and response.status_code == 302 and response.url == reverse('homepage')
