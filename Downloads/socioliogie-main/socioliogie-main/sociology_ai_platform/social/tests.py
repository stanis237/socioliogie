from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Comment, Notification

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='This is a test post content.'
        )

    def test_post_creation(self):
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'This is a test post content.')

    def test_post_str(self):
        self.assertEqual(str(self.post), 'Test Post')

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='This is a test post content.'
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='This is a test comment.'
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.content, 'This is a test comment.')

    def test_comment_str(self):
        self.assertEqual(str(self.comment), f"Comment by {self.user.username}")

class NotificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.notification = Notification.objects.create(
            user=self.user,
            message='You have a new message.',
            is_read=False
        )

    def test_notification_creation(self):
        self.assertEqual(self.notification.user, self.user)
        self.assertEqual(self.notification.message, 'You have a new message.')
        self.assertFalse(self.notification.is_read)

    def test_notification_str(self):
        self.assertEqual(str(self.notification), f"Notification for {self.user.username}")
