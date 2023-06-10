from django.urls import reverse
import pytest
test_username = "1"

@pytest.mark.django_db
def test_character_existent_generate_list_with_player(client, character):
    response = client.get(reverse('characters_page', args=['1']))
    content = response.content.decode('utf-8')

    check_character_in_list = f"Name: {character.name}" in content

    assert check_character_in_list

@pytest.mark.django_db
def test_character_non_existent_generate_empty_list(client):
    response = client.get(reverse('characters_page', args=['1']))
    content = response.content.decode('utf-8')

    check_character_in_list = f"Name: {test_username}" not in content

    assert check_character_in_list