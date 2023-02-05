from django.contrib.auth.models import User
from socialnetwork.models import UserProfile, UserPost
from api.model_factories import UserFactory, UserProfileFactory, UserPostFactory
from rest_framework.test import APITestCase
from django.urls import reverse


# Create your tests here.

class GetUserTest(APITestCase):
    """
    Test module for /user/<username> GET request
    """

    def setUp(self):
        self.user_profile = UserProfileFactory.create()
        self.good_url = reverse('api:profile_api', kwargs={'user__username': self.user_profile.user.username})
        self.bad_url = "/something/random"

    def tearDown(self):
        UserProfile.objects.all().delete()
        User.objects.all().delete()

    def test_user_profile_good(self):
        """
        Test for a status code 200 to ensure a valid request is made to user/<str:username>.
        """
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)

    def test_user_profile_bad(self):
        """
        Test for a status code 404 to ensure an invalid request is made when using the bad url.
        """
        response = self.client.get(self.bad_url, format='json')

        self.assertEqual(response.status_code, 404)


class GetAllUsersTest(APITestCase):
    """
    Test module for /profiles GET request
    """

    def setUp(self):
        # Create user
        self.user_1 = UserProfileFactory.create()
        self.user_2 = UserFactory.create(username='janedoe', first_name='Jane', last_name='Doe')
        self.userprofile2 = UserProfileFactory.create(user=self.user_2, status="Hey! I am new here!",
                                                      profile_visibility=True)

        # Set urls
        self.good_url = reverse('api:user_list_api')
        self.bad_url = "/something/random"

    def tearDown(self):
        UserProfile.objects.all().delete()
        User.objects.all().delete()

    def test_user_profiles_good(self):
        """
        Test for a status code 200 to ensure a valid request is made to users/.
        """
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)

    def test_user_profiles_bad(self):
        """
        Test for a status code 404 to ensure an invalid request is made when using a bad url.
        """
        response = self.client.get(self.bad_url, format='json')
        self.assertEqual(response.status_code, 404)


class GetUserPostTest(APITestCase):
    """
    Test module for /posts/<str:username> GET request
    """

    def setUp(self):
        self.user = UserFactory.create(username='tim', first_name='Tim', last_name='Doe')
        self.user_profile = UserProfileFactory.create(user=self.user)
        self.good_url = reverse('api:posts_api', kwargs={'user__username': self.user_profile.user.username})
        self.user_posts = UserPostFactory.create(author=self.user)
        self.bad_url = "/something/random"

    def tearDown(self):
        UserProfile.objects.all().delete()
        User.objects.all().delete()
        UserPost.objects.all().delete()

    def test_user_post_good(self):
        """
        Test for a status code 200 to ensure a valid request is made to posts/<str:username>.
        """
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)

    def test_user_post_bad(self):
        """
        Test for a status code 404 to ensure an invalid request is made when using the bad url.
        """
        response = self.client.get(self.bad_url, format='json')

        self.assertEqual(response.status_code, 404)
