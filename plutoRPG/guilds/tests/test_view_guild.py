import pytest
from django.shortcuts import reverse

@pytest.mark.django_db
def test_view_guild_not_existent_redirect(client):
    response = client.get(reverse('guild_view', args=['abc']))
    assert response.status_code == 302 and response.url == reverse('homepage')

@pytest.mark.django_db
def test_view_guild_existent_content(client, guild):
    response = client.get(reverse('guild_view', args=[guild.name]))
    # Guild in ctx means the guild is found.
    assert response.context['guild'].name == guild.name and response.status_code == 200