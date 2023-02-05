from socialnetwork.models import UserProfile, UserPost
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


# Create your tests here.

class LoginTestCase(TestCase):
    """
    test case to log in user
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('johndoe', 'john@doe.com', 'John@123')

    def test_login(self):
        response = self.client.post(reverse('login'), data={
            'username': 'johndoe',
            'password': 'John@123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')


class SignupTestCase(TestCase):
    """
    test case to sign up a user
    """

    def setUp(self):
        self.client = Client()

    def test_signup(self):
        response = self.client.post(reverse('signup'), data={
            'username': 'johndoe',
            'email': 'john@doe.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'John@123',
            'password2': 'John@123'
        })
        self.assertEqual(response.status_code, 302)


class CreatePostTestCase(TestCase):
    """
    test case to create a post
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('johndoe', 'john@doe.com', 'John@123')
        self.userprofile = UserProfile.objects.create(user=self.user, status="Hey! This is my new status",
                                                      profile_visibility=False)

    def test_create_a_post(self):
        self.client.post(reverse('login'), data={
            'username': 'johndoe',
            'password': 'John@123',
        })

        response = self.client.post(reverse('home'), data={
            'text': 'This is a test post from the test case!'
        })

        self.assertEqual(response.status_code, 200)


class UpdateUserProfile(TestCase):
    """
    test case to update a user profile
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('johndoe', 'john@doe.com', 'John@123')
        self.userprofile = UserProfile.objects.create(user=self.user, status="Hey! This is my old status",
                                                      profile_visibility=False)

    def test_update_user_profile(self):
        self.client.post(reverse('login'), data={
            'username': 'johndoe',
            'password': 'John@123',
        })

        response = self.client.post(reverse('profile-edit'), data={
            'status': 'Hello Everyone. This is my very new status!',
            'profile_visibility': True
        })

        self.assertEqual(response.status_code, 200)


class UserSearchTestCase(TestCase):
    """
    test case to search a user
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('johndoe', 'john@doe.com', 'John@123')
        self.user = User.objects.create_user('janedoe', 'jane@doe.com', 'Jane@123')

    def test_search_user(self):
        self.client.post(reverse('login'), data={
            'username': 'johndoe',
            'password': 'John@123',
        })

        response = self.client.get(reverse('user-search'), {'query': 'jane'})
        self.assertEqual(response.status_code, 200)


class UserProfileTestCase(TestCase):
    """
    test case to view a user profile
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('johndoe', 'john@doe.com', 'John@123')
        self.userprofile = UserProfile.objects.create(user=self.user, status="Hey! This is my new status",
                                                      profile_visibility=False)

    def test_profile_user(self):
        self.client.post(reverse('login'), data={
            'username': 'johndoe',
            'password': 'John@123',
        })

        response = self.client.get(reverse('profile', kwargs={'username': 'johndoe'}))
        self.assertEqual(response.status_code, 200)
