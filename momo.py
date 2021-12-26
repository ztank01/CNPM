import base64
import json
import uuid
import hmac
import hashlib

import requests
from flask import render_template, request, redirect


def momoRequestJSON(amount, orderInfo, hopdong):
    # parameters send to MoMo get get payUrl
    endpoint = "https://test-payment.momo.vn/gw_payment/transactionProcessor"
    partnerCode = "MOMOT5GJ20211110"
    accessKey = "gEzSrZwe5E4ahJri"
    secretKey = b"U9ylR6QzZsW4oOwkHq3si4ACpI2uhiDK"
    redirectUrl = "/thanh_toan_thanh_cong"
    ipnUrl = "http://127.0.0.1:5000/"
    orderId = str(uuid.uuid4())
    requestId = str(uuid.uuid4())
    requestType = "captureWallet"
    hopdong = '{"' + 'hopdong' + '": [' + hopdong + ']}'
    phong_byte = hopdong.encode("utf-8")
    extraData = base64.b64encode(phong_byte).decode('utf-8')  # pass empty value or Encode base64 JsonString

    # before sign HMAC SHA256 with format: accessKey=$accessKey&amount=$amount&extraData=$extraData&ipnUrl=$ipnUrl
    # &orderId=$orderId&orderInfo=$orderInfo&partnerCode=$partnerCode&redirectUrl=$redirectUrl&requestId=$requestId
    # &requestType=$requestType
    rawSignature = "accessKey=" + accessKey + "&amount=" + amount + "&extraData=" + extraData.__str__() + "&ipnUrl=" + ipnUrl + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&partnerCode=" + partnerCode + "&redirectUrl=" + redirectUrl + "&requestId=" + requestId + "&requestType=" + requestType

    # puts raw signature
    # signature
    h = hmac.new(secretKey, rawSignature.encode('utf-8'), hashlib.sha256)
    signature = h.hexdigest()

    # json object send to MoMo endpoint

    data = {
        'partnerCode': partnerCode,
        'partnerName': "Test",
        'storeId': "MomoTestStore",
        'requestId': requestId,
        'amount': amount,
        'orderId': orderId,
        'orderInfo': orderInfo,
        'redirectUrl': redirectUrl,
        'ipnUrl': ipnUrl,
        'lang': "vi",
        'extraData': extraData,
        'requestType': requestType,
        'signature': signature
    }
    # print(data)
    headers = {"Content-Type": "application/json; charset=UTF-8", "Content-Length": str(len(data)),
               "Host": "test-payment.momo.vn"}
    resp = requests.post(url="https://test-payment.momo.vn/v2/gateway/api/create", json=data, headers=headers)
    # print(resp.json())
    return resp.json()['payUrl']


if __name__ == '__main__':
    print(momoRequestJSON(amount="60000", orderInfo="Thanh toán phòng 101", hopdong="1,2"))
    # print(base64.b64decode(extraData))
