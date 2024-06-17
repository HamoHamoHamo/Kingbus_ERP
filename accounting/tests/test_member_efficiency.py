from django.db.models.query import QuerySet
from django.test import TestCase
from django.urls import reverse
from datetime import datetime, timedelta, date
from unittest.mock import patch
from humanresource.models import Member
from accounting.views import MemberEfficiencyList

class MemberEfficiencyListTestCase(TestCase):
    def setUp(self):
        # 테스트에 필요한 데이터 설정
        self.member = Member.objects.create(name='John', authority=2, use='사용')
        self.client.defaults['HTTP_USER_AGENT'] = 'Test'
        self.today = date.today()
        self.last_month = self.today.replace(day=1) - timedelta(days=1)
        self.url = reverse('accounting:member_efficiency')

    # def test_member_efficiency_list_view(self):
    #     # 로그인되지 않은 경우 권한 오류 테스트
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'authority.html')

    #     # 세션에 권한 부여
    #     self.client.session['authority'] = 2

    #     # 멤버 리스트 페이지 접속 테스트
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'accounting/member_efficiency.html')

    #     # 템플릿에서 반환된 컨텍스트 데이터 테스트
    #     self.assertIn('member_list', response.context)
    #     self.assertIn('date1', response.context)
    #     self.assertIn('date2', response.context)
    #     self.assertIn('date_type', response.context)
    #     self.assertIn('data_list', response.context)
    #     self.assertIn('total_data', response.context)
    #     self.assertIn('person_avg_data', response.context)

    # @patch('myapp.views.calculate_date_difference')
    # @patch('myapp.views.get_hour_minute')
    # def test_get_queryset(self, mock_get_hour_minute, mock_calculate_date_difference):
    def test_get_queryset(self):
        # get_queryset 메서드 테스트
        view = MemberEfficiencyList()
        queryset = view.get_queryset()

        # 필터링된 멤버 리스트 반환 확인
        self.assertIsInstance(queryset, QuerySet)
        self.assertEqual(queryset.count(), 1)

    def test_calculate_avg_data(self):
        # calculate_avg_data 메서드 테스트
        view = MemberEfficiencyList()

        total_data = {
            'salary': 10000,
            'price': 5000,
            'driving_cnt': 10,
            'distance': 200,
            'driving_distance': 150,
            'minutes': 300,
            'driving_minutes': 200,
            'fuel_cost': 300,
            'driving_fuel_cost': 200,
            'tolerance_distance': 50,
            'tolerance_time': 60,
        }
        divisor = 5  # 테스트용 divisor 설정

        avg_data = view.get_avg_data(total_data, divisor)

        # 각 필드의 평균값 확인
        self.assertEqual(avg_data['salary'], 2000)
        self.assertEqual(avg_data['price'], 1000)
        self.assertEqual(avg_data['driving_cnt'], 2)
        self.assertEqual(avg_data['distance'], 40)
        self.assertEqual(avg_data['driving_distance'], 30)
        self.assertEqual(avg_data['minutes'], 60)
        self.assertEqual(avg_data['driving_minutes'], 40)
        self.assertEqual(avg_data['fuel_cost'], 60)
        self.assertEqual(avg_data['driving_fuel_cost'], 40)
        self.assertEqual(avg_data['tolerance_distance'], 10)
        self.assertEqual(avg_data['tolerance_time'], 12)
