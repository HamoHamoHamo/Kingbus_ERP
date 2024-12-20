from django.test import TestCase
from common.test_setting import AuthenticatedUserTestCase
from django.urls import reverse

from assignment.models import OldAssignment, OldAssignmentConnect
from dispatch.models import RegularlyGroup, DispatchRegularlyData, DispatchRegularly, DispatchRegularlyConnect, DispatchOrder, DispatchOrderConnect
from humanresource.models import Member
from vehicle.models import Vehicle
from common.constant import TODAY

# class YourTestClass(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         print("setUpTestData: Run once to set up non-modified data for all class methods.")
#         pass

#     def setUp(self):
#         print("setUp: Run once for every test method to setup clean data.")
#         pass

#     def test_false_is_false(self):
#         print("Method: test_false_is_false.")
#         self.assertFalse(False)

#     def test_false_is_true(self):
#         print("Method: test_false_is_true.")
#         self.assertTrue(False)

#     def test_one_plus_one_equals_two(self):
#         print("Method: test_one_plus_one_equals_two.")
#         self.assertEqual(1 + 1, 2)


class RegularlyEditCheckViewTest(AuthenticatedUserTestCase):

    DEPARTURE_DATE1 = f'{TODAY} 01:00'
    ARRIVAL_DATE1 = f'{TODAY} 08:00'
    DEPARTURE_DATE2 = f'{TODAY} 01:00'
    ARRIVAL_DATE2 = f'{TODAY} 08:00'
    DEPARTURE_DATE3 = f'{TODAY} 01:00'
    ARRIVAL_DATE3 = f'{TODAY} 08:00'

    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        
        cls.bus = Vehicle.objects.create()
        cls.member = Member.objects.create()
        # 그룹까지 생성해주기
        cls.group = RegularlyGroup.objects.create(settlement_date='01')

        cls.set_init_model()
        # order = DispatchOrder.objects.create(price=0, bus_cnt=1)
        # cls.order_connect = DispatchOrderConnect.objects.create(order_id=order, departure_date=cls.DEPARTURE_DATE2, arrival_date=cls.ARRIVAL_DATE2, bus_id=cls.bus, driver_id=cls.member)

        # assignment = Assignment.objects.create()
        # cls.assignment_connect = AssignmentConnect.objects.create(assignment_id=assignment, start_date=cls.DEPARTURE_DATE3, end_date=cls.ARRIVAL_DATE3, bus_id=cls.bus, member_id=cls.member)
        
        # no_bus_assignment = Assignment.objects.create(use_vehicle='미사용')
        # cls.no_bus_assignment_connect = AssignmentConnect.objects.create(assignment_id=no_bus_assignment, start_date=cls.DEPARTURE_DATE3, end_date=cls.ARRIVAL_DATE3, member_id=cls.member)
        # cls.set_view_type(cls.regularly_data.id, reverse('dispatch:regularly_route_edit_check'))

    @classmethod
    def set_init_model(cls):
        
        regularly_data = DispatchRegularlyData.objects.create(group=cls.group)
        regularly = DispatchRegularly.objects.create(group=cls.group, regularly_id=regularly_data)
        regularly_connect = DispatchRegularlyConnect.objects.create(regularly_id=regularly, departure_date=cls.DEPARTURE_DATE1, arrival_date=cls.ARRIVAL_DATE1, bus_id=cls.bus, driver_id=cls.member)

        cls.set_view_type(regularly_data.id, reverse('dispatch:regularly_route_edit_check'))

    @classmethod
    def set_view_type(cls, id, test_url):
        cls.test_id = id
        cls.test_url = test_url

        OVERLAP_DEPARTURE_TIME = '01:00'
        OVERLAP_ARRIVAL_TIME = '10:00'

        DEPARTURE_TIME = '09:00'
        ARRIVAL_TIME = '10:00'

        cls.false_data = {
            'id' : cls.test_id,
            'departure_date' : OVERLAP_DEPARTURE_TIME,
            'arrival_date' : OVERLAP_ARRIVAL_TIME,
        }

        cls.true_data = {
            'id' : cls.test_id,
            'departure_date' : DEPARTURE_TIME,
            'arrival_date' : ARRIVAL_TIME,
        }

    def setUp(self):
        super().setUp()
        
    # 출퇴근배차 중복인 경우 확인
    def test_regularly_edit_check_overlap_with_regularly(self):
        regularly_data = DispatchRegularlyData.objects.create(group=self.group)
        regularly = DispatchRegularly.objects.create(group=self.group, regularly_id=regularly_data)
        regularly_connect = DispatchRegularlyConnect.objects.create(regularly_id=regularly, departure_date=self.DEPARTURE_DATE1, arrival_date=self.ARRIVAL_DATE1, bus_id=self.bus, driver_id=self.member)

        response = self.client.post(self.test_url, self.false_data)
        json_data = response.json()
        self.assertEqual(json_data['status'], 'fail')
        regularly_data.delete()
        regularly.delete()
        regularly_connect.delete()

    # 일반배차 중복인 경우 확인
    def test_regularly_edit_check_overlap_with_order(self):
        order = DispatchOrder.objects.create(price=0, bus_cnt=1)
        order_connect = DispatchOrderConnect.objects.create(order_id=order, departure_date=self.DEPARTURE_DATE2, arrival_date=self.ARRIVAL_DATE2, bus_id=self.bus, driver_id=self.member)

        response = self.client.post(self.test_url, self.false_data)
        json_data = response.json()
        self.assertEqual(json_data['status'], 'fail')

        order.delete()
        order_connect.delete()

    # 업무배차 중복인 경우 확인
    def test_regularly_edit_check_overlap_with_assignment(self):
        assignment = OldAssignment.objects.create()
        assignment_connect = OldAssignmentConnect.objects.create(assignment_id=assignment, start_date=self.DEPARTURE_DATE3, end_date=self.ARRIVAL_DATE3, bus_id=self.bus, member_id=self.member)

        response = self.client.post(self.test_url, self.false_data)
        json_data = response.json()
        self.assertEqual(json_data['status'], 'fail')
        
        assignment.delete()
        assignment_connect.delete()

    # 업무배차(차량 미사용) 중복인 경우 확인
    def test_regularly_edit_check_overlap_with_assignment_no_bus(self):
        no_bus_assignment = OldAssignment.objects.create(use_vehicle='미사용')
        no_bus_assignment_connect = OldAssignmentConnect.objects.create(assignment_id=no_bus_assignment, start_date=self.DEPARTURE_DATE3, end_date=self.ARRIVAL_DATE3, member_id=self.member)

        response = self.client.post(self.test_url, self.false_data)
        json_data = response.json()
        self.assertEqual(json_data['status'], 'fail')

        no_bus_assignment.delete()
        no_bus_assignment_connect.delete()

    
     # 출퇴근배차 edit_check 통과하는 경우 확인
    def test_regularly_edit_check_pass_with_regularly(self):
        regularly_data = DispatchRegularlyData.objects.create(group=self.group)
        regularly = DispatchRegularly.objects.create(group=self.group, regularly_id=regularly_data)
        regularly_connect = DispatchRegularlyConnect.objects.create(regularly_id=regularly, departure_date=self.DEPARTURE_DATE1, arrival_date=self.ARRIVAL_DATE1, bus_id=self.bus, driver_id=self.member)

        response = self.client.post(self.test_url, self.true_data)
        json_data = response.json()
        self.assertEqual(json_data['status'], 'success')
        regularly_data.delete()
        regularly.delete()
        regularly_connect.delete()

    # 일반배차 edit_check 통과하는 경우 확인
    def test_regularly_edit_check_pass_with_order(self):
        order = DispatchOrder.objects.create(price=0, bus_cnt=1)
        order_connect = DispatchOrderConnect.objects.create(order_id=order, departure_date=self.DEPARTURE_DATE2, arrival_date=self.ARRIVAL_DATE2, bus_id=self.bus, driver_id=self.member)

        response = self.client.post(self.test_url, self.true_data)
        json_data = response.json()
        self.assertEqual(json_data['status'], 'success')

        order.delete()
        order_connect.delete()

    # 업무배차 edit_check 통과하는 경우 확인
    def test_regularly_edit_check_pass_with_assignment(self):
        assignment = OldAssignment.objects.create()
        assignment_connect = OldAssignmentConnect.objects.create(assignment_id=assignment, start_date=self.DEPARTURE_DATE3, end_date=self.ARRIVAL_DATE3, bus_id=self.bus, member_id=self.member)

        response = self.client.post(self.test_url, self.true_data)
        json_data = response.json()
        self.assertEqual(json_data['status'], 'success')
        
        assignment.delete()
        assignment_connect.delete()

    # 업무배차(차량 미사용) edit_check 통과하는 경우 확인
    def test_regularly_edit_check_pass_with_assignment_no_bus(self):
        no_bus_assignment = OldAssignment.objects.create(use_vehicle='미사용')
        no_bus_assignment_connect = OldAssignmentConnect.objects.create(assignment_id=no_bus_assignment, start_date=self.DEPARTURE_DATE3, end_date=self.ARRIVAL_DATE3, member_id=self.member)

        response = self.client.post(self.test_url, self.true_data)
        json_data = response.json()
        self.assertEqual(json_data['status'], 'success')

        no_bus_assignment.delete()
        no_bus_assignment_connect.delete()


