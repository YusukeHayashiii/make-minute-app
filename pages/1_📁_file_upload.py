# basic
import sys
from pathlib import Path
import warnings

# streamlit
import streamlit as st
# from st_pages import add_page_title
# original
from st_components.st_session_states import initialize_session_state, reset_session_state
import utils.functions as func
from utils.auth import check_authentication
import importlib
importlib.reload(func)

warnings.filterwarnings('ignore')
# appのディレクトリをパスに追加
current_dir = Path(__file__).absolute()
parent_dir = current_dir.parent.parent
sys.path.append(str(parent_dir))


def file_upload():
    # ファイルアップロード
    st.header('ファイルアップロード')
    file_type = st.radio("ファイルタイプを選択してください", ("Teamsの文字起こし", "Zoomの文字起こし"))

    if file_type == "Teamsの文字起こし":
        uploaded_file = st.file_uploader('ファイルをアップロードしてください', type=['vtt'])
    elif file_type == "Zoomの文字起こし":
        uploaded_file = st.file_uploader('ファイルをアップロードしてください', type=['txt'])

    if uploaded_file is not None:
        st.success("ファイルが正常にアップロードされました!")

        try:
            if file_type == "Teamsの文字起こし":
                # UploadedFileオブジェクトの内容を文字列として読み込む
                vtt_content = uploaded_file.getvalue().decode('utf-8-sig')
                df = func.vtt_to_dataframe(vtt_content)
                # start, end列を削除
                df = df.drop(columns=['start', 'end'])
            elif file_type == "Zoomの文字起こし":
                txt_content = uploaded_file.getvalue().decode('utf-8-sig')
                df = func.txt_to_dataframe(txt_content)
                # time列を削除
                df = df.drop(columns=['time'])
            st.session_state.raw_data = df
        except Exception as e:
            st.error(f"アップロードが失敗しました: {e}")


def chk_data():
    df = st.session_state.raw_data
    if not type(df) is str:
        st.header('データ確認')
        # データ確認
        st.write(f'データ数: {df.shape[0]}件')
        st.write(df)


def main():
    # add_page_title()
    st.title('ファイルアップロード')

    if st.button('変数情報を初期化'):
        reset_session_state()
        initialize_session_state()
        st.rerun()
    st.info('このボタンを押すことでアプリの状態を初期化し、ページをリロードできます')

    # ファイルアップロードし、データフレームに変換
    file_upload()
    # データを確認
    chk_data()


if __name__ == "__main__":
    st.set_page_config(
        page_title="file_upload",
        page_icon="📁",
    )
    if not check_authentication():
        st.stop()
    main()
