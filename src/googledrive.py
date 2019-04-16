import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import urllib.request
import json
import datetime

# .envを使うのに必要
from dotenv import load_dotenv

load_dotenv()
load_dotenv(verbose=True)
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
# --- end ---

ENVIRONMENT_PATH_HEADER = os.getenv('ENVIRONMENT_PATH_HEADER') or os.environ.get('ENVIRONMENT_PATH_HEADER')
CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH') or os.environ.get('CHROME_DRIVER_PATH')
CHROME_BINARY_PATH = os.getenv('CHROME_BINARY_PATH') or os.environ.get('CHROME_BINARY_PATH')

CLIENT_ID = 'client_id'
CLIENT_SECRET = 'client_secret'
REDIRECT_URI = 'redirect_uri'

# 最大待機時間（秒）
wait_time = 10


def setup():
    options = Options()
    # Heroku以外ではNone
    if CHROME_BINARY_PATH is not None:
        print('CHROME_BINARY_PATH')
        options.binary_location = CHROME_BINARY_PATH
    options.add_argument('--headless')

    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options)
    driver.maximize_window()  # 画面サイズ最大化

    conf_dir = {
        CLIENT_ID: os.getenv(CLIENT_ID) or os.environ.get(CLIENT_ID),
        REDIRECT_URI: os.getenv(REDIRECT_URI) or os.environ.get(REDIRECT_URI),
        'scope': os.getenv('scopes') or os.environ.get('scopes'),
        'access_type': 'offline',
        'response_type': 'code',
        'approval_prompt': 'force',
    }
    # print(conf_dir)

    url = 'https://accounts.google.com/o/oauth2/v2/auth' \
          '?client_id={client_id}' \
          '&redirect_uri={redirect_uri}' \
          '&scope={scope}' \
          '&access_type={access_type}' \
          '&response_type={response_type}' \
          '&approval_prompt={approval_prompt}' \
        .format(**conf_dir)
    driver.get(url)

    return driver


def get_authrozation_code(driver):
    login_id = os.getenv('login_id') or os.environ.get('login_id')
    login_password = os.getenv('login_password') or os.environ.get('login_password')

    # IDを入力
    login_id_xpath = '//*[@id="identifierNext"]'
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, login_id_xpath)))
    driver.find_element_by_name("identifier").send_keys(login_id)
    driver.find_element_by_xpath(login_id_xpath).click()
    time.sleep(2)

    # パスワードを入力
    login_password_xpath = '//*[@id="passwordNext"]'
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, login_password_xpath)))
    driver.find_element_by_name("password").send_keys(login_password)
    driver.find_element_by_xpath(login_password_xpath).click()

    # アカウント選択
    # select_account = '//*[@data-identifier="{}"]'.format(login_id)
    # # select_account = '//*[@jsname="rwl3qc"]'
    # WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, select_account)))
    # driver.find_element_by_xpath(select_account).submit()
    # time.sleep(1)

    # ダイアログ取得
    # dialog_xpath = '//*[@class="g3VIld aQ7q2c Up8vH J9Nfi iWO5td"][@id="oauthScopeDialog"]'
    # WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, dialog_xpath)))
    # dialog = driver.find_element_by_xpath(dialog_xpath)

    # oauthScopeDialogの許可
    allow_login_xpath = '//*[@class="U26fgb O0WRkf oG5Srb C0oVfc kHssdc M9Bg4d"]'
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, allow_login_xpath)))
    allow_login = driver.find_element_by_xpath(allow_login_xpath)
    allow_login.click()

    # スコープの許可
    approve_access_xpath = '//*[@id="submit_approve_access"]'
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, approve_access_xpath)))
    approve_access = driver.find_element_by_xpath(approve_access_xpath)
    approve_access.click()

    # authorization_codeの取得
    authorization_xpath = '//textarea[@class="qBHUIf"]'
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, authorization_xpath)))
    authorization = driver.find_element_by_xpath(authorization_xpath)
    code = authorization.text

    driver.quit()

    return code


def get_tokens(code):
    url = 'https://accounts.google.com/o/oauth2/token'
    params = {
        'client_id': os.getenv('client_id') or os.environ.get('client_id'),
        'client_secret': os.getenv('client_secret') or os.environ.get('client_secret'),
        'redirect_uri': os.getenv('redirect_uri') or os.environ.get('redirect_uri'),
        'grant_type': 'authorization_code',
        'code': code,
    }
    header = {
        'Content-Type': 'application/json',
    }

    req = urllib.request.Request(url, json.dumps(params).encode(), header)
    with urllib.request.urlopen(req) as res:
        body = json.loads(res.read())
        access_token = body['access_token']
        refresh_token = body['refresh_token']
        print('access_token: ', access_token)
        print('refresh_token: ', refresh_token)

        return access_token, refresh_token


# def create_settings_yaml(code, access_token):
#     yaml_filenamne = 'settings.yaml'
#     # if not os.path.isfile(yaml_filenamne):
#     with open(yaml_filenamne, 'w') as f:
#         data = {
#             'client_config_backend': 'settings',
#             'client_config': {
#                 CLIENT_ID: os.getenv(CLIENT_ID) or os.environ.get(CLIENT_ID),
#                 CLIENT_SECRET: os.getenv(CLIENT_SECRET) or os.environ.get(CLIENT_SECRET),
#                 REDIRECT_URI: os.getenv(REDIRECT_URI) or os.environ.get(REDIRECT_URI),
#                 'access_token': access_token,
#                 'authorization_code': code,
#             },
#             'save_credentials': True,
#             'save_credentials_backend': 'file',
#             'save_credentials_file': 'credentials.json',
#             'get_refresh_token': True,
#             'oauth_scope': ['https://www.googleapis.com/auth/drive.file'],
#         }
#         f.write(yaml.dump(data))


def create_credentials(access_token, refresh_token):
    with open('credentials.json', 'w') as f:
        time_after_hour = datetime.datetime.now() + datetime.timedelta(hours=1)
        time_after_hour = time_after_hour.strftime('%Y-%m-%dT%H:%M:%SZ')

        data = {
            "access_token": access_token,
            CLIENT_ID: os.getenv(CLIENT_ID) or os.environ.get(CLIENT_ID),
            CLIENT_SECRET: os.getenv(CLIENT_SECRET) or os.environ.get(CLIENT_SECRET),
            "refresh_token": refresh_token,
            "token_expiry": time_after_hour,
            "token_uri": "https://accounts.google.com/o/oauth2/token",
            "user_agent": "ConvertMovie2Radio",
            "revoke_uri": "https://oauth2.googleapis.com/revoke",
            "id_token": None,
            "id_token_jwt": None,
            "token_response": {
                "access_token": access_token,
                "expires_in": 3600,
                "refresh_token": refresh_token,
                "scope": os.getenv('scopes') or os.environ.get('scopes'),
                "token_type": "Bearer"
            },
            "scopes": [

            ],
            "token_info_uri": "https://oauth2.googleapis.com/tokeninfo",
            "invalid": False,
            "_class": "OAuth2Credentials",
            "_module": "oauth2client.client"
        }

        json.dump(data, f)


# ここにアクセスで処理開始
def start():
    # Chromeを起動
    driver = setup()

    # authorization_codeの取得
    code = get_authrozation_code(driver)
    print('authorization_code: ', code)
    access_token, refresh_token = get_tokens(code)
    create_credentials(access_token, refresh_token)


if __name__ == '__main__':
    start()
