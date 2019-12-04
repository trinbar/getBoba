from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@gmail.com',
            password = 'testpassword23'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='gimmeboba123',
            name='Test user full name'
        )

    def test_users_listed(self):
        """Tests that users are listed on user page"""
        url = reverse('admin:core_user_changelist')  # generates url for list user page
        res = self.client.get(url) # uses test client to perform HTTP GET on url

        # check for status code 200 and checks content
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        # reverse fn creates a url like this: /admin/core/user/id
        # anything that gets passed in args is assigned to user
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, 200)

