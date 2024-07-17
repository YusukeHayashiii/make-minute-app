import os
import re
import io
import warnings
import time
from dotenv import load_dotenv

from webvtt import WebVTT
import pandas as pd
import jaconv
# from openai import OpenAI
from openai import AzureOpenAI as AOAI
import openai

warnings.filterwarnings('ignore')
# 環境変数の読み込み
dotenv_path = '.env'
load_dotenv(dotenv_path)


def vtt_to_dataframe(data):
    '''
    vttデータをpandas.DataFrameに変換する
    '''
    vtt = WebVTT().read_buffer(io.StringIO(data))
    captions = []

    for caption in vtt:
        # 話者名を抽出するための正規表現パターン
        pattern = r'<v\s(.*?)>'
        match = re.search(pattern, caption.raw_text)
        if match:
            user = match.group(1)  # マッチしたユーザー名の部分を取得
        else:
            user = 'Unknown'
        captions.append([caption.start, caption.end, caption.text, user])

    df = pd.DataFrame(captions, columns=["start", "end", "text", "user"])
    return df


def txt_to_dataframe(data):
    '''
    txtデータをpandas.DataFrameに変換する
    '''
    pattern = r'\[(\w+)\] (\d{2}:\d{2}:\d{2})\n((?:(?!\[).)*(?:\n(?!\[).*)*)'
    # パターンにマッチする部分を抽出
    matches = re.findall(pattern, data, re.DOTALL)
    # データフレームを作成
    df = pd.DataFrame(matches, columns=['user', 'time', 'text'])
    # テキストから余分な改行を削除
    df['text'] = df['text'].str.replace('\n', ' ').str.strip()
    # 列の順序を変更
    df = df[['time', 'text', 'user']]
    return df


# 前処理 #####

def clean_text(text):
    '''
    テキストクリーニングを行う
    '''
    replaced_text = text
    replaced_text = re.sub(r'[【】]', ' ', replaced_text)       # 【】の除去
    replaced_text = re.sub(r'[（）()]', ' ', replaced_text)     # （）の除去
    replaced_text = re.sub(r'[［］\[\]]', ' ', replaced_text)   # ［］の除去
    replaced_text = re.sub(r'[@＠]\w+', '', replaced_text)  # メンションの除去
    replaced_text = re.sub(r'https?:\/\/.*?[\r\n ]', '', replaced_text)  # URLの除去
    replaced_text = re.sub(r'　', '', replaced_text)  # 全角空白の除去
    replaced_text = re.sub(r' ', '', replaced_text)  # 半角空白の除去
    replaced_text = jaconv.z2h(replaced_text, kana=False, digit=True, ascii=True)  # アルファベットと数字を半角に統一
    return replaced_text


def comment_marge_by_user(df):
    '''
    userが前のレコードと同じ場合、textを一つにまとめて新たなデータフレームに格納
    '''
    for i in range(len(df)):
        if i == 0:
            continue
        if df.at[i, 'user'] == df.at[i - 1, 'user']:
            df.at[i, 'text'] = df.at[i - 1, 'text'] + ' ' + df.at[i, 'text']
            df.at[i - 1, 'text'] = ''
    # textが空白の行を削除
    df = df[df['text'] != ''].reset_index(drop=True)
    return df


# LLM関連_OpenAI #####

