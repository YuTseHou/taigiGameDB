from __future__ import absolute_import
from celery import shared_task
from django.shortcuts import render
from django.http import HttpResponse
from queryClosePronounce.models import Pronounce
from difflib import SequenceMatcher


@shared_task
def similar(strA, strB):
	return SequenceMatcher(None, strA, strB).ratio()

@shared_task
def hello_world(request):
    return HttpResponse("Hello taigiGameDB!")

@shared_task
def query(request, pronounceQ):

    # cut off if pronounceQ is too short
    if(len(pronounceQ) <= 1):
        return HttpResponse("Query is too short")

    # the string for returning
    theAnswer = ""

    allPronounce = Pronounce.objects.all()

    # The rank for all simlarities(pronounce, pronounceQ)
    # Higher is better
    theRank = {}

    # singlePronounce contains its pronounce and matching chinese chracters
    for singlePronounce in allPronounce:
        theRank[singlePronounce.pronounce] = similar.delay(pronounceQ, singlePronounce.pronounce)

    # sorting ranking and append result to theAnswer
    for theKey, theSimilarity in sorted(theRank.iteritems(), key = lambda (k, v) : (v, k), reverse=True):
        if(theSimilarity > 0):
            theAnswer = theAnswer + theKey + ", " + str(round(theSimilarity, 2)) + " : " + allPronounce.get(pronounce = theKey).chineses + "<br>"

    if(theAnswer == ""):
        return HttpResponse("No results")
    else:
        return HttpResponse(theAnswer)