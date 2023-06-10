import pytest
from django.shortcuts import reverse

@pytest.mark.django_db
def test_redirect_if_not_logged_in(client, guild):
    content = client.get(reverse('guild_manage', args=[guild.name]))
    assert content.status_code == 302 and content.url == reverse("homepage")

@pytest.mark.django_db
def test_manage_content_if_is_a_leader(client, user, guild):
    client.force_login(user)
    content = client.get(reverse('guild_manage', args=[guild.name]))
    assert content.status_code == 200 and content.context['guild']
