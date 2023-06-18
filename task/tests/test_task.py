import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from task.models import Task, SubTask

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data(api_client):
    user_data = {
        'email': 'tests@example.com',
        'password': 'password1234!',
        'username': 'tests',
        'team': 'Danbi',
    }
    user = User.objects.create_user(**user_data)
    response = api_client.post(reverse('login'), {
        'email': user_data['email'],
        'password': user_data['password'],
    }, format='json')

    return {
        'data': user,
        'team': user_data['team'],
        'access_token': response.data['token']['access_token']
    }


@pytest.fixture
def task_and_payload():
    return {
        'team': [],
        'title': '연필 만들기',
        'content': '각 팀에 일을 분배',
        'subtasks': [
            {
                'title': '흑연 가공',
                'content': '좋은 품질의 흑연을 가공',
                'team': [
                    'Danbi',
                    'Chullo'
                ]
            },
            {
                'title': '나무 가공',
                'content': '좋은 목재를 가공',
                'team': [
                    'Sufi'
                ]
            },
        ]
    }


@pytest.fixture
def create_task_with_subtasks(user_data, task_and_payload):
    task_data = {
        'create_user': user_data['data'],
        'team': [user_data['team']],
        'title': '연필 만들기',
        'content': '각 팀에 일을 분배',
    }
    task = Task.objects.create(**task_data)

    subtasks_payload = task_and_payload['subtasks']
    for subtask_payload in subtasks_payload:
        subtask_data = {
            'task': task,
            'title': subtask_payload['title'],
            'content': subtask_payload['content'],
            'team': subtask_payload['team'],
        }
        SubTask.objects.create(**subtask_data)

    return {
        'user_data': user_data,
        'task': task
    }


def test_create_task_and_subtask(api_client, user_data, task_and_payload):
    '''
        Task와 Subtask 생성
    '''
    user = user_data['data']
    user_team = user_data['team']
    access_token = f'Bearer {user_data["access_token"]}'
    api_client.credentials(HTTP_AUTHORIZATION=access_token)

    url = reverse('task-list')
    response = api_client.post(url, task_and_payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    task = Task.objects.get(id=response.data['id'])
    assert task.create_user == user
    assert task.team == [user_team]
    assert task.title == '연필 만들기'

    subtasks = task.subtasks.all()
    assert len(subtasks) == 2

    subtask1 = subtasks[0]
    assert subtask1.title == '흑연 가공'
    assert subtask1.content == '좋은 품질의 흑연을 가공'
    assert subtask1.team == ['Danbi', 'Chullo']

    subtask2 = subtasks[1]
    assert subtask2.title == '나무 가공'
    assert subtask2.content == '좋은 목재를 가공'
    assert subtask2.team == ['Sufi']


def test_put_task_and_subtask(api_client, task_and_payload, create_task_with_subtasks):
    '''
        Task와 SubTask 수정
    '''
    user_data = create_task_with_subtasks['user_data']
    task = create_task_with_subtasks['task']

    access_token = f'Bearer {user_data["access_token"]}'
    api_client.credentials(HTTP_AUTHORIZATION=access_token)

    task_and_payload['team'].append(user_data['team'])
    task_and_payload['content'] = '좋은 연필 만들기'
    task_and_payload['subtasks'][1]['team'].append('Ttangi')

    url = reverse('task-detail', kwargs={'pk': task.id})
    response = api_client.put(url, task_and_payload, format='json')
    assert response.status_code == status.HTTP_200_OK

    task.refresh_from_db()
    assert task.team == response.data['team']
    assert task.content == response.data['content']

    subtasks = task.subtasks.all()
    for i, subtask in enumerate(subtasks):
        subtask.refresh_from_db()
        assert subtask.team == response.data['subtasks'][i]['team']


def test_get_task_and_subtask(api_client, create_task_with_subtasks):
    '''
        Task 조회.
    '''
    user_data = create_task_with_subtasks['user_data']
    task = create_task_with_subtasks['task']
    access_token = f'Bearer {user_data["access_token"]}'
    api_client.credentials(HTTP_AUTHORIZATION=access_token)

    url = reverse('task-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    task_data = response.data[0]
    assert task_data['id'] == task.id
    assert task_data['title'] == task.title
    assert task_data['content'] == task.content

    if 'subtasks' in task_data:
        for subtask_data in task_data['subtasks']:
            subtask = SubTask.objects.get(id=subtask_data['id'])
            assert subtask_data['id'] == subtask.id
            assert subtask_data['title'] == subtask.title
            assert subtask_data['content'] == subtask.content


def test_update_subtask(api_client, create_task_with_subtasks):
    '''
        SubTask.is_complete 수정
    '''
    user_data = create_task_with_subtasks['user_data']
    task = create_task_with_subtasks['task']
    subtask = task.subtasks.first()

    access_token = f'Bearer {user_data["access_token"]}'
    api_client.credentials(HTTP_AUTHORIZATION=access_token)

    url = reverse('subtask-detail', kwargs={'id': subtask.id})
    data = {
        'is_complete': True
    }
    response = api_client.patch(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK

    subtask.refresh_from_db()
    assert subtask.is_complete is True


def test_delete_subtask(api_client, create_task_with_subtasks):
    '''
        SubTask 삭제
    '''
    user_data = create_task_with_subtasks['user_data']
    task = create_task_with_subtasks['task']
    subtask = task.subtasks.first()

    access_token = f'Bearer {user_data["access_token"]}'
    api_client.credentials(HTTP_AUTHORIZATION=access_token)

    url = reverse('subtask-detail', kwargs={'id': subtask.id})
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data['message'] == 'Subtask has been deleted.'
