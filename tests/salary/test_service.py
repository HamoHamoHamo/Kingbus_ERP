import pytest
from django.urls import reverse

def test_salary_table_view(authorized_client):
    url = reverse("salary:table3")

    assert authorized_client.session['name'] == 'admin'
