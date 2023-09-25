import pyxel

# Bookerクラス：値の変化を予約する
# イベント登録時：update()内でBooker.add()を使う
# Booker.add(対象インスタンス(obj), の変数名(str), 変化させたい量(int),
#   変化開始時間(単位フレーム後開始)(int), 変化に要する時間(0<int), イージング(str))
# イージングはCubicなベジェ曲線を使用(カスタマイズ可)、デフォルトは'linear'
# イベント出力時：Booker.do()をBooker.add()より後ろに記述し、毎フレーム実行する
# 配布元：https://github.com/namosuke/pyxel_class_booker


class Booker:
    books = []
    fr = 0

    @classmethod
    def add(cls, obj, key, value, start_time, end_time, easing='linear'):
        cls.books.append([
            cls.fr + start_time,
            end_time,
            key,
            value,
            0,  # 最後の差分
            easing,
            obj
        ])

    @classmethod
    def do(cls):
        # 逆順にアクセス
        for i in range(len(cls.books) - 1, -1, -1):
            b = cls.books[i]  # 予約情報
            if b[0] <= cls.fr:
                # イージング処理参考　http://nakamura001.hatenablog.com/entry/20111117/1321539246
                if b[5] == 'linear':
                    diff = b[3] * (cls.fr - b[0]) / b[1]
                elif b[5] == 'ease in':
                    t = (cls.fr - b[0]) / b[1]
                    diff = b[3] * t*t*t
                elif b[5] == 'ease out':
                    t = (cls.fr - b[0]) / b[1]
                    t -= 1
                    diff = b[3] * (t*t*t + 1)
                elif b[5] == 'ease in out':
                    t = (cls.fr - b[0]) / (b[1] / 2)
                    if t < 1:
                        diff = (b[3] / 2) * t*t*t
                    else:
                        t -= 2
                        diff = (b[3] / 2) * (t*t*t + 2)

                # 小数誤差を無くすため、毎回整数値を反映させている
                b[6].__dict__[b[2]] -= b[4]
                b[6].__dict__[b[2]] += round(diff)
                b[4] = round(diff)

            if b[0] + b[1] <= cls.fr:
                del cls.books[i]

        cls.fr += 1
