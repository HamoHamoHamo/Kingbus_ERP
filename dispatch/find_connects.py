import asyncio
import aiohttp
from django.shortcuts import render
from datetime import datetime, timedelta
from django.core.exceptions import BadRequest
from functools import partial
from asgiref.sync import sync_to_async
from .models import *
from my_settings import KAKAO_KEY
import json
from config.custom_logging import logger

def get_station_type(data):
    if data.work_type == "출근":
        departure_type = "첫 정류장 대기장소"
        arrival_type = "사업장"
    else:
        departure_type = "사업장"
        arrival_type = "마지막 정류장"
    return departure_type, arrival_type

def get_time_in_minutes(time_str):
    """시간 문자열(HH:MM)을 분으로 변환"""
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def format_departure_time(base_date, time_str):
    """기준 날짜와 HH:MM 형식의 시간을 카카오 API용 포맷(YYYYMMDDHHmm)으로 변환"""
    hours, minutes = map(int, time_str.split(':'))
    time_obj = datetime.strptime(base_date, "%Y%m%d").replace(hour=hours, minute=minutes)
    return time_obj.strftime("%Y%m%d%H%M")

async def async_get_distance_and_time_from_kakao(session, origin, destination, departure_time, test_data, departure_station, arrival_station, retry_count=3):
    if origin == destination:
        return 0, 0, {'error': '출발지와 도착지가 동일합니다.'}
    
    #  이미 계산된 데이터가 있는지 확인
    get_empty_run_data = sync_to_async(lambda: EmptyRunTimeCalculation.objects.filter(
        regulalry_data_station_id=arrival_station['station__id'],
        arrival_data_station_id=departure_station['station__id']
    ).last())
    
    empty_run_data = await get_empty_run_data()
    
    if empty_run_data:
        # logger.info(f"이미 계산된 데이터가 있습니다. Test Data ID: {test_data.id} empty_data id: {empty_run_data.id}")
        return int(empty_run_data.distance), get_minutes_from_formatted_duration(empty_run_data.duration) * 60, {'error': '이미 계산된 데이터가 있습니다.'}

    
    """비동기 카카오 API 호출 함수"""
    
    api_url = 'https://apis-navi.kakaomobility.com/v1/directions'
    # api_url = 'https://apis-navi.kakaomobility.com/v1/future/directions'
    headers = {
        'Authorization': f"KakaoAK {KAKAO_KEY}"
    }

    for attempt in range(retry_count):
        try:
            async with session.get(api_url, params={
                'departure_time': departure_time,
                'origin': origin,
                'destination': destination,
                'car_type': 3
            }, headers=headers, timeout=30) as response:
                data = await response.json()
                
                if response.status == 200:
                    if data['routes'][0]['result_code'] == 104:
                        logger.warning(f"출발지와 도착지가 5m 이내 - Origin: {origin} > Destination: {destination}")
                        return 0, 0, data
                    try:
                        distance = data['routes'][0]['summary']['distance']
                        duration = data['routes'][0]['summary']['duration']
                        logger.info("API 호출 성공")
                        return distance, duration, data
                    except Exception as e:
                        logger.error(f"API 응답 파싱 실패: {str(e)}")
                        return None, None, data
                elif response.status == 429:  # Too Many Requests
                    if attempt < retry_count - 1:
                        await asyncio.sleep(1)
                        continue
                    
                logger.error(f"API 호출 실패 - Status: {response.status}, Test Data ID: {test_data.id} / {arrival_station['station__id']} -> {departure_station['station__id']}")
                return None, None, data
        except asyncio.TimeoutError:
            if attempt < retry_count - 1:
                await asyncio.sleep(1)
                continue
        except Exception as e:
            logger.error(f"API 요청 실패: {str(e)}")
            if attempt < retry_count - 1:
                await asyncio.sleep(1)
                continue
            return None, None, {'error': str(e)}
    
    return None, None, {'error': 'Max retries reached'}

