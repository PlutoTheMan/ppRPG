import pytest
from django.shortcuts import reverse

@pytest.mark.django_db
def test_redirect(client):
    response = client.get(reverse('patch_notes'))
    ctx = response.context['content']
    assert response.status_code == 200 and ctx == "patch_notes"