# streamlit
import streamlit as st
from st_pages import add_page_title
from st_components.st_session_states import initialize_session_state


def home_page():
    add_page_title()

    # 説明
    st.header('このアプリについて')
    tmp = '''
    このアプリは会議の文字起こしから議事録を作成します。
    ファイルアップロード、議事録作成ページからなっています。
    '''
    st.write(tmp)

    # 注意事項
    st.header('注意事項')
    tmp = '''
    以下の注意事項を必ずご確認ください。
    ご利用は自己責任でお願いいたします。
    '''
    st.write(tmp)
    tmp = '''
    - 文字起こしデータに個人情報や機密情報が含まれないようにしてください！
        - ただし、発言者の名前はアプリ内でマスキングされるのでそのままで構いません
    - AzureOpenAIを使っています。セキュリティに関しては[公式ページ](https://learn.microsoft.com/ja-jp/legal/cognitive-services/openai/data-privacy?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext) をご確認ください
    - 自己研鑽の一環で一環で公開しているため、こちらの都合でサービスを停止することがあります
    '''
    st.warning(tmp)
    st.write('また、以下のエラーが出た場合はファイルアップロードページの「変数情報を初期化」ボタンを押すと解決する場合があります。')
    st.error('AttributeError: st.session_state has no attribute~')

    st.header('ページの説明')

    st.subheader('ファイルアップロード')
    tmp = '''
    Teams、およびZoomの文字起こしデータを対象にしています。\n
    Teamsは.vtt、Zoomは.txtファイルをアップロードしてください。
    '''
    st.write(tmp)
    tmp = '''
    手順
    - 最初にTeamsかZoomのどちらの文字起こしかを選択し、ファイルをアップロード
    - データを確認し、問題なければ次のページに進む
    '''
    st.info(tmp)

    st.subheader('議事録作成')
    tmp = '''
    アップロードされた文字起こしデータから議事録を作成します。\n
    はじめに前処理を行い、発言者の名前が自動でマスキングされます。\n
    作成は数秒〜1分ほどかかります。\n
    作成された議事録はダウンロードすることができます。
    '''
    st.write(tmp)
    tmp = '''
    手順
    - データの前処理：「前処理を実行」ボタンを押す
    - 議事録の作成：「議事録を作成」ボタンを押す
        - 議事録のフォーマットを変えたい場合は「フォーマットの変更」を開き、編集する
    - 後処理：「マスキングしたユーザー名を元に戻す」ボタンを押す
    '''
    st.info(tmp)


# ファイル実行
if __name__ == "__main__":
    # セッションステートの初期化
    initialize_session_state()
    home_page()