async def process_batch(session, potential_routes, base_date, arrival_station, data):
    """배치 단위로 API 요청 처리"""
    tasks = []
    for potential in potential_routes:
        p_departure_time = get_time_in_minutes(potential.departure_time)
        a_arrival_time = get_time_in_minutes(data.arrival_time)
        a_departure_time = get_time_in_minutes(data.departure_time)
        
        time_diff = p_departure_time - a_arrival_time
        if 0 <= time_diff <= 90 and not (a_departure_time <= p_departure_time <= a_arrival_time):
            get_monthly_last = sync_to_async(lambda p: p.monthly.last())
            p_regularly = await get_monthly_last(potential)
            
            if p_regularly:
                p_departure_type, _ = get_station_type(potential)
                
                get_station_info = sync_to_async(lambda r: r.regularly_station.filter(
                    station_type=p_departure_type
                ).values(
                    'index',
                    'station_type',
                    'station__name',
                    'station__latitude',
                    'station__longitude',
                    'station__id',
                    'time'
                ).first())
                
                departure_station = await get_station_info(p_regularly)

                if departure_station:
                    origin = f"{arrival_station['station__longitude']},{arrival_station['station__latitude']}"
                    destination = f"{departure_station['station__longitude']},{departure_station['station__latitude']}"
                    departure_time = format_departure_time(base_date, data.arrival_time)
                    
                    tasks.append({
                        'api_call': async_get_distance_and_time_from_kakao(
                            session,
                            origin=origin,
                            destination=destination,
                            departure_time=departure_time,
                            test_data=data,
                            departure_station=departure_station,
                            arrival_station=arrival_station,
                        ),
                        'route_info': {
                            'route_id': potential.id,
                            'route_name': potential.route,
                            'departure_time': potential.departure_time,
                            'departure_station': departure_station,
                        }
                    })
    
    if not tasks:
        return []
    
    results = []
    for batch in range(0, len(tasks), 10):  # 배치 크기 10
        batch_tasks = tasks[batch:batch + 10]
        api_responses = await asyncio.gather(*[task['api_call'] for task in batch_tasks])
        
        for task, api_response in zip(batch_tasks, api_responses):
            distance, duration, api_data = api_response
            if distance is not None:
                results.append({
                    **task['route_info'],
                    'distance': distance,
                    'duration': duration,
                    'formatted_duration': format_duration(duration),
                    'api_response': api_data
                })
        
        await asyncio.sleep(0.05)  # 배치 사이 딜레이
    
    return results


async def async_find_connecting_dispatches(request):
    logger.info("연결 노선 검색 시작")
    base_date = "20241228"
    
    # TCP 연결 설정
    connector = aiohttp.TCPConnector(limit=50)
    timeout = aiohttp.ClientTimeout(total=60)
    
    datas = await sync_to_async(list)(
        # DispatchRegularlyData.objects.filter(use="사용").prefetch_related('monthly').order_by('departure_time')
        DispatchRegularlyData.objects.filter(use="사용").prefetch_related('monthly').order_by('departure_time').filter(id=1837)
    )
    # print(f"기준 노선 데이터 조회 완료 - 총 {len(datas)}개 노선")
    
    # 테스트를 위해 데이터 제한
    # datas = datas[650:700]

    results = []
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        for data in datas:
            print(f"노선 분석 시작 - Route: {data.route}")
            logger.info(f"노선 분석 시작 - Route: {data.route}")
            departure_type, arrival_type = get_station_type(data)
            
            get_monthly_last = sync_to_async(lambda d: d.monthly.last())
            regularly = await get_monthly_last(data)
            
            if regularly:
                get_station_info = sync_to_async(lambda r: r.regularly_station.filter(
                    station_type=arrival_type
                ).values(
                    'index',
                    'station_type',
                    'station__name',
                    'station__latitude',
                    'station__longitude',
                    'station__id',
                    'time'
                ).first())
                
                arrival_station = await get_station_info(regularly)

                if not arrival_station:
                    print(f"도착 정류장 정보 없음 - Route: {data.route}")
                    continue

                print(f"도착 정류장 정보 찾음 - Station: {arrival_station['station__name']}")

                get_potential_connects = sync_to_async(lambda: list(
                    DispatchRegularlyData.objects.filter(use="사용")
                    .exclude(id=data.id)
                    .prefetch_related('monthly')
                ))
                
                potential_connects = await get_potential_connects()
                print(f"잠재적 연결 노선 수: {len(potential_connects)}")

                # 배치 처리로 변경
                connecting_routes = await process_batch(
                    session,
                    potential_connects,
                    base_date,
                    arrival_station,
                    data
                )

                if connecting_routes:
                    print(f"연결 가능 노선 찾음 - {len(connecting_routes)}개")
                    results.append({
                        'base_route': {
                            'id': data.id,
                            'name': data.route,
                            'arrival_time': data.arrival_time,
                            'arrival_station': arrival_station
                        },
                        'connecting_routes': connecting_routes
                    })

            # break  # 테스트를 위해 첫 번째 데이터만 처리


    print(f"검색 완료 - 총 {len(results)}개의 기준 노선에 대한 연결 노선 찾음")
    logger.info(f"검색 완료 - 총 {len(results)}개의 기준 노선에 대한 연결 노선 찾음")
    
    # 결과 상세 로깅
    # for result in results:
    #     print(f"\n=== 기준 노선 상세 정보 ===")
    #     print(f"노선명: {result['base_route']['name']}")
    #     print(f"도착 정류장: {result['base_route']['arrival_station']['station__name']}")
    #     print(f"도착 시간: {result['base_route']['arrival_time']}")
    #     print(f"id: {result['base_route']['id']}")
    #     print(f"\n=== 연결 가능 노선들 ===")
    #     for route in result['connecting_routes']:
    #         print(f"- 노선명: {route['route_name']}")
    #         print(f"  출발 시간: {route['departure_time']}")
    #         print(f"  출발 정류장: {route['departure_station']['station__name']}")
    #         print(f"  예상 거리: {route['distance']}m")
    #         print(f"  예상 소요시간: {route['formatted_duration']}")
    #         print(f"  id: {route['route_id']}")

    # 결과 데이터 저장
    await sync_to_async(bulk_create_empty_run_calculations)(results)

    logger.info("연결 노선 검색 종료")
    async_render = sync_to_async(render)
    return await async_render(request, 'dispatch/dispatch_test.html', {
        'results': results
    })

