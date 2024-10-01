FROM python:3.8.1

# 작업 디렉터리를 /code로 설정
WORKDIR /code

# 최신 pip 설치
RUN python -m pip install --upgrade pip

# 로컬의 requirements.txt 파일을 컨테이너로 복사
COPY requirements.txt /code/

# 필요한 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 로컬 프로젝트의 모든 파일을 컨테이너로 복사
COPY . /code/

# Django 서버를 실행할 포트 8000을 외부에 노출
EXPOSE 8000

# 서버 실행 명령어
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]