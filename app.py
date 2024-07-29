# basic
import sys
from pathlib import Path
import warnings
# import yaml
# from yaml.loader import SafeLoader
# streamlit
import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title
# import streamlit_authenticator as stauth
# original
from st_components.st_session_states import initialize_session_state
# import utils.functions as func

warnings.filterwarnings('ignore')
# appのディレクトリをパスに追加
current_dir = Path(__file__).absolute()
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))


# Streamlitアプリの構築開始
def main():
    add_page_title()
    show_pages(
        [
            Page("st_components/st_home_page.py", "ホーム", "🏠"),
            Page("st_components/st_file_upload.py", "ファイルアップロード", "📁"),
            Page("st_components/st_make_minute.py", "議事録作成", "✎"),
            Section("上から順に実行してください", icon="⚠️"),
        ]
    )


# ファイル実行
if __name__ == "__main__":
    # 初期化とページ作成
    initialize_session_state()
    main()
    # # ログインページの作成
    # authenticator = func.make_authentication('utils/config.yaml')
    # name, authentication_status, username = authenticator.login()
    # if authentication_status:
    #     # 認証に成功
    #     authenticator.logout("Logout", "main")
    # elif authentication_status == False:
    #     # 認証に失敗(入力値が不正)
    #     st.error("username/password is incorrect")
    # elif authentication_status == None:
    #     # 入力せずにログインを試みた場合
    #     st.warning("Please enter your username and password")
