import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import StandardScaler


class xgbModel:
    def __init__(self):
        # 读取数据集
        self.data = pd.read_excel("数据集1.xlsx")
        self.trainning()

    def trainning(self):
        # 划分特征和标签
        X = self.data.iloc[:, :-1].values
        y = self.data.iloc[:, -1].values

        # 特征缩放
        self.sc_X = StandardScaler()
        self.sc_y = StandardScaler()
        X = self.sc_X.fit_transform(X)
        y = self.sc_y.fit_transform(y.reshape(-1, 1))

        # 建立XGBoost模型
        self.xgbr = xgb.XGBRegressor(n_estimators=100,
                                learning_rate=0.1,
                                gamma=0.001,
                                subsample=0.8,
                                colsample_bytree=0.8,
                                max_depth=5,
                                seed=42)

        self.xgbr.fit(X, y)

    def predict(self, feature1, feature2, feature3, feature4, feature5, feature6):
        # 将特征值转换为模型所需的格式
        features = [[feature1, feature2, feature3, feature4, feature5, feature6]]
        features_scaled = self.sc_X.transform(features)

        # 使用训练好的模型进行预测
        prediction_scaled = self.xgbr.predict(features_scaled)
        prediction = self.sc_y.inverse_transform(prediction_scaled)
        return prediction
