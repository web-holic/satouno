import pyxel
import webbrowser
from module.booker import Booker

class App:
    def __init__(self):
        pyxel.init(150, 82)
        pyxel.load("satouno.pyxres")
        pyxel.mouse(True)
        self.init_game()
        pyxel.run(self.update, self.draw)

    def chagepos(self):
        num = self.pos
        while self.pos == num:
            num = pyxel.rndi(0, 2)
        self.next = num

    def update(self):
        # 現在選択されているシーンのupdateを読み込みます。
        if self.my_gamemode == 0:
            self.update_title()
        elif self.my_gamemode == 1:
            self.update_main()
        elif self.my_gamemode == 2:
            self.update_end()
        Booker.do()

    def update_title(self):

        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y):
            self.my_gamemode = 1

    def update_main(self):
        self.time = self.time - 0.1
        if self.time < 0:
            self.my_gamemode = 2

        if self.state == 0:
            if self.timerFlag == 0:
                if self.pos == 1:
                    if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                        self.next = 2
                        self.state = 1
                        # self.timerFlag = 0
                    if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                        self.next = 0
                        self.state = 1
                        # self.timerFlag = 0
                else:
                    self.current = self.pos
                    self.chagepos()
                    Booker.add(self, 'state', 1, 10, 1)
                    Booker.add(self, 'timerFlag', -1, 10, 1)
                    self.timerFlag = 1
        elif self.state == 1:
            if self.timerFlag == 0:
                self.pos = self.next
                if self.pos == 1:
                    if self.soundFlag == 0:
                        pyxel.play(0, 1)
                        self.soundFlag = 1
                    if pyxel.btnp(pyxel.KEY_RIGHT):
                        self.next = 2
                        self.state = 2
                        self.soundFlag = 0

                    if pyxel.btnp(pyxel.KEY_LEFT):
                        self.next = 0
                        self.state = 2
                        self.soundFlag = 0
                else:
                    pyxel.play(0, 1)
                    self.chagepos()
                    Booker.add(self, 'state', 1, 10, 1)
                    Booker.add(self, 'timerFlag', -1, 10, 1)
                    self.timerFlag = 1
        elif self.state == 2:
            if self.timerFlag == 0:
                pyxel.play(0, 2)
                self.current = self.pos
                self.pos = self.next
                self.chagepos()
                Booker.add(self, 'state', 1, 10, 1)
                Booker.add(self, 'timerFlag', -1, 10, 1)
                self.timerFlag = 1
            if self.pos != 1:
                if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y):
                        self.current = self.pos
                        self.score += 10
                        self.state = 3
            if self.pos == 1:
                if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y):
                        self.score -= 50
        elif self.state == 3:
            if self.timerFlag == 0:
                self.current = self.pos
                if self.pos != 1:
                    if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y):
                            self.score += 10
                            self.state = 4
                else:
                    self.state = 4
        elif self.state == 4:
            if pyxel.btnp(pyxel.KEY_SPACE):
                    self.score -= 50
            if self.timerFlag == 0:
                pyxel.play(0, 0)
                if self.pos != 1:
                    Booker.add(self, 'state', -3, 10, 1)
                else:
                    Booker.add(self, 'state', -4, 10, 1)
                Booker.add(self, 'timerFlag', -1, 10, 1)
                self.timerFlag = 1

    def update_end(self):
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y):
            self.init_game()
            self.my_gamemode = 0

    def draw(self):
        # こちらでは，画面の描画処理を行っています。
        # updateと同じく、GAMEMODEで実行される描画を変更しています。
        pyxel.cls(10)
        if self.my_gamemode == 0:
            self.draw_title()

        elif self.my_gamemode == 1:
            self.draw_main()

        elif self.my_gamemode == 2:
            self.draw_end()

    def draw_title(self):
        pyxel.blt(0, 10, 0, 0, 64, 150, 48)
        pyxel.text(15, 70 , 'Push Space or GamePad Button' , 5)
    def draw_main(self):
        # メインのゲーム画面の描画です
        pyxel.text(5, 5, 'SCORE ' + str(self.score), 5)
        pyxel.text(5, 12, 'TIME' , 5)
        if self.time < 60:
            pyxel.rect(25, 12, self.time, 5, 8)
        else:
            pyxel.rect(25, 12, self.time, 5, 5)


        self.draw_arrow()
        pyxel.blt(23, 35, 0, 0, 0, 16, 16)
        pyxel.blt(69, 35, 0, 0, 0, 16, 16)
        pyxel.text(71, 52, "YOU", 5)
        pyxel.blt(115, 35, 0, 0, 0, 16, 16)

        if (self.state == 1):
            pyxel.blt((self.current * 46) + 7, 20, 0, 0, 16, 48, 16)
        elif (self.state == 2):
            pyxel.blt((self.current * 46) + 7, 20, 0, 0, 32, 48, 16)
        elif (self.state == 4):
            if self.pos == 0:
                pyxel.blt(53, 20, 0, 0, 48, 48, 16)
                pyxel.blt(99, 20, 0, 0, 48, 48, 16)

                pyxel.blt(69, 35, 0, ((pyxel.frame_count %
                          2) * 16 + 16), 0, 16, 16)
                pyxel.blt(115, 35, 0, ((pyxel.frame_count %
                          2) * 16 + 16), 0, 16, 16)
            elif self.pos == 1:
                pyxel.blt(7, 20, 0, 0, 48, 48, 16)
                pyxel.blt(99, 20, 0, 0, 48, 48, 16)

                pyxel.blt(23, 35, 0, ((pyxel.frame_count %
                          2) * 16 + 16), 0, 16, 16)
                pyxel.blt(115, 35, 0, ((pyxel.frame_count %
                          2) * 16 + 16), 0, 16, 16)
            elif self.pos == 2:
                pyxel.blt(7, 20, 0, 0, 48, 48, 16)
                pyxel.blt(53, 20, 0, 0, 48, 48, 16)

                pyxel.blt(69, 35, 0, ((pyxel.frame_count %
                          2) * 16 + 16), 0, 16, 16)
                pyxel.blt(23, 35, 0, ((pyxel.frame_count %
                          2) * 16 + 16), 0, 16, 16)
    def draw_end(self):
        pyxel.text(64, 10 , 'TIME UP' , 5)
        pyxel.text(45, 25 , 'Your Score: ' + str(self.score) , pyxel.frame_count % 16)
        pyxel.blt(23, 40, 0, 64, 0, 16, 16)
        pyxel.text(49, 45 , '<- Share Score' , 5)
        pyxel.text(15, 70 , 'Push Space or GamePad Button' , 5)

    def draw_arrow(self):
        pyxel.blt((self.pos * 46) + 23, 60, 0, 48, 0, 16, 16)

    def init_game(self):
        self.my_gamemode = 0
        self.score = 0
        self.state = 0
        self.current = 0
        self.start = 0
        self.next = 0
        self.pos = 0
        self.timerFlag = False
        self.soundFlag = 0
        self.time = 120

App()
