from __future__ import absolute_import
from celery import shared_task
from difflib import SequenceMatcher

@shared_task
def similar(strA, strB):
    return SequenceMatcher(None, strA, strB).ratio()