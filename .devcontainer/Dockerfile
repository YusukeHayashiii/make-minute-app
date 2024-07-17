# dockerfile

# ベースイメージの指定
FROM python:3.12

# Add non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && apt-get clean

# システムパッケージのアップデート
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
    git \
    curl \
    fonts-ipaexfont \
    fonts-noto-cjk \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# Pythonライブラリのインストール
COPY requirements.txt .
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt \
    && rm -rf ~/.cache/pip

WORKDIR /workspace

EXPOSE 8501

# Streamlitを起動するための設定
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]