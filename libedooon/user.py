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
        self.sex = 1  # 1 for male, 2 for sex
        self.endpoint = constant.Endpoint('')

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
            self.endpoint = constant.Endpoint(user_data['authCode'])
        elif response['code'] == '7':
            # Wrong credential
            raise exception.CredentialError(self.username)
        # currently edooon doesn't check client token, so the lines commented out below are totally useless.
        # payload = {'token': constant.client_token}
        # token_request = requests.post(self.endpoint.user_token, headers=self.header, data=json.dumps(payload))

    def modify_info(self, new_info_dict):
        for key in new_info_dict:
            payload = {key: new_info_dict[key]}
            modify_request = requests.post(self.endpoint.update_info, headers=self.header, data=json.dumps(payload))
            # Actually edooon doesn't validate anything. Checks below are here just in case of other errors.
            if json.loads(modify_request.text)['code'] == '0':
                pass
            else:
                raise exception.ServerError(self.endpoint.update_info)