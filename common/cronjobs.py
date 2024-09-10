import os
from config.settings import MEDIA_ROOT
from config.custom_logging import logger

def delete_tmp_media_files():
    folder_path = os.path.join(MEDIA_ROOT, "tmp")
    try:
        # 폴더 내 모든 파일 목록 가져오기
        files = os.listdir(folder_path)
        
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            os.remove(file_path)
        logger.info("CRONJOB All files have been deleted.")
    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"Error delete tmp files. {e}")
