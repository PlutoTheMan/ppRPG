import pytest
from django.shortcuts import reverse
import json

@pytest.mark.django_db
def test_get_map_tile_sets_logged_out_empty_response(client):
    response = client.get(reverse('get_map_tile_sets'))
    assert len(response.content) == 0

@pytest.mark.django_db
def test_get_map_tile_sets_logged_in_response(client, user):
    client.force_login(user)
    response = client.get(reverse('get_map_tile_sets'))
    content = json.loads(response.content.decode('utf-8'))
    assert 'tile_set' in content