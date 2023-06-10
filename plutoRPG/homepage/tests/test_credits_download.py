import pytest
from django.shortcuts import reverse

@pytest.mark.django_db
def test_download_file_detected(client):
    response = client.get(reverse('credits_download'))
    check_attachment = "attachment" in response.headers['Content-Disposition']
    check_attachment_filename = "CREDITS.csv" in response.headers['Content-Disposition']
    check_content_len = int(response.headers['Content-Length']) > 4000000

    assert check_content_len and check_attachment and check_attachment_filename

@pytest.mark.django_db
def test_not_returning_homepage(client):
    # returning homepage in case of file errors
    response = client.get(reverse('credits_download'))
    assert response.status_code != 302

