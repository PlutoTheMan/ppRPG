import pytest
from django.shortcuts import reverse
from django.contrib import auth

@pytest.mark.django_db
def test_logged_in_trying_log_in_redirect(client, user):
    client.force_login(user)
    content = client.get(reverse('login'))
    assert content.status_code == 302 and content.url == reverse('homepage')

@pytest.mark.django_db
def test_logged_out_trying_log_in_accept(client, user):
    content = client.get(reverse('login'))
    assert content.status_code == 200 and content.context['content'] == "page_login"

@pytest.mark.django_db
def test_login_non_existent_user(client, login_form_fake_data):
    response = client.post(reverse('login'), login_form_fake_data)
    check_wrong_username_or_password_put = response.context['msg'] == "Wrong username or password."
    assert check_wrong_username_or_password_put

@pytest.mark.django_db
def test_login_existent_user(client, user, login_form_real_data):
    check_is_logged_out_before_url_navigate = auth.get_user(client).is_anonymous
    response = client.post(reverse('login'), login_form_real_data)
    check_logged_in_after_url_post = not auth.get_user(client).is_anonymous
    assert check_is_logged_out_before_url_navigate and check_logged_in_after_url_post