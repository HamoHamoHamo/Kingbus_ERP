from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from .models import MemberFile
from firebase.media_firebase import delete_firebase_file

@receiver(pre_delete, sender=MemberFile)
def delete_member_file(sender, instance, **kwargs):
    result = delete_firebase_file(instance.path)
    # 파일 삭제 실패하면 어떻게 할지?