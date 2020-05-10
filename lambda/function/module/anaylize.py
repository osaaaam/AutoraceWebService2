import pandas
from sklearn.ensemble import RandomForestRegressor


class Sklearn:
    def __init__(self, mode):
        # ランダムフォレスト
        if mode == "RandomForestRegressor":
            self.model = RandomForestRegressor()

    def execute_anaylize(self, l_d_train_data, l_d_test_data, target, l_feature):
        # 訓練データをpandasにセット
        pd_df_train = pandas.DataFrame(l_d_train_data)
        # テストデータをpandasにセット
        pd_df_test = pandas.DataFrame(l_d_test_data)

        # 訓練データから学習モデルを作成
        train_output = pd_df_train[target]
        train_input = pd_df_train[l_feature]
        model = self.model.fit(train_input, train_output)

        # 作成した学習モデルで、テストデータをinputで予測
        test_input = pd_df_test[l_feature]
        l_result = model.predict(test_input)

        return l_result
