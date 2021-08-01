from typing import Tuple

import mlflow
import pandas as pd
import matplotlib
# from local
import config

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def main():
    '''
    main process
    '''
    # 固定パラメータ取得
    CSV_DATAPATH = config.CSV_DATAPATH

    # csvを読み込んで前処理済のdataframe作成
    df_preprocessed = convert_csv2preprocessed_df(CSV_DATAPATH)

    # データ分割
    train_x, test_x ,train_y, test_y = divide_xydatas(df_preprocessed)

    # tracking uri
    mlflow.set_tracking_uri('http://localhost:5000/')
    mlflow.set_experiment("/my-experiment-mlruns-artifacts")

    run = rfc_with_mlflow(train_x, test_x ,train_y, test_y)
    run_id = run.info.run_id
    print('====run_id=====>>',run_id)

    predict(run_id, CSV_DATAPATH)

    # # 実際に翌日のデータを推論する
    # loaded_model = mlflow.sklearn.load_model(f'runs:/{run_id}/model')
    # predict_x = convert_csv2predict_df(CSV_DATAPATH)

    # mlflow.set_experiment("/my-evaluations")
    # with mlflow.start_run() as run:
    #     mlflow.log_param(key='predict_date', value='7/1')
    #     predictions = loaded_model.predict([predict_x])
    #     mlflow.log_metric(key='predict_score', value=predictions[0])
    #     print('====predictions=====>>',predictions[0])    


def convert_csv2preprocessed_df(CSV_DATAPATH:str) -> pd.DataFrame:
    df = pd.read_csv(CSV_DATAPATH)
    # ホームランは2本以上打っていても1に換算
    df.loc[df['home_run'] > 0, 'home_run'] = 1
    # 翌日のHRを正解ラベルとして予測したいので、1日ずらす
    df['home_run'] = df['home_run'].shift(-1)

    # ラベル用の列だけ分ける
    train_y = df[['game_date', 'home_run']]

    # 説明変数系の前処理
    train_x = df.drop(['home_run'], axis=1)

    WINDOW_DAY = 10
    # 窓関数を使って、指定された日数の平均値を取得する
    # 指定期間の平均成績と、翌日のHRが表現されたデータになる
    df_preprocessed = pd.concat([train_x.rolling(WINDOW_DAY).mean(), train_y], axis=1)

    # na列を全て削除
    df_preprocessed.dropna(how='any', inplace=True)

    return df_preprocessed



def divide_xydatas(df_preprocessed:pd.DataFrame) -> Tuple[pd.DataFrame,pd.DataFrame,pd.DataFrame,pd.DataFrame]:
    # 前処理後のデータでさいどx,y取得
    train_x = df_preprocessed.drop(['game_date', 'home_run'], axis=1)
    train_y = df_preprocessed['home_run']

    # 分割
    (train_x, test_x ,train_y, test_y) = train_test_split(train_x, train_y, test_size = 0.3, random_state = 42)
    return train_x, test_x ,train_y, test_y


def fetch_logged_data(run_id):
    client = mlflow.tracking.MlflowClient()
    data = client.get_run(run_id).data
    tags = {k: v for k, v in data.tags.items() if not k.startswith("mlflow.")}
    artifacts = [f.path for f in client.list_artifacts(run_id, "model")]
    return data.params, data.metrics, tags, artifacts


def rfc_with_mlflow(train_x, test_x ,train_y, test_y):
    random_forest = RandomForestClassifier(max_depth=5, n_estimators=10, random_state=42)

    # enable autologging
    mlflow.sklearn.autolog()

    with mlflow.start_run() as run:
        random_forest.fit(train_x, train_y)
        metrics = mlflow.sklearn.eval_and_log_metrics(
            random_forest, test_x, test_y, prefix="val_")

    return run


def convert_csv2predict_df(CSV_DATAPATH:str) -> pd.DataFrame:
    df = pd.read_csv(CSV_DATAPATH)[0:10]
    predict_date = df.loc[:, ['game_date']]
    # print('target_dates\n', predict_date)
    # TODO:日付は誤り
    print('predict date :', predict_date.iat[0, 0])

    # 説明変数系の前処理
    predict_x = df.drop(['game_date', 'home_run'], axis=1).mean()
    return predict_x


def predict(run_id:str, CSV_DATAPATH:str) -> None:
    # 最後の訓練で作成したrunidのモデルをロード
    loaded_model = mlflow.sklearn.load_model(f'runs:/{run_id}/model')
    # predict専用の前処理
    predict_x = convert_csv2predict_df(CSV_DATAPATH)

    # predict用のExperimentを作って実行、ロギングする
    mlflow.set_experiment("/my-evaluations")
    # runの実行
    with mlflow.start_run() as run:
        # 実行日を取得する
        mlflow.log_param(key='predict_date', value='7/1')
        # 推論実行と記録
        predictions = loaded_model.predict([predict_x])
        mlflow.log_metric(key='predict_score', value=predictions[0])
        print('====predictions=====>>',predictions[0])    



if __name__ == '__main__':
    main()

