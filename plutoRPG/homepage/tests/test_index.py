import pytest
from django.shortcuts import reverse
from django.contrib import auth

@pytest.mark.django_db
def test_detected_logged_in_user(client, user):
    client.force_login(user)
    content = client.get(reverse('homepage'))
    check_client_anonymous = not auth.get_user(client).is_anonymous
    check_view_anonymous = not content.context['user'].is_anonymous
    assert check_client_anonymous and check_view_anonymous

@pytest.mark.django_db
def test_detected_logged_out_user(client, user):
    content = client.get(reverse('homepage'))
    check_client_anonymous = auth.get_user(client).is_anonymous
    check_view_anonymous = content.context['user'].is_anonymous
    assert check_client_anonymous and check_view_anonymous

@pytest.mark.django_db
def test_returned_homepage(client, user):
    content = client.get(reverse('homepage'))
    assert content.status_code == 200 and content.context['content'] == "homepage"
