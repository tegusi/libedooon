import requests
import json
import constant
import exception


class User:

    def __init__(self, username, password):
        """
        Create an user instance.
        :param username: account email address
        :param password: account password
        :return:
        """
        self.username = username
        self.password = password
        self.header = constant.default_header
        self.nickname = ''
        self.cell_phone = ''
        self.authentication_code = ''
        self.weight = 0
        self.height = 0
        self.uid = ''
        self.sex = 1  # 1 for male

    def login(self):
        """
        Login and retrieve an authentication code.
        :return:
        """
        payload = {'name': self.username,
                   'passwd': self.password,
                   'userType': 1}
        login_request = requests.post(constant.Endpoint.login, headers=self.header, data=json.dumps(payload))
        response = json.loads(login_request.text)
        if response['code'] == '0':
            # login successful
            user_data = response['message']
            self.nickname = user_data['nickName']
            self.cell_phone = user_data['mobile']
            self.authentication_code = user_data['authCode']
            self.weight = user_data['weight']
            self.height = user_data['height']
            self.uid = user_data['uName']
            self.sex = user_data['sex']
            self.header['authCode'] = user_data['authCode']
        elif response['code'] == '7':
            # Wrong credential
            raise exception.CredentialError(self.username)
