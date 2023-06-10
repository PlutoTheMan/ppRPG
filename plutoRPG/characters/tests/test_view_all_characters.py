from django.urls import reverse
import pytest

test_username = "1"


@pytest.mark.django_db
def test_generate_table_with_character_info(client, character):
    response = client.get(reverse('characters_all') + character.name)
    content = response.content.decode('utf-8')

    check_char_name = character.name in content
    check_level = str(character.level) in content
    check_experience = str(character.experience) in content

    assert check_char_name and check_level and check_experience


@pytest.mark.django_db
def test_non_existent_character_generate_with_no_character_found_msg(client):
    response = client.get(reverse('characters_all') + test_username)
    content = response.content.decode('utf-8')

    assert "Character not found." in content


