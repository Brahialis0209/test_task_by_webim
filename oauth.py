import requests


class VKAuth:
    def __init__(self):

        self.session = requests.Session()
        self.user_id = None
        self.access_token = None
        self.response = None
        self.api_v = 5.52
        self.app_id = 7561984
        self.security_code = '9B74dJdjCJKeoasypn11'
        self.auto_access = True
        # self.password = 'RAFAFAfa290911'
        self.client_secret = '9B74dJdjCJKeoasypn11'
        # self.username = '89817882901'

    def get_url(self):
        api_auth_url = 'https://oauth.vk.com/authorize'
        app_id = self.app_id
        redirect_uri = 'https://oauth.vk.com/blank.html'
        display = 'wap'
        api_version = self.api_v
        access_date = 'friends'

        auth_url_template = '{0}?client_id={1}&scope={2}&redirect_uri={3}&display={4}&v={5}&response_type=token'
        auth_url = auth_url_template.format(api_auth_url, app_id, access_date, redirect_uri, display,
                                            api_version)

        return auth_url

    def get_url_with_password(self):
        api_auth_url = 'https://oauth.vk.com/token?grant_type'
        password = 'RAFAFAfa290911'
        client_secret = '9B74dJdjCJKeoasypn11'
        app_id = self.app_id
        username = '89817882901'
        redirect_uri = 'https://oauth.vk.com/blank.html'
        display = 'wap'
        api_version = self.api_v
        access_date = 'friends'

        auth_url_template = '{0}={1}&client_id={2}&client_secret={3}&username={4}&password={5}&scope=friends&v=5.122&2fa_supported=1'
        auth_url = auth_url_template.format(api_auth_url, 'password', app_id, client_secret, username,
                                            password)

        return auth_url

