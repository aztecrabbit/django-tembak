from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from tembak.forms import XlSigninForm, XlSendPackageForm

import requests
import json

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def index(request):
    return HttpResponse(reverse('tembak:index'))

def xl_index(request):
    if not request.session.get('tembak_xl'):
        return HttpResponseRedirect(reverse('tembak:xl-signin'))

    if request.method == 'POST':
        form = XlSendPackageForm(request.POST)

        if form.is_valid():
            msisdn = request.session['tembak_xl']['msisdn']
            session_id = request.session['tembak_xl']['session_id']
            request_id = timezone.now().now().strftime('%Y%m%d%H%M%S')
            package_id = form.cleaned_data['package_id']

            content = {
                "Header": None,
                "Body": {
                    "HeaderRequest": {
                        "applicationID": "3",
                        "applicationSubID": "1",
                        "touchpoint": "MYXL",
                        "requestID": request_id,
                        "msisdn": msisdn,
                        "serviceID": package_id
                    },
                    "opPurchase": {
                        "msisdn": msisdn,
                        "serviceid": package_id
                    },
                    "XBOXRequest": {
                        "requestName": "GetSubscriberMenuId",
                        "Subscriber_Number": "1219456993",
                        "Source": "mapps",
                        "Trans_ID": request_id,
                        "Home_POC": "JK0",
                        "PRICE_PLAN": "513738114",
                        "PayCat": "PRE-PAID",
                        "Active_End": "20190704",
                        "Grace_End": "20190803",
                        "Rembal": "0",
                        "IMSI": "638362452848946",
                        "IMEI": "3424467086686843",
                        "Shortcode": "mapps"
                    },
                    "Header": {
                        "ReqID": request_id
                    }
                },
                "sessionId": session_id,
                "serviceId": package_id,
                "packageRegUnreg": "Reg",
                "reloadType": "",
                "reloadAmt": "",
                "packageAmt": "0",
                "platform": "04",
                "appVersion": "3.8.2",
                "sourceName": "Firefox",
                "sourceVersion": "",
                "msisdn_Type": "P",
                "screenName": "home.storeFrontReviewConfirm",
                "mbb_category": "",
            }

            headers = {
                "Host": "my.xl.co.id",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,id;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://my.xl.co.id/pre/index1.html",
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "True",
                "Content-Length": str(len(str(content))),
                "DNT": "1",
                "Connection": "keep-alive",
            }

            try:
                response = requests.request('POST', 'https://my.xl.co.id/pre/opPurchase', headers=headers, json=content, timeout=30, verify=False)
                response = response.text
            except Exception as exception:
                return HttpResponseRedirect(f"{reverse('tembak:xl-index')}?error={exception}")

            if 'IN PROGRESS' in response:
                return HttpResponseRedirect(f"{reverse('tembak:xl-index')}?success={response}")

            return HttpResponseRedirect(f"{reverse('tembak:xl-index')}?warning={response}")

    else:
        form = XlSendPackageForm()

    context = {
        'form': form,
    }

    return render(request, 'tembak/xl_index.html', context)

def xl_request_otp(request):
    if not request.GET.get('msisdn'):
        return HttpResponse('{"error": true}')

    msisdn = request.GET.get('msisdn')

    content = {
        "Header": None,
        "Body": {
            "Header": {
              "ReqID": "20190622115421",
            },
            "LoginSendOTPRq": {
              "msisdn": msisdn,
            }
        },
        "sessionId": None,
        "onNet": "False",
        "platform": "04",
        "appVersion": "3.8.2",
        "sourceName": "Firefox",
        "screenName": "login.enterLoginNumber",
    }

    headers = {
        "Host": "my.xl.co.id",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,id;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://my.xl.co.id/pre/index1.html",
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "True",
        "Content-Length": str(len(str(content))),
        "DNT": "1",
        "Connection": "keep-alive",
    }

    try:
        response = requests.request('POST', 'https://my.xl.co.id/pre/LoginSendOTPRq', headers=headers, json=content, timeout=30, verify=False)
        response = response.text
    except Exception as exception:
        return HttpResponse(exception)

    return HttpResponse(response)

def xl_signin(request):
    if request.session.get('tembak_xl'):
        return HttpResponseRedirect(reverse('tembak:xl-index'))

    if request.method == 'POST':
        form = XlSigninForm(request.POST)

        if form.is_valid():
            request_id = timezone.now().now().strftime('%Y%m%d%H%M%S')
            request_date = timezone.now().now().strftime('%Y%m%d')

            content = {
                "Header": None,
                "Body": {
                    "Header": {
                            "ReqID": request_id,
                    },
                    "LoginValidateOTPRq": {
                        "headerRq": {
                            "requestDate": request_date,
                            "requestId": request_id,
                            "channel": "MYXLPRELOGIN"
                        },
                        "msisdn": form.cleaned_data['msisdn'],
                        "otp":form.cleaned_data['otp'],
                    }
                },
                "sessionId": None,
                "platform":"04",
                "msisdn_Type":"P",
                "serviceId":"",
                "packageAmt":"",
                "reloadType":"",
                "reloadAmt":"",
                "packageRegUnreg":"",
                "appVersion":"3.8.2",
                "sourceName":"Firefox",
                "sourceVersion":"",
                "screenName":"login.enterLoginOTP",
                "mbb_category":""
            }

            try:
                response = requests.request('POST', 'https://my.xl.co.id/pre/LoginValidateOTPRq', json=content, timeout=30)
                response = json.loads(response.text)
            except Exception as exception:
                return HttpResponseRedirect(f"{reverse('tembak:xl-signin')}?error={exception}")

            if 'headerRs' not in response['LoginValidateOTPRs']:
                request.session['tembak_xl'] = {
                    'msisdn': response['LoginValidateOTPRs']['msisdn'],
                    'session_id': response['sessionId'],
                }

                return HttpResponseRedirect(reverse('tembak:xl-index'))

            return HttpResponseRedirect(f"{reverse('tembak:xl-signin')}?error={response}")

    else:
        form = XlSigninForm()

    context = {
        'form': form,
    }

    return render(request, 'tembak/xl_signin.html', context)


def xl_signout(request):
    if request.session.get('tembak_xl'):
        del request.session['tembak_xl']

    return HttpResponseRedirect(reverse('tembak:xl-signin'))
