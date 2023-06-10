from characters.models import Character
from django.urls import reverse
import pytest

@pytest.mark.django_db
def test_logged_in_existent_get_confirmation_msg(client, user, character):
    client.force_login(user=user)

    response = client.get(reverse('character_delete', args=[character.name]))
    response_text = response.content.decode('utf-8')
    assert response.status_code == 200 and "Do you really want to delete" in response_text

@pytest.mark.django_db
def test_logged_in_existent_delete_character_owner(client, user, character):
    client.force_login(user=user)
    response = client.post(reverse('character_delete', args=[character.name]))
    assert response.status_code == 302 and Character.objects.all().first() is None

@pytest.mark.django_db
def test_logged_in_delete_character_not_owner(client, user, character, character2):
    client.force_login(user=user)
    response = client.post(reverse('character_delete', args=[character2.name]))
    assert response.status_code == 302 and Character.objects.all().first()

@pytest.mark.django_db
def test_logged_in_delete_character_not_found(client, user):
    client.force_login(user=user)
    response = client.post(reverse('character_delete', args=['1']))
    assert response.status_code == 302 and Character.objects.filter(name='1').first() is None

