# MLflow & Airflow Prototyping repo
* MLflowの理解がてら、トイプロブレム的なデータ収集->モデル訓練->推論を一通り書いたリポジトリ
  * モデルそのものの有用性は度外視(かなり適当な前処理＋RandomForestをしているだけ)
* Pythonの各処理はAirflowのDAGに設定して実行する
  * 本来cronで出来るレベルのことをDocker-compose内で完結させるためだけにAirflowを使っており、厳密にはAirflowが必要なほど複雑なワークフローは実行していない

## How to run
* とりあえず可搬性高く何も考えず動かせるように、Docker-composeで動かせるようにした
  * ただしスクレイピングのコードが取得先URLの構成依存 ＆ 自分が実験した時のURLはgitにない`.env`で管理しているので、仮に関係ないURLに対して利用する場合はこの部分は適宜変更が必要
```
docker-compose -f docker-compose.yml up --build
# Airflowのschedulerを利用したい場合は、コンテナ内に入って以下手順でscheduler起動
airflow scheduler
```

## Docker-compose構成の解説
### mlflow-server
  * MLflow Tracking Serverを構成＆CMDで起動している
  * artifactsはDcokerでマウントしているローカルパスに対して吐き出すようになっている
  * DBはsqliteを利用
### airflow-server
  * Airflowを構成＆CMDで起動している
    * ただし、schedulerは別途起動が必要。DAGをキックしても動かない
    * DBはsqliteを利用
  * `pipenv`を用いて`/scrape`と`/mlporject`以下のデータ収集・モデル訓練と推論のスクリプト実行環境を構築している


## 各フォルダについて
### [airflow-server](airflow-server)
* airflow-serverコンテナのDockerflieと、実行時には`AIRFLOW_HOME`以下をマウントしてAirflow関連のファイルも保管
* dags以下にワークフローを作成して設定できる

### [data](data)
* scrapeの処理で取得したcsvデータが保管される(親から確認しやすいようマウント済)

### [logs](logs)
* scrapeとmlporojectのloggerから吐き出したlog(親から確認しやすいようマウント済)

### [mlflow-server](mlflow-server)
* mlflow-serverコンテナのDockerflieと、sqliteファイルを保管

### [mlproject](mlproject)
* 任意のMLプロジェクト実行スクリプトをもつ
  * csvデータを読み込んでモデル訓練、推論を行う
  * 結果をmlflow-serverに書き込む
* `.env`の書き方例
```
CSV_DATAPATH = './data/hogehoge.csv'
```

### [mlruns-artifacts](mlruns-artifacts)
* mlprojectが実行された際に生成されるArtifactの置き場所(model等々)

### [scrape](scrape)
* 任意のデータスクレピングスクリプトをもつ
  * 任意のURLに対してスクレイピングを行い、必要なデータをcsv化する
* `.env`の書き方例
```
TARGET_URL = 'https://hogehoge.com/hogepage'
CSV_SAVEPATH = './data/hogehoge.csv'
```

## ローカル稼働時のPipenv
* Pipfileも利用できる
* Docker-composeでMLflowを建てておけば単純にpipenvから実験もできる


## ToDo

- [x] Airflowコンテナにpipenv実行環境を追加する
  - [x] Dockerfileにpipenv環境の構築を追加する
  - [x] pipenvのコマンドから各処理を行えるようディレクトリ整理
  - [x] DAGに設定してスケジュール実行する
- [ ] リモート環境に移行する
  - [ ] Docker-compose環境をマシン上につくる
  - [ ] 移行して動かす
  - [ ] 終わり？


```
pipenv lock -r >> airflow-server/requirements.txt
```

# EOF