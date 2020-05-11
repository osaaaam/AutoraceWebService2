import pandas
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import LinearRegression



class Sklearn:
    def __init__(self, mode):
        # ランダムフォレスト
        if mode == "RandomForestRegressor":
            self.model = RandomForestRegressor()
        # リッジ回帰 不要な特徴量を削る 相関の高い特徴量をどちらも残すことができない
        elif mode == "Ridge":
            self.model = Ridge(alpha=0.1)
        # ラッソ回帰 過学習を防ぐ 特徴量の削減(係数を0にする)ことには向いてない
        elif mode == "Lasso":
            self.model = Lasso(alpha=0.1)
        # リッジ回帰とラッソ回帰を合体
        elif mode == "ElasticNet":
            self.model = ElasticNet(alpha=0.1, l1_ratio=0.5)
        # 線形回帰
        elif mode == "LinearRegression":
            self.model = LinearRegression()

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

        print(l_result)

        return l_result
