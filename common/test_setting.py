from django.test import TestCase

from humanresource.models import Member

class AuthenticatedUserTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_member = Member.objects.create(authority=0, name='test', id=1)

    def set_session(self):
        session = self.client.session
        session['user'] = self.test_member.id
        session['name'] = self.test_member.name
        session['authority'] = self.test_member.authority
        session.save()

    def setUp(self):
        self.set_session()
        print("\n----------------------------test start----------------------------")
