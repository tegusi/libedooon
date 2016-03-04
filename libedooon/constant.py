default_header = {
    'AppVersion': '3.1.5',
    'Accept': '*/*',
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate',
    'App': 1,
    'Content-Type': 'application/json',
    'User-Agent': 'EdooonGPS/18 CFNetwork/758.2.8 Darwin/15.0.0',
    'Connection': 'keep-alive',
    'authCode': ''
}


class Endpoint:
    base = 'http://edooon.com'
    login = base + '/commInterface/v1/user/login'
