import streamlit as st


def initialize_session_state():
    default_values = {
        # ファイルアップロード
        'raw_data': '',
        # 議事録作成
        'prep_data': '', 'info_mask': '',
        'minute': '', 'make_tim': '',
        'return_username': False,
        'minute_post': '',
    }
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_session_state():
    # セッションステートをクリア
    for key in list(st.session_state.keys()):
        del st.session_state[key]