class OrderEditCheckViewTest(RegularlyEditCheckViewTest):
    @classmethod
    def set_init_model(cls):
        order = DispatchOrder.objects.create(price=0, bus_cnt=1)
        order_connect = DispatchOrderConnect.objects.create(order_id=order, departure_date=cls.DEPARTURE_DATE1, arrival_date=cls.ARRIVAL_DATE1, bus_id=cls.bus, driver_id=cls.member)

        cls.set_view_type(order.id, reverse('dispatch:order_edit_check'))

    @classmethod
    def set_view_type(cls, id, test_url):
        cls.test_id = id
        cls.test_url = test_url

        OVERLAP_DEPARTURE_TIME = f'{TODAY} 01:00'
        OVERLAP_ARRIVAL_TIME = f'{TODAY} 10:00'

        DEPARTURE_TIME = f'{TODAY} 09:00'
        ARRIVAL_TIME = f'{TODAY} 10:00'

        cls.false_data = {
            'id' : cls.test_id,
            'departure_date' : OVERLAP_DEPARTURE_TIME,
            'arrival_date' : OVERLAP_ARRIVAL_TIME,
        }

        cls.true_data = {
            'id' : cls.test_id,
            'departure_date' : DEPARTURE_TIME,
            'arrival_date' : ARRIVAL_TIME,
        }