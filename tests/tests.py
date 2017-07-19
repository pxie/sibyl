import os
import json
import sys
sys.path.append(os.getcwd())

import unittest
import sibyl.data_generator as dg
import sibyl.analytic as ax
from sibyl.logger import log


class TestDataGenerator(unittest.TestCase):

    def test_rand(self):
        count = 100
        data = dg.rand(count)
        self.assertEqual(len(data["values"]), count)
        for item in data["values"]:
            self.assertFalse(self.__greater(item[1], 0.05 * item[0] + 1))

    def __greater(self, num1, num2):
        return True if num1 > num2 else False


class TestAnalytic(unittest.TestCase):

    def test_predict(self):
        count = 100
        data = dg.rand(count)
        linear_predict = ax.LinearPredict()
        predict_json = linear_predict.predict(json.dumps(data))
        log.debug("predict_json: %s", predict_json)

    def test_draw(self):
        count = 100
        data = dg.rand(count)

        # calcuate formula
        linear_predict = ax.LinearPredict()
        df, regr = linear_predict.linear_regression(data["values"])
        print(df)

        # predict next 25% data points
        step = df["ts"][1] - df["ts"][0]
        total = int(round(len(df["ts"]) / 4))
        tslist = []
        for i in range(total):
            log.debug("df.tail(1)['ts']: %s", df.tail(1)["ts"])
            tslist.append(df.tail(1)["ts"] + step * (i + 1))

        predic_df = linear_predict.do_predict(tslist, regr)

        linear_predict.draw(df, predic_df, regr)


if __name__ == "__main__":
    unittest.main()
