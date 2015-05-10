from __future__ import absolute_import
from celery import shared_task
from difflib import SequenceMatcher

@shared_task
def matcher(strA, strB):
	return SequenceMatcher(None, strA, strB).ratio()

@shared_task
def similar(allPronounce, pronounceQ):
	theRank = {}
	for singlePronounce in allPronounce:
		tmp = matcher(pronounceQ, singlePronounce.pronounce)
		if(tmp > 0.6):
			theRank[singlePronounce.pronounce] = tmp
	return theRank