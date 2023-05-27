import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from django.urls import reverse
from students.models import Course, Student
from pprint import pprint



@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return baker.make(Course, **kwargs)

    return factory

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_get_course(api_client, course_factory):
    course = course_factory(_quantity=10)

    resp = api_client.get('/courses/')

    assert resp.status_code == 200

    resp = resp.json()

    assert resp[0]['id'] == course[0].id


@pytest.mark.django_db
def test_get_courses(api_client, course_factory):
    course = course_factory(_quantity=100)

    resp = api_client.get(f'/courses/{course[0].id}/')

    assert resp.status_code == 200

    resp = resp.json()
    assert resp['id'] == course[0].id


@pytest.mark.django_db
def test_filter_by_id(api_client, course_factory):
    course = course_factory(_quantity=100)

    resp = api_client.get(f'/courses/{course[0].id}/')

    assert resp.status_code == 200

    resp = resp.json()
    assert course[0].id == resp['id']


@pytest.mark.django_db
def test_filter_by_name(api_client, course_factory):
    course = course_factory(_quantity=100)

    f = {
        "name": course[0].name,
        }

    resp = api_client.get(f'/courses/?filter={f}/')

    assert resp.status_code == 200

    resp = resp.json()

    assert course[0].name == resp[0]['name']



@pytest.mark.django_db
def test_post_course(api_client):
    count = Course.objects.count()

    response = api_client.post('/courses/', data={'name': 'asd'})

    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_patch_course(api_client, course_factory):
    course = course_factory(_quantity=1)

    response = api_client.patch(f'/courses/{course[0].id}/', {'name': 'asd'}, format='json')

    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    course = course_factory(_quantity=1)
    count = Course.objects.count()

    response = api_client.delete(f'/courses/{course[0].id}/')

    assert response.status_code == 200 or response.status_code == 204
    assert Course.objects.count() == count - 1