# パッケージについて

このパッケージは、麻雀点数計算用のWebアプリのサンプル版です。Flaskを使ったシンプルな機能を実装しています。


# 環境構築

```
$ cd PROJECT_HOME
$ python3 -m venv env
$ source env/bin/activate
$ git clone git@github.com:mahjong-app/sample-web-app.git
$ cd sample-web-app
$ pip install . -e
```

## 起動

```
$ python mahjong_sample_web_app/run.py
```

http://localhost:9080 で確認できる


# テスト

## テスト環境構築

```
$ pip install -e .["test"]
```

## テストの実行

```
$ pytest -v
```

