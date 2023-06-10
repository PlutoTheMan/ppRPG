import pytest
from django.shortcuts import reverse

def test_classes_redirect(client):
    response = client.get(reverse('classes'))
    ctx = response.context['content']
    assert response.status_code == 200 and ctx == "classes"
