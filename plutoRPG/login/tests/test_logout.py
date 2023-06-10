import pytest
from django.shortcuts import reverse
from django.contrib import auth

@pytest.mark.django_db
def test_logout_when_logged_in(client, user):
    client.force_login(user)
    check_is_logged_in_before_logout = not auth.get_user(client).is_anonymous
    content = client.get(reverse('logout'))
    check_is_logged_out = auth.get_user(client).is_anonymous
    assert check_is_logged_in_before_logout and check_is_logged_out

@pytest.mark.django_db
def test_logout_when_logged_out_redirect(client):
    check_is_logged_out_before_url_navigate = auth.get_user(client).is_anonymous
    content = client.get(reverse('logout'))
    assert check_is_logged_out_before_url_navigate and content.status_code == 302 and content.url == reverse('homepage')


