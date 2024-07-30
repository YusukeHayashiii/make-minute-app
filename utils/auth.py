import os
import sys
from pathlib import Path
import yaml
from yaml.loader import SafeLoader
import streamlit as st
from streamlit_authenticator import Authenticate, Hasher

# homeのディレクトリをパスに追加
current_dir = Path(__file__).absolute()
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))


def load_config():
    config_path = 'utils/config.yaml'
    if not os.path.exists(config_path):
        st.error(f"設定ファイルが見つかりません: {config_path}")
        return None

    try:
        with open(config_path) as file:
            config = yaml.load(file, Loader=SafeLoader)

        # 最小限の構造チェック
        if 'credentials' not in config or 'usernames' not in config['credentials']:
            st.error("設定ファイルの構造が正しくありません。")
            return None

        return config
    except yaml.YAMLError as e:
        st.error(f"設定ファイルの読み込みエラー: {e}")
        return None


def initialize_authentication():
    config = load_config()
    if config is None:
        return None, None

    try:
        authenticator = Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days']
        )
        return authenticator, config
    except KeyError as e:
        st.error(f"認証の初期化エラー: 必要な設定キーが見つかりません - {e}")
        return None, None


def check_authentication():
    if st.session_state['authentication_status'] is None:
        authenticator, config = initialize_authentication()
        if authenticator is None or config is None:
            st.error("認証システムの初期化に失敗しました。管理者に連絡してください。")
            return False

        st.session_state['authenticator'] = authenticator
        st.session_state['config'] = config

    authenticator = st.session_state['authenticator']
    # ログインフォームを表示
    name, authentication_status, username = authenticator.login()

    if authentication_status is False:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and password')

    st.session_state['authentication_status'] = authentication_status
    st.session_state['name'] = name
    st.session_state['username'] = username

    if st.session_state['authentication_status']:
        st.write(f'Welcome *{name}*')
        authenticator.logout('Logout', 'main')
        return True
    else:
        # 登録ボタンを表示
        if st.button('新規登録'):
            st.session_state['show_registration'] = True

        if st.session_state.get('show_registration', False):
            show_registration_form()

        return False


def show_registration_form():
    st.subheader('新規ユーザー登録')
    # authenticator = st.session_state['authenticator']
    config = st.session_state['config']

    with st.form('registration_form'):
        new_username = st.text_input('ユーザー名')
        # new_name = st.text_input('氏名')
        new_password = st.text_input('パスワード', type='password')
        new_password_repeat = st.text_input('パスワード（確認）', type='password')

        if st.form_submit_button('登録'):
            if new_password != new_password_repeat:
                st.error('パスワードが一致しません')
            elif new_username in config['credentials']['usernames']:
                st.error('このユーザー名は既に使用されています')
            else:
                # 新しいユーザーを追加
                hashed_password = Hasher([new_password]).generate()[0]
                config['credentials']['usernames'][new_username] = {
                    'name': new_username,
                    'password': hashed_password
                }
                save_config(config)
                st.session_state['registration_completed'] = True
                st.session_state['show_registration'] = False
                st.success('ユーザー登録が完了しました。ログインしてください。')


def save_config(config):
    config_path = 'utils/config.yaml'
    try:
        with open(config_path, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
    except Exception as e:
        st.error(f"設定の保存中にエラーが発生しました: {e}")
