from datetime import datetime, timedelta
from pathlib import Path
from firebase_admin import credentials, initialize_app, storage, _apps, get_app, delete_app
import os
from config.settings import BASE_DIR
from my_settings import CRED_PATH, STORAGE_BUCKET, CLOUD_MEDIA_PATH
from config.custom_logging import logger

def is_correct_storage_bucket(app, expected_bucket):
    try:
        bucket = storage.bucket(app=app)
        return bucket.name == expected_bucket
    except Exception as e:
        logger.error(f"Error checking storage bucket: {e}")
        return False


def init_firebase():
    cred = credentials.Certificate(os.path.join(BASE_DIR, CRED_PATH))
    if not _apps:
        logger.info(f"storage_bucket {STORAGE_BUCKET}")
        initialize_app(cred, {
            'storageBucket': STORAGE_BUCKET,
        })

    try:
        app = get_app()
        if not is_correct_storage_bucket(app, STORAGE_BUCKET):
            logger.info("Existing Firebase app has incorrect storage bucket. Reinitializing...")
            delete_app(app)
            initialize_app(cred, {
                'storageBucket': STORAGE_BUCKET,
            })
            logger.info(f"Firebase initialized with storage bucket: {STORAGE_BUCKET}")
        else:
            logger.info("Existing Firebase app has correct storage bucket.")
    except ValueError:
        # Firebase app has not been initialized yet
        initialize_app(cred, {
            'storageBucket': STORAGE_BUCKET,
        })
        logger.info(f"Firebase initialized with storage bucket: {STORAGE_BUCKET}")


def upload_to_firebase(file, file_path):
    init_firebase()
    bucket = storage.bucket()
    logger.info(f"bucket {bucket}, _apps {_apps}")
    blob = bucket.blob(file_path)
    blob.upload_from_filename(file.file.path)

    return

def get_download_url(path):
    init_firebase()
    # Firebase Storage에서 다운로드 링크 가져오기
    bucket = storage.bucket()
    blob = bucket.blob(path)
    
    # 만료 시간 설정 (예: 1시간)
    expiration = datetime.now() + timedelta(hours=1)
    url = blob.generate_signed_url(expiration)

    return url

def delete_firebase_file(path):
    init_firebase()
    try:
        bucket = storage.bucket()
        blob = bucket.blob(path)
        blob.delete()
        print(f"File {path} deleted successfully.")
        return True
    except Exception as e:
        print(f"File delete fail\nError: {e}" )
        return False