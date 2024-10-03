import pytest
from humanresource.models import Member

@pytest.fixture
def authorized_client(client, authorized_user):
    # 세션에 권한을 설정 (예: user_id, permission 등의 정보)
    session = client.session
    session['user'] = authorized_user
    session['name'] = authorized_user.name  # 가정: user_id=1 사용자가 로그인된 상태
    session['authority'] = authorized_user.authority  # 가정: 관리자 권한을 가진 사용자
    session.save()

    # 권한이 설정된 client를 반환
    return client

@pytest.fixture
def authorized_user():
    try:
        return Member.objects.get(name="admin", authority=0)
    except:
        return Member.objects.create(name="admin", authority=0)