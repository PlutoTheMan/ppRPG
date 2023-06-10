from django.shortcuts import reverse
import pytest

@pytest.mark.django_db
def test_quests_redirect(client):
    response = client.get(reverse('quests'))
    ctx = response.context['content']
    assert response.status_code == 200 and ctx == "quests"