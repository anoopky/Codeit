from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from .models import Questions, Result, TestCases
from django.core.urlresolvers import reverse


class CodeItTest(TestCase):
    def setUp(self):
        self.question = Questions.objects.create(title="Even or odd?", description="test_description",
                                                 input_public="1", output_public="odd", explanation="test_explanation"
                                                 , verification="1")

        self.test1 = TestCases.objects.create(questionId=self.question, input_private="2",
                                              output_private="even")
        self.test2 = TestCases.objects.create(questionId=self.question, input_private="23",
                                              output_private="odd")

        User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        User.objects.create_superuser('temporary1', 'temporary1@gmail.com', 'temporary1')

    def question_create_test(self):
        now = timezone.now()
        self.assertLess(self.question.created_at, now)

    def TestCases_create_test(self):
        now = timezone.now()
        self.assertLess(self.test1.created_at, now)

    def test_logout(self):
        self.client.login(username='temporary', password='temporary')
        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(resp.status_code, 200)
        self.client.get(reverse('logout'))
        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(resp.status_code, 302)

    def test_student_view(self):
        self.client.login(username='temporary', password='temporary')
        resp = self.client.get(reverse('dashboard'))
        resp1 = self.client.get(reverse('result'))
        resp2 = self.client.get(reverse('questions', args=str(self.question.id)))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

    def test_dashboard_non_login_view(self):
        resp = self.client.get(reverse('dashboard'))
        resp1 = self.client.get(reverse('add_question'))
        resp2 = self.client.get(reverse('result'))
        resp3 = self.client.get(reverse('questions', args=str(self.question.id)))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp1.status_code, 302)
        self.assertEqual(resp2.status_code, 302)
        self.assertEqual(resp3.status_code, 302)

    def test_dashboard_staff_redirect_view(self):
        self.client.login(username='temporary1', password='temporary1')
        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(resp.status_code, 302)

    def test_dashboard_staff_add_question_view(self):
        self.client.login(username='temporary1', password='temporary1')
        resp = self.client.get(reverse('add_question'))
        self.assertEqual(resp.status_code, 200)

    def test_debug_code(self):
        self.client.login(username='temporary', password='temporary')
        resp = self.client.post('/compileTest',
                                {'id': str(self.question.id), 'lang': 'Python',
                                 'code': 'x = int(input())\nif x%2 == 0:\n\tprint("even")\nelse:\n\tprint("odd")',
                                 'custom': '0'})
        self.assertContains(resp, self.question.output_public, 2, 200)

    def test_submit_code(self):
        self.client.login(username='temporary', password='temporary')
        resp = self.client.post('/compile',
                                {'id': str(self.question.id), 'lang': 'Python',
                                 'code': 'x = int(input())\nif x%2 == 0:\n\tprint("even")\nelse:\n\tprint("odd")'})
        self.assertContains(resp, "1", 2, 200)

