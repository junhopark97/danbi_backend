import jwt
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from danbi.settings import SECRET_KEY

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_info():
    return {
        'email': 'test@example.com',
        'password': 'password1234!',
        'password2': 'password1234!',
        'username': 'test',
        'team': 'Danbi',
    }


def test_create_user_success(api_client, user_info):
    response = api_client.post(reverse('register'), user_info, format='json')
    user_data = response.data['data']
    assert response.status_code == status.HTTP_201_CREATED
    assert user_data['email'] == user_info['email']
    assert 'password' not in response.data
    assert response.data['message'] == 'Member registration success'


def test_create_user(user_info):
    '''
    직접적으로 USER 생성
    '''
    password2 = user_info.pop('password2', None)
    user = User.objects.create_user(**user_info)
    assert user.email == user_info['email']
    assert user.check_password(user_info['password'])
    assert user.username == user_info['username']
    assert user.team == user_info['team']
    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.parametrize(
    ('email', 'pw', 'pw2', 'username', 'team',),
    (
        ('test@example.com', 'password', 'password', 'Kimcoding', 'Danbi',),
        ('test@example.com', 'password', 'password1234!', 'Minsu', 'Blabla',),
        ('test', 'password1234!', 'password1234!', 'Jaemin', 'test'),
    ),
)
def test_create_user_fail(api_client, email, pw, pw2, username, team):
    response = api_client.post(reverse('register'), {
        'email': email,
        'password': pw,
        'password2': pw2,
        'username': username,
        'team': team,
    }, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_success(api_client, user_info):
    password2 = user_info.pop('password2', None)
    user = User.objects.create_user(**user_info)
    response = api_client.post(reverse('login'), {
        'email': user_info['email'],
        'password': user_info['password'],
    }, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'access_token' in response.data['token']
    assert 'refresh_token' in response.data['token']

    access = response.data['token']['access_token']
    verify_access = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
    refresh = response.data['token']['refresh_token']
    verify_refresh = jwt.decode(refresh, SECRET_KEY, algorithms=['HS256'])

    assert verify_access.get('user_id') == user.id
    assert verify_refresh.get('user_id') == user.id


@pytest.mark.parametrize(
    ('email', 'password'),
    [
        pytest.param('test@example.com', 'password'),
        pytest.param('test1@example.com', 'password1234!'),
    ],
)
def test_login_fail(api_client, user_info, email, password):
    password2 = user_info.pop('password2', None)
    User.objects.create_user(**user_info)
    response = api_client.post(reverse('login'), {
        'email': email,
        'password': password,
    }, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'token' not in response.data


# def test_logout_success(api_client, jwt_token):
#     api_client.cookies['jwt'] = jwt_token
#     response = api_client.post(reverse('logout'), format='json')
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data['message'] == 'Logout Successful'
#
#
# def test_logout_fail(api_client):
#     response = api_client.post(reverse('logout'), format='json')
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
