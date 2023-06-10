import pytest
from django.shortcuts import reverse

@pytest.mark.django_db
def test_guilds_view_all_none_existent(client):
    response = client.get(reverse('guild_view_all', args=[1]))
    queryset = response.context['guilds']
    assert not queryset

@pytest.mark.django_db
def test_guilds_view_all_one_existent(client, guild):
    response = client.get(reverse('guild_view_all', args=[1]))
    queryset = response.context['guilds']
    assert queryset

