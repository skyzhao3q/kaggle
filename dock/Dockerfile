FROM ubuntu:14.04
WORKDIR root
EXPOSE 8080

# update and add required repositories
RUN apt-get -y update
RUN apt-get -y install software-properties-common
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN add-apt-repository ppa:coolwanglu/pdf2htmlex
RUN apt-get -y update

# install common packages
RUN apt-get -y install build-essential cmake git pkg-config wget vim curl
RUN apt-get -y install zlib1g-dev \
                       libssl-dev \
                       libreadline-dev \
                       libyaml-dev \
                       libxml2-dev \
                       libxslt-dev \
                       libncurses5-dev \
                       libncursesw5-dev

# pyenv のインストール
RUN git clone git://github.com/yyuu/pyenv.git /root/.pyenv
RUN git clone https://github.com/yyuu/pyenv-pip-rehash.git /root/.pyenv/plugins/pyenv-pip-rehash
ENV PYENV_ROOT /root/.pyenv
ENV PATH $PYENV_ROOT/bin:$PATH
RUN echo 'eval "$(pyenv init -)"' >> .bashrc

# anaconda のインストール
ENV ANACONDA_VER 4.1.1
RUN pyenv install anaconda3-$ANACONDA_VER
RUN pyenv global anaconda3-$ANACONDA_VER
ENV PATH $PYENV_ROOT/versions/anaconda3-$ANACONDA_VER/bin:$PATH

# ライブラリのアップデート
RUN conda update -y conda
RUN pip install --upgrade pip