def single_ask_gpt_to_respond(prompt,
                              sys_prompt="You are a highly skilled data scientist.",
                              model=os.environ.get("OPENAI_ENGINE_LLM"),
                              max_tokens=2500,
                              temp=0,
                              top_p=1,
                              freq_pn=0,
                              pres_pn=0,
                              stop=None):
    """
    LLMに1往復の応答を実行させる関数
    :param
    - prompt: ユーザープロンプト
    - sys_prompt: システムプロンプト
    - model: モデル名
    - max_tokens: 出力の最大トークン数
    - temp: 0-1の値を取り、大きい方が生成文章のランダム性が上がる
    - top_p: 0-1の値を取り、累積確率が上位p*100%までの単語を候補にする
    - freq_pn: -2.0 から 2.0 の数値。 値を正にすると、これまでのテキストに存在する頻度に基づいて新しいトークンにペナルティが課せられ、モデルが同じ行を逐語的に繰り返す可能性が低下します。
    - pres_pn: -2.0 から 2.0 の数値。 正の値を指定すると、これまでのテキストに出現するかどうかに基づいて新しいトークンにペナルティが課せられ、モデルが新しいトピックを扱う可能性が高まります。
    - stop:API がそれ以上のトークンの生成を停止する、最大 4 つのシーケンス。
    :return: APIの出力
    """
    client = AOAI(
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version=os.environ.get("AZURE_API_VERSION"),
        azure_endpoint=os.environ.get("AZURE_OPENAI_API_ENDPOINT")
    )
    chat_completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temp,
        top_p=top_p,
        frequency_penalty=freq_pn,
        presence_penalty=pres_pn,
        stop=stop)
    if chat_completion.choices[0].message:
        output = chat_completion.choices[0].message.content.strip()
    else:
        output = 'No message'
    return output


# エラーハンドリング #####

# openai関連のエラーを対処する
class MaxRetryException(Exception):
    """
    Custom exception class for handling maximum retry attempts.

    Example Usage:
    ```python
    try:
        # code that may raise MaxRetryException
    except MaxRetryException:
        # handle the exception
    ```
    """
    pass


def handle_openai_errors(max_retries=6):
    """
    A decorator that wraps around another function and handles specific OpenAI errors by retrying the function a maximum number of times.

    Args:
        max_retries: The maximum number of retries for the decorated function.

    Returns:
        The decorator function with a specified max_retries.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            retry_count = 0
            while retry_count < max_retries:
                try:
                    return func(*args, **kwargs)
                # openai関連のエラーを拾う
                except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError,
                        openai.BadRequestError, openai.AuthenticationError, openai.PermissionDeniedError,
                        openai.NotFoundError, openai.UnprocessableEntityError, openai.InternalServerError
                        ) as e:
                    retry_count += 1
                    last_error = e
                    print(e)
                    time.sleep(10)
                except Exception as e:  # その他の例外をキャッチ
                    retry_count += 1
                    print(e)
                    last_error = e
                    time.sleep(10)

            raise MaxRetryException(f"Maximum retries ({max_retries}) reached. Last error: {last_error}")  # 最大再試行回数に達したら例外を送出
        return wrapper
    return decorator


# APIのやり取りをエラーハンドリングに対応させる
@handle_openai_errors(max_retries=1)
def ask_gpt_with_retry(*args, **kwargs):
    """
    Decorator that wraps around the single_ask_gpt_to_respond function and handles specific OpenAI errors by retrying the function a maximum number of times.

    Args:
        *args: Positional arguments to be passed to the single_ask_gpt_to_respond function.
        **kwargs: Keyword arguments to be passed to the single_ask_gpt_to_respond function.
    Returns:
        The result of the single_ask_gpt_to_respond function.
    Raises:
        MaxRetryException: If the maximum number of retries is reached.
    """
    return single_ask_gpt_to_respond(*args, **kwargs)


# タスク関連 #####
def excute_make_sentence(prompt,
                         sys_prompt,
                         model=os.environ.get("OPENAI_ENGINE_LLM"), max_tokens=2500, temp=0, top_p=1):
    """
    LLMで一回のやり取りをする関数
    """
    time_sta = time.perf_counter()
    try:
        output = ask_gpt_with_retry(prompt=prompt, sys_prompt=sys_prompt,
                                    model=model, max_tokens=max_tokens, temp=temp, top_p=top_p)
        time_end = time.perf_counter()
        tim = time_end - time_sta
        return output, tim, None
    except MaxRetryException as e:
        error_message = str(e)
        if "429" in error_message:
            return None, 0, "Error: API rate limit reached. Please try again later or consider upgrading your API plan."
        elif "401" in error_message:
            return None, 0, "Error: Authentication failed. Please check your API key."
        elif "503" in error_message:
            return None, 0, "Error: Service temporarily unavailable. Please try again later."
        else:
            return None, 0, f"Error: {error_message}"
    except Exception as e:
        return None, 0, f"Unexpected error: {str(e)}"
