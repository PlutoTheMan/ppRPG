from django.urls import reverse
import pytest
from characters.models import Character

@pytest.mark.django_db
def test_not_logged_in_redirected_home(client):
    response = client.get(reverse('character_manager'))
    assert response.status_code == 302 and response.url == "/"

@pytest.mark.django_db
def test_logged_in_render(client, user):
    client.force_login(user=user)
    response = client.get(reverse('character_manager'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_logged_in_existent_character_create_decline(client, user, character):
    client.force_login(user=user)
    response = client.post(reverse('character_manager'), {'name': character.name})
    check_errors_length = len(response.context['form'].errors.keys()) > 0
    assert check_errors_length

@pytest.mark.django_db
def test_logged_in_wrong_name_create_decline(client, user):
    client.force_login(user=user)
    response = client.post(reverse('character_manager'), {'name': ""})
    check_errors_length = len(response.context['form'].errors.keys()) > 0
    assert check_errors_length

@pytest.mark.django_db
def test_logged_in_non_existent_character_create_accept(client, user):
    test_name = "Gulu"
    client.force_login(user=user)
    response = client.post(reverse('character_manager'), {'name': test_name})
    char = Character.objects.filter(name=test_name).first()
    assert char