def format_duration(seconds):
    """초 단위 시간을 HH:MM 형식으로 변환"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours:02d}:{minutes:02d}"

def get_minutes_from_formatted_duration(duration_str):
    """HH:MM 형식의 시간을 분으로 변환"""
    hours, minutes = map(int, duration_str.split(':'))
    return hours * 60 + minutes

def bulk_create_empty_run_calculations(results):
    """
    results 데이터를 EmptyRunTimeCalculation 모델로 대량 생성
    운행 가능 여부(can_drive)를 시간 계산하여 결정
    """
    bulk_objects = []
    
    for result in results:
        base_route = result['base_route']

        base_arrival_time = get_time_in_minutes(base_route['arrival_time'])
        base_regularly_data = DispatchRegularlyData.objects.get(id=base_route['id'])
        base_station = Station.objects.get(id=base_route['arrival_station']['station__id'])
        
        for route in result['connecting_routes']:
            # 이미 생성된 데이터가 있는지 확인
            if EmptyRunTimeCalculation.objects.filter(regularly_data_id=base_route['id'], arrival_data_id=route['route_id']).exists():
                print("이미 생성된 데이터가 있습니다.", base_route['id'])
                logger.warning(f"이미 생성된 데이터가 있습니다. {base_route['id']}")
                continue
            departure_time = get_time_in_minutes(route['departure_time'])
            duration_minutes = get_minutes_from_formatted_duration(route['formatted_duration'])
            
            # 운행 가능 여부 계산
            # 기준 노선 도착 시간 + 이동 소요 시간이 다음 노선 출발 시간보다 작거나 같아야 함
            can_drive = (base_arrival_time + duration_minutes) <= departure_time
            
            departure_station = Station.objects.get(id=route['departure_station']['station__id'])
            departure_regularly_data = DispatchRegularlyData.objects.get(id=route['route_id'])
            
            bulk_objects.append(
                EmptyRunTimeCalculation(
                    regularly_data_id=base_regularly_data,
                    regulalry_data_station_id=base_station,
                    arrival_data_id=departure_regularly_data,
                    arrival_data_station_id=departure_station,
                    duration=route['formatted_duration'],
                    distance=str(route['distance']),
                    can_drive=can_drive
                )
            )
    
    # 대량 생성 수행
    if bulk_objects:
        EmptyRunTimeCalculation.objects.bulk_create(bulk_objects)
        print(f"총 {len(bulk_objects)}개의 데이터 생성 완료")
        logger.info(f"총 {len(bulk_objects)}개의 데이터 생성 완료")


# Django view 함수
def find_connecting_dispatches_view(request):
    login_user = Member.objects.get(id=request.session.get('user'))
    if login_user.name != "신태환":
        raise BadRequest("권한이 없습니다.")
    return asyncio.run(async_find_connecting_dispatches(request))