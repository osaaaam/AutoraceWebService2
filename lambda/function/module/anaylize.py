import pandas
from sklearn.ensemble import RandomForestRegressor


class Sklearn:

    def __init__(self, mode):
        # ランダムフォレスト
        if mode == "RandomForestRegressor":
            self.model = RandomForestRegressor()

    def execute_anaylize(self, train_data, test_data, anaylize_target, list_feature):
        # 訓練データをpandasにセット
        pd_df_train = pandas.DataFrame(train_data)
        # テストデータをpandasにセット
        pd_df_test = pandas.DataFrame(test_data)

        # 訓練データから学習モデルを作成
        train_output = pd_df_train[anaylize_target]
        train_input = pd_df_train[list_feature]
        model = self.model.fit(train_input, train_output)

        # 作成した学習モデルで、テストデータをinputで予測
        test_input = pd_df_test[list_feature]
        result_predict = model.predict(test_input)

        return result_predict
