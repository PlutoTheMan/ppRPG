import pytest
from django.shortcuts import reverse

test_guild_name = "test_guild_123"

@pytest.mark.django_db
def test_check_context_guild_not_existent(client):
    content = client.get(reverse('guild_members', args=[test_guild_name]))
    assert content.status_code == 302 and content.url == reverse('homepage')

@pytest.mark.django_db
def test_check_context_guild_existent(client, guild):
    content = client.get(reverse('guild_members', args=[guild.name]))
    # Checking just a leader for now, since leader is not counted as member
    assert content.status_code == 200 and content.context['leader']

