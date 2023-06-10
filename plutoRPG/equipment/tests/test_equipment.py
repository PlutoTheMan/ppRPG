import pytest
from django.shortcuts import reverse

def test_devlogs_redirect(client):
    response = client.get(reverse('equipment'))
    ctx = response.context['content']
    assert response.status_code == 200 and ctx == "equipment"
