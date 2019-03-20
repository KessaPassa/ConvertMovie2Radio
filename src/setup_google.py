import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# .envを使うのに必要
from dotenv import load_dotenv

load_dotenv()
load_dotenv(verbose=True)
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
# --- end ---

# 最大待機時間（秒）
wait_time = 10


def setup():
    # chromedriverのPATHを指定（Pythonファイルと同じフォルダの場合）
    driver_path = './chromedriver'

    # Chrome起動
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.maximize_window()  # 画面サイズ最大化

    conf_dir = {
        'client_id': os.getenv('client_id') or os.environ.get('client_id'),
        'redirect_uri': os.getenv('redirect_uri') or os.environ.get('redirect_uri'),
        'scope': 'https://www.googleapis.com/auth/drive.file',
        'access_type': 'offline',
        'response_type': 'code',
    }
    print(conf_dir)

    url = 'https://accounts.google.com/o/oauth2/v2/auth' \
          '?client_id={client_id}&redirect_uri={redirect_uri}' \
          '&scope={scope}' \
          '&access_type={access_type}' \
          '&response_type={response_type}' \
        .format(**conf_dir)
    driver.get(url)

    return driver


def login_google(driver):
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
    time.sleep(1)

    return driver


def get_authrozation_code(driver):
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


# ここにアクセスで処理開始
# if __name__ == '__main__':
def main():
    # Chromeを起動
    driver = setup()

    # Googleにログイン
    driver = login_google(driver)

    # authorization_codeの取得
    code = get_authrozation_code(driver)
    print('authorization_code', code)
