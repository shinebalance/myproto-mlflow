# MLFlow & Airflow Prototyping repo
* MLFlowの理解がてら、トイプロブレム的なデータ収集->モデル訓練->推論を一通り書いたリポジトリ
  * モデルそのものの有用性は気にしない
* Pythonの実行ジョブはAirflowを使って実行する(予定)

## How to run
* 深く何も考えず動かせるように、Docker-composeを準備
```
docker-compose -f docker-compose.yml up --build
```

## 各コンポーネントについて

### mlflow-server
* mlflowのサーバーとして
  * artifactはローカルのパスをClientと共有して使う方式、S3とかはマウントしない

### Airflow-server
* DAGのスケジュール実行をする

### scrape(移行予定)
* 任意のデータスクレピングスクリプトをもつ
  * 任意のURLに対してスクレイピングを行い、必要なデータをcsv化する

### mlproject(移行予定)
* 任意のMLプロジェクト実行スクリプトをもつ
  * csvデータを読み込んでモデル訓練、推論を行う
  * 結果をmlflow-serverに書き込む


## ToDo

- [ ] Airflowコンテナにpipenv実行環境を追加する
  - [ ] Dockerfileにpipenv環境の構築を追加する
  - [ ] pipenvのコマンドから各処理を行えるようディレクトリ整理
  - [ ] DAGに設定してスケジュール実行する
- [ ] リモート環境に移行する
  - [ ] Docker-compose環境をマシン上につくる
  - [ ] 移行して動かす
  - [ ] 終わり？


# EOF