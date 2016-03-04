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

    def get_info(self):
        payload = {}
        update_request = requests.post(self.endpoint.get_info, headers=self.header, data=json.dumps(payload))
        response = json.loads(update_request.text)
        if response['code'] == '0':
            new_info = response['message']
            self.cell_phone = new_info['mobile']
            self.nickname = new_info['nickName']
            self.height = new_info['height']
            self.weight = new_info['weight']
            self.sex = new_info['sex']
        else:
            raise exception.ServerError(self.endpoint.get_info)

    def modify_info(self, new_info_dict):
        for key in new_info_dict:
            payload = {key: new_info_dict[key]}
            modify_request = requests.post(self.endpoint.update_info, headers=self.header, data=json.dumps(payload))
            # Actually edooon doesn't validate anything. Checks below are here just in case of other errors.
            if json.loads(modify_request.text)['code'] == '0':
                self.get_info()
            else:
                raise exception.ServerError(self.endpoint.update_info)

    def get_map_offset(self, latitude, longitude, sport_type=0):
        """
        Get map offset based on current location.
        :param latitude:
        :param longitude:
        :param sport_type:
        :return:
        """
        map_offset = {}
        payload = {'type': sport_type, 'longitude': longitude, 'latitude': latitude}
        map_offset_request = requests.post(self.endpoint.get_map_offset,
                                           headers=self.header,
                                           data=json.dumps(payload))
        response = json.loads(map_offset_request.text)
        if response['code'] == '0':
            map_offset['lat'] = response['message']['latoffset']
            map_offset['lon'] = response['message']['lngoffset']
            return map_offset
        else:
            raise exception.ServerError(self.endpoint.get_map_offset)

    def post_comment(self, activity_id, text):
        payload = {'comment': text, 'id': activity_id, 'feedbackid': 0}
        comment_request = requests.post(self.endpoint.post_comment,
                                        headers=self.header,
                                        data=json.dumps(payload))
        response = json.loads(comment_request.text)
        if response['code'] == '0':
            return response['message']['feedbackid']
        else:
            raise exception.ServerError(self.endpoint.post_comment)

    def new_activity(self, activity):
        payload = {'reportHistory': [activity.to_dict()]}
        activity_request = requests.post(self.endpoint.new_activity,
                                         headers=self.header,
                                         data=json.dumps(payload))
        response = json.loads(activity_request.text)
        if response['code'] == '0':
            return response['message']['ids'][0]
        else:
            raise exception.ServerError(self.endpoint.new_activity)

    @classmethod
    def register(cls, email, nickname, password, user_type=1):
        payload = {'email': email,
                   'passwd': password,
                   'nickName': nickname,
                   'userType': user_type}
        register_request = requests.post(constant.Endpoint.register,
                                         headers=constant.default_header,
                                         data=json.dumps(payload))
        response = json.loads(register_request.text)
        if response['code'] == '0':
            return cls(email, password)
        else:
            raise exception.ServerError(constant.Endpoint.register)
