from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from friendship.models import Friend, FriendshipRequest
from users.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import base64

User = get_user_model()

class FriendTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.user3 = User.objects.create_user(username='user3', password='password3')

    def test_add_friend(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('users:add_friend', args=[self.user2.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(FriendshipRequest.objects.filter(from_user=self.user1, to_user=self.user2).exists())

    def test_accept_friend_request(self):
        Friend.objects.add_friend(self.user1, self.user2)
        friend_request = FriendshipRequest.objects.get(from_user=self.user1, to_user=self.user2)
        self.client.login(username='user2', password='password2')
        response = self.client.get(reverse('users:accept_friend_request', args=[friend_request.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Friend.objects.are_friends(self.user1, self.user2))

    def test_reject_friend_request(self):
        Friend.objects.add_friend(self.user1, self.user2)
        friend_request = FriendshipRequest.objects.get(from_user=self.user1, to_user=self.user2)
        self.client.login(username='user2', password='password2')
        response = self.client.get(reverse('users:reject_friend_request', args=[friend_request.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(FriendshipRequest.objects.filter(id=friend_request.id).exists())

    def test_view_friends(self):
        Friend.objects.add_friend(self.user1, self.user2)
        friend_request = FriendshipRequest.objects.get(from_user=self.user1, to_user=self.user2)
        friend_request.accept()
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('users:view_friends'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user2.username)

    def test_view_friend_requests(self):
        Friend.objects.add_friend(self.user1, self.user2)
        self.client.login(username='user2', password='password2')
        response = self.client.get(reverse('users:view_friend_requests'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.username)

    def test_search_friends(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('users:search_friends'), {'q': 'user2'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user2.username)


class ProfileTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

    def test_view_profile(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('users:profile', args=[self.user1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.username)

    def test_edit_profile(self):
        self.client.login(username='user1', password='password1')
        response = self.client.post(reverse('users:profile', args=[self.user1.id]), {
            'username': 'user1',
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName',
            'email': 'newemail@example.com',
        })
        self.assertEqual(response.status_code, 302)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, 'NewFirstName')
        self.assertEqual(self.user1.last_name, 'NewLastName')
        self.assertEqual(self.user1.email, 'newemail@example.com')

    def test_save_cropped_image(self):
        self.client.login(username='user1', password='password1')
        image_data = base64.b64encode(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01').decode()
        response = self.client.post(reverse('users:save_cropped_image'), {
            'image': f'data:image/png;base64,{image_data}'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.json())
        self.assertEqual(response.json()['status'], 'success')
        self.user1.refresh_from_db()
        self.assertTrue(self.user1.image)

