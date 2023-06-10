import pytest
from django.shortcuts import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_logged_in_redirect(client, user):
    client.force_login(user)
    response = client.get(reverse('register'))
    assert response.status_code == 302 and response.url == reverse('homepage')

@pytest.mark.django_db
def test_logged_out_render(client, user):
    response = client.get(reverse('register'))
    assert response.status_code != 302

@pytest.mark.django_db
def test_user_exists_deny(client, user, register_form_real_data):
    response = client.post(reverse('register'), register_form_real_data)
    check_errors_length = len(response.context['form'].errors.keys())
    assert check_errors_length > 0

@pytest.mark.django_db
def test_accept_registering_non_existent_user_correct_form(client, register_form_correct_user_data):
    response = client.post(reverse('register'), register_form_correct_user_data)
    user = User.objects.filter(username=register_form_correct_user_data['username'])
    assert user

@pytest.mark.django_db
def test_wrong_password_not_registered_deny(client, register_form_incorrect_user_password):
    response = client.post(reverse('register'), register_form_incorrect_user_password)
    user = User.objects.filter(username=register_form_incorrect_user_password['username'])
    assert not user

@pytest.mark.django_db
def test_empty_password_not_registered_deny(client, register_form_empty_user_name):
    response = client.post(reverse('register'), register_form_empty_user_name)
    user = User.objects.filter(username=register_form_empty_user_name['username'])
    assert not user
