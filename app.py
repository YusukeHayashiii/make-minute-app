# basic
import sys
from pathlib import Path
import warnings
# streamlit
from st_pages import Page, Section, show_pages, add_page_title
# original
from st_components.st_session_states import initialize_session_state

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
    # セッションステートの初期化
    initialize_session_state()
    main()
