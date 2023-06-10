import pytest
from django.shortcuts import reverse

@pytest.mark.django_db
def test_credits_render(client):
    response = client.get(reverse('credits'))
    check_content = response.context['content'] == "credits"
    check_status = response.status_code == 200
    assert check_content and check_status

@pytest.mark.django_db
def test_credits_authors_mentioned(client):
    response = client.get(reverse('credits'))
    html_decoded = response.content.decode('utf-8').lower()
    check_outfits_credits = "outfit" in html_decoded
    check_tiled_credits = "tiled" in html_decoded
    check_tailwind_credits = "tailwind" in html_decoded
    assert check_outfits_credits and check_tiled_credits and check_tailwind_credits