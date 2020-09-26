from configparser import ConfigParser
import os

# get abs path
folder = os.path.dirname(os.path.abspath(__file__))
# get file path
file = os.path.join(folder, 'dev_config.ini')
# read api key file
config = ConfigParser()
config.read(file)


class BotConfig:
    def __init__(self, dev=False):
        if dev:
            self.token = config.get('main', 'dev_api_key')
        else:
            self.token = config.get('main', 'prod_api_key')
        self.version = '1.3'
        self.dividend_url = 'https://www.dividends.sg/view/'
        self.upcoming_dividends_url = 'https://www.dividends.sg/dividend/coming'
        self.admin_id = config.get('main', 'admin_id')
        self.admin_password = config.get('main', 'admin_password')
