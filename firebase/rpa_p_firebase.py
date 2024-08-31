import sys
import os
from firebase_admin import credentials, initialize_app, storage, _apps, get_app, delete_app, firestore

# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.custom_logging import logger

class RpaPFirebase():
    
    def __init__(self):
        self.db = firestore.Client()
        self.ref = self.db.collection("Server").document("Dev")
        self.init_sunghwatour_firebase()

    def init_sunghwatour_firebase(self):
        # cred = credentials.Certificate(dir)
        if not _apps:
            initialize_app()
    
        try:
            app = get_app()
            if app:
                delete_app(app)
            app = initialize_app()
        except Exception as e:
            print("firebase init error", e)
            app = initialize_app()
            print("init firebase", app)
        return

    def add_estimate(self, data, user_uid, station_list):
        try:
            estimate_ref = self.ref.collection("User").document(user_uid).collection("Estimate")
            new_estimate = estimate_ref.add(data)
            print(new_estimate[1].path)
    
            for address in station_list:
                estimate_ref.document(new_estimate[1].id).collection("EstimateAddress").add(address)
            
        except Exception as e:
            logger.error(f"Firebase add error : {e}")
            raise Exception(f"Firebase add error : {e}")

        return new_estimate[1].path, new_estimate[1].id


    def get_doc_path(self, uid, user_uid):
        doc = self.ref.collection("User").document(user_uid).collection("Estimate").document(uid)
        return doc.path

    def edit_estimate(self, path, type, value):
        doc = self.db.document(path)
        estimate = doc.get()
        if not estimate:
            raise Exception("Firebase get error : No matched data")
        estimate_data = estimate.to_dict()
        estimate_data[type] = value

        try:
            doc.set(estimate_data)
        except Exception as e:
            logger.error(f"Firebase add error : {e}")
            raise Exception(f"Firebase add error : {e}")

        return estimate_data

    def get_value(self, uid, field):
        doc = self.db.document(uid)
        print("TEST", doc)
        estimate = doc.get()
        if not estimate:
            raise Exception("Firebase get error : No matched data")
        try:
            estimate_data = estimate.to_dict()
            return estimate_data[field]

        except Exception as e:
            logger.error(f"Firebase add error : {e}")
            raise Exception(f"Firebase add error : {e}")
        
