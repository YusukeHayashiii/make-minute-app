# basic
import sys
import yaml
from pathlib import Path
import warnings

import pandas as pd
# streamlit
import streamlit as st
from st_pages import add_page_title

# original
import utils.functions as func
import st_components.st_config as config
import importlib
importlib.reload(func)
importlib.reload(config)

warnings.filterwarnings('ignore')
# appのディレクトリをパスに追加
current_dir = Path(__file__).absolute()
parent_dir = current_dir.parent.parent
sys.path.append(str(parent_dir))


def preprocess():
    st.header('データの前処理')
    df_prep = st.session_state.raw_data
    if st.button('前処理を実行'):
        with st.spinner('前処理を実行中です...'):
            if not type(df_prep) is str:
                # テキストクリーニング
                df_prep['text'] = df_prep['text'].apply(func.clean_text)
                # userでのコメント結合
                df_prep = func.comment_marge_by_user(df_prep)
                # user名をマスキング
                masking_map = {}
                for i, user in enumerate(df_prep['user'].unique()):
                    masking_map[user] = f'User_{i}'
                df_prep['user'] = df_prep['user'].map(masking_map)
                # フィラー除去
                # df_prep = _clear_filler(df_prep)
                st.session_state.prep_data = df_prep  # 前処理後のデータを保存
                info_mask = pd.DataFrame(masking_map.items(), columns=['user', 'masking'])
                st.session_state.info_mask = info_mask  # マスキング情報を保存
    # 結果を表示
    if not type(st.session_state.prep_data) is str:
        st.success("データの前処理が完了しました!")
        # データ確認
        st.subheader("処理されたデータ")
        st.write(f'データ数: {st.session_state.prep_data.shape[0]}件')
        st.write(st.session_state.prep_data)
        st.write('ユーザー名のマスキング情報')
    if not type(st.session_state.info_mask) is str:
        st.write(st.session_state.info_mask)


def make_minute():
    st.header('議事録作成')

    # プロンプトの準備
    with open(config.MAKE_MINUTE_PROMPT_FILE, 'r') as f:
        prompts = yaml.safe_load(f)
    sys_prompt = prompts[config.SYS_MAKE_MINUTE_PROMPT]
    with open(config.MAKE_MINUTE_PROMPT_FILE, 'r') as f:
        prompts = yaml.safe_load(f)
    minute_format = prompts[config.MINUTE_FORMAT]
    st.info('議事録のフォーマットを変えたい場合は以下を編集してください')
    with st.expander('フォーマットの変更'):
        minute_format = st.text_area('現在のフォーマット',
                                     minute_format,
                                     height=300,
                                     )
    sys_prompt = sys_prompt.format(format=minute_format)

    if st.button('議事録を作成'):
        with st.spinner('議事録を作成中です...'):
            df_prep = st.session_state.prep_data
            if not type(df_prep) is str:
                # データフレームの各行を{text:user}の辞書に変換
                text_dict = df_prep.to_dict(orient='records')
                # ユーザープロンプト準備
                with open(config.MAKE_MINUTE_PROMPT_FILE, 'r') as f:
                    prompts = yaml.safe_load(f)
                usr_prompt = prompts[config.MAKE_MINUTE_PROMPT]
                usr_prompt = usr_prompt.format(data=text_dict)
                # GPTによる文章生成
                result, tim, error = func.excute_make_sentence(prompt=usr_prompt,
                                                               sys_prompt=sys_prompt,
                                                               )
                if error:
                    tmp = 'エラーが発生しました。詳しくはアプリ作成者にお問い合わせください。'
                    error = tmp + '\n\n' + error
                    st.error(error)
                else:
                    st.success("議事録が作成されました！")
                    st.session_state.minute = result  # 議事録を保存
                    st.session_state.make_tim = tim  # 処理時間を保存
    # 結果を表示
    if type(st.session_state.make_tim) is float:
        st.subheader('作成された議事録')
        st.code(st.session_state.minute)
        st.write(f'処理時間: {st.session_state.make_tim:,.2f}s')
        # ファイルダウンロード
        # st.download_button(
        #     label="議事録をテキストファイルでダウンロード",
        #     data=st.session_state.minute,
        #     file_name='generated_minute.txt',
        # )


def postprocess():
    st.header('後処理')
    # マスキングしたユーザー名を元に戻す
    info_mask = st.session_state.info_mask
    minute = st.session_state.minute  # テキストデータの議事録
    if st.button('マスキングしたユーザー名を元に戻す'):
        with st.spinner('後処理を実行中です...'):
            if not type(info_mask) is str:
                for user, masking in info_mask.values:
                    minute = minute.replace(masking, user)
                st.session_state.minute_post = minute
                st.session_state.return_username = True
    # 結果を表示
    if st.session_state.return_username:
        st.subheader('後処理後の議事録')
        st.code(st.session_state.minute_post)
        # ファイルダウンロード
        st.download_button(
            label="後処理後の議事録をダウンロード",
            data=st.session_state.minute_post,
            file_name='generated_minute.txt',
        )


def main():
    add_page_title()
    # データの前処理
    preprocess()
    # 議事録の作成
    make_minute()
    # 後処理
    postprocess()


if __name__ == "__main__":
    main()
