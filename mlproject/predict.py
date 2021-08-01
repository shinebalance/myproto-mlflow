import mlflow
import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def main(run_id, CSV_DATAPATH):
    '''
    main process
    '''
    # 固定パラメータ取得
    CSV_PATH = CSV_DATAPATH

    print("----------predict---------")

    # 推論評価用
    loaded_model = mlflow.sklearn.load_model(f'runs:/{run_id}/model')

    # tracking uri
    # mlflow.set_tracking_uri('http://localhost:5000/')
    # mlflow.set_experiment("/my-experiment-evaluation")

    # with mlflow.start_run() as run:

    # 推論
    predict_x = convert_csv2predict_df(CSV_PATH)
    predictions = loaded_model.predict([predict_x])

    print(predictions)

def convert_csv2predict_df(CSV_PATH:str) -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH)[0:10]
    predict_date = df.loc[:, ['game_date']]
    print('target_dates\n', predict_date[0])

    # 説明変数系の前処理
    predict_x = df.drop(['game_date', 'home_run'], axis=1).mean()
    return predict_x


if __name__ == '__main__':
    main()

