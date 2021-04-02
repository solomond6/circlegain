# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect 
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.template.context_processors import csrf
from django.core import serializers
from django.conf import settings as conf_settings
# from adminPortal.models import VerificationOfficers, Driversapprovals, Driverschedules, VerificationResult
# from adminPortal.serializers import VerificationOfficerLoginSerializer, VerificationResultSerializer, VerificationOfficerPerformanceSerializer, VerificationOfficerScheduleSerializer
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import base64
import datetime
import ccxt

def ping(request):
    return HttpResponse("00")

class ExchangeRate(APIView):
	def get(self, request, format=None):
		try:

			# side = request.GET.get('Side', None)
			side = self.request.query_params.get('side', None)
			amount = self.request.query_params.get('amount', None)

			order = "";
			if side is None:
				response = {"responseCode":"99", "msg":"missing side"}
				return HttpResponse(json.dumps(response), content_type="text/json-comment-filtered")
			elif amount is None:
				response = {"responseCode":"77", "msg":"invalid amount"}
				return HttpResponse(json.dumps(response), content_type="text/json-comment-filtered")
			else:
				# if side is 'buy':
				# 	response = {"responseCode":"88", "msg":"invalid side"}
				# 	return HttpResponse(json.dumps(response), content_type="text/json-comment-filtered")

				PUBLIC_API_KEY = conf_settings.PUBLIC_API_KEY
				SECRET_PRIVATE_KEY = conf_settings.SECRET_PRIVATE_KEY

				# binance_ticker = ccxt.binance().fetch_ticker('BTC/USDT')

				exchange = ccxt.binance({
				    'enableRateLimit': True,
				    'apiKey': PUBLIC_API_KEY,
				    'secret': SECRET_PRIVATE_KEY,
				    'options': {
				        'defaultType': 'future',
				    },
				})

				# print('Loading markets from', exchange.id)
				exchange.load_markets()
				# print('Loaded markets from', exchange.id)

				exchange.verbose = False

				symbol = 'BTC/USDT'
				type = 'market'
				side = side  # long
				amount = float(amount)

				order_response = exchange.create_order(symbol, 'market', 'buy', amount)

				response = {"responseCode":"00", "msg":"order created", "responseData":order_response}
				return HttpResponse(json.dumps(response), content_type="text/json-comment-filtered")
		except Exception as exception:
			response = {"responseCode":"66", "msg":"Exception", "responseData":str(exception)}
			return HttpResponse(json.dumps(response), content_type="text/json-comment-filtered")