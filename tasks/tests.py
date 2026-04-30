from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskViewsTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='pass12345')
        self.other_user = User.objects.create_user(username='other', password='pass12345')
        self.task = Task.objects.create(
            title='Owner task',
            description='Visible only to owner',
            owner=self.owner,
            status=Task.Status.TODO,
            priority=Task.Priority.HIGH,
        )
        Task.objects.create(
            title='Other task',
            description='Hidden from owner',
            owner=self.other_user,
            status=Task.Status.DONE,
            priority=Task.Priority.LOW,
        )

    def test_list_requires_login(self):
        response = self.client.get(reverse('task_list'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_list_shows_only_current_user_tasks(self):
        self.client.login(username='owner', password='pass12345')

        response = self.client.get(reverse('task_list'))

        self.assertContains(response, 'Owner task')
        self.assertNotContains(response, 'Other task')

    def test_list_filters_by_status_and_priority(self):
        self.client.login(username='owner', password='pass12345')
        Task.objects.create(
            title='Done task',
            owner=self.owner,
            status=Task.Status.DONE,
            priority=Task.Priority.LOW,
        )

        response = self.client.get(reverse('task_list'), {'status': Task.Status.DONE, 'priority': Task.Priority.LOW})

        self.assertContains(response, 'Done task')
        self.assertNotContains(response, 'Owner task')

    def test_create_task_sets_owner_automatically(self):
        self.client.login(username='owner', password='pass12345')

        response = self.client.post(reverse('task_create'), {
            'title': 'New task',
            'description': 'Created from form',
            'status': Task.Status.IN_PROGRESS,
            'priority': Task.Priority.MEDIUM,
        })

        self.assertRedirects(response, reverse('task_list'))
        task = Task.objects.get(title='New task')
        self.assertEqual(task.owner, self.owner)

    def test_owner_can_update_task(self):
        self.client.login(username='owner', password='pass12345')

        response = self.client.post(reverse('task_edit', args=[self.task.id]), {
            'title': 'Updated task',
            'description': self.task.description,
            'status': Task.Status.DONE,
            'priority': Task.Priority.MEDIUM,
        })

        self.assertRedirects(response, reverse('task_list'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated task')

    def test_other_user_cannot_update_task(self):
        self.client.login(username='other', password='pass12345')

        response = self.client.get(reverse('task_edit', args=[self.task.id]))

        self.assertEqual(response.status_code, 403)

    def test_owner_can_delete_task(self):
        self.client.login(username='owner', password='pass12345')

        response = self.client.post(reverse('task_delete', args=[self.task.id]))

        self.assertRedirects(response, reverse('task_list'))
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

# Create your tests here.
