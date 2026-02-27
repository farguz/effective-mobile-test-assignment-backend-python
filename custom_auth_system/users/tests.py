import pytest
from django.urls import reverse

from custom_auth_system.users.models import CustomUser


@pytest.mark.django_db
class TestUserAuth:
    
    @pytest.fixture
    def user_data(self):
        return {
            'email': 'test@gmail.com',
            'password': 'test@gmail.comtest@gmail.com',
            'first_name': 'Ivan',
            'middle_name': 'Ivanovich',
            'last_name': 'Ivanov'
        }

    @pytest.fixture
    def active_user(self, user_data):
        return CustomUser.objects.create_user(**user_data)

    @pytest.fixture
    def inactive_user(self, user_data):
        user_data['email'] = 'inactive@gmail.com'
        user = CustomUser.objects.create_user(**user_data)
        user.is_active = False
        user.save()
        return user

    def test_create_user(self, active_user):
        assert active_user.email == 'test@gmail.com'
        assert active_user.is_active is True

    def test_login_success(self, client, active_user, user_data):
        url = reverse('login')
        response = client.post(url, {
            'email': user_data['email'],
            'password': user_data['password']
        })
        
        assert response.status_code == 302
        assert response.url == reverse('index_page')
        assert 'access_token' in client.cookies
        assert 'refresh_token' in client.cookies

    def test_login_inactive_user(self, client, inactive_user, user_data):
        url = reverse('login')
        response = client.post(url, {
            'email': inactive_user.email,
            'password': user_data['password']
        })
        
        assert response.status_code == 200
        assert 'has been deleted' in response.content.decode('utf-8')
        assert 'access_token' not in client.cookies

    def test_login_invalid_password(self, client, active_user):
        url = reverse('login')
        response = client.post(url, {
            'email': active_user.email,
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 200
        assert 'Invalid credentials' in response.content.decode('utf-8')