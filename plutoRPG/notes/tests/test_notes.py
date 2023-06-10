import pytest
from django.shortcuts import reverse
from notes.models import Note

@pytest.mark.django_db
def test_logged_out_redirect(client):
    response = client.get(reverse('notes'))
    assert response.status_code == 302 and response.url == reverse('homepage')

@pytest.mark.django_db
def test_logged_in_render(client, user):
    client.force_login(user)
    response = client.get(reverse('notes'))
    check_context_notes = response.context['content'] == "notes"
    assert response.status_code == 200 and check_context_notes

@pytest.mark.django_db
def test_note_saved_after_post(client, user, notes_correct_form_data):
    client.force_login(user)
    response = client.post(reverse('notes'), notes_correct_form_data)
    note = Note.objects.filter(author=user).first()
    check_saved_note = notes_correct_form_data['content'] == note.content
    assert response.status_code == 200 and check_saved_note



