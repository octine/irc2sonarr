import requests
import json
import datetime


class SonarrApi:
    def __init__(self, api_key, server_ip, server_port):
        self.api_key = api_key
        self.endpoint = 'http://{}:{}/api/'.format(server_ip, server_port)
        self.template = '{}{}?apikey={}'

    def server_status(self):
        return requests.get(self.template.format(self.endpoint, 'system/status', self.api_key))

    def release_push(self, title, url):
        data = {'title': title,
                'downloadURL': url,
                'protocol': 'Torrent',
                'publishDate': datetime.datetime.utcnow().isoformat()}
        return requests.post(self.template.format(self.endpoint, 'release/push', self.api_key), json=data)


if __name__ == '__main__':
    api_key = ''
    ip = 'localhost'
    s = SonarrApi(api_key, ip)
    print(json.dumps(s.server_status().json(), indent=4))
