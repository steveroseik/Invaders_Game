from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.image import Image
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.vector import Vector
from kivy.core.audio import SoundLoader
import random

steps = 10
GamePause = True


class Invader(Widget):
    image_path = StringProperty()
    posX = 0
    posY = 0
    timer = 0
    resistance = 1
    dead = False
    ov_anim = ['atlas://d1Anim.atlas/',
               'atlas://d2Anim.atlas/',
               'atlas://d3Anim.atlas/',
               'atlas://d4Anim.atlas/',
               'atlas://d5Anim.atlas/',
               'atlas://d6Anim.atlas/']
    eType = 0
    src = StringProperty(ov_anim[eType] + 'frame1')
    frames = []
    frame_count = 0
    f_index = 1
    f_end = 3
    ready = False

    def __init__(self, e, **kwargs):
        super().__init__(**kwargs)
        if e == 1:
            self.eType = 0
            self.setSize(200, 200)
            self.f_index = 1
            self.f_end = 3
        elif e == 2:
            self.eType = 1
            self.setSize(200, 200)
            self.f_index = 1
            self.f_end = 3
        elif e == 3:
            self.eType = 2
            self.setSize(200, 200)
            self.f_index = 1
            self.f_end = 3
        elif e == 4:
            self.eType = 3
            self.setSize(200, 200)
            self.f_index = 1
            self.f_end = 3
        elif e == 5:
            self.eType = 4
            self.setSize(150, 150)
            self.f_index = 1
            self.f_end = 3
        elif e == 6:
            self.eType = 5
            self.setSize(150, 150)
            self.f_index = 1
            self.f_end = 4
        else:
            self.eType = 5
            self.setSize(150, 150)
            self.f_index = 5
            self.f_end = 4

        self.frame_count = self.f_index
        for i in range(self.f_index, self.f_index + self.f_end):
            self.frames.append('frame' + str(i))
        self.ready = True

    def setPos(self, x, y):
        self.pos = (x, y)

    def setSize(self, w, h):
        self.size = (w, h)

    def animate(self, dt):
        if self.ready:
            self.frame_count += 1
            if self.frame_count >= (self.f_index + self.f_end) - 1:
                self.frame_count = self.f_index
            key = self.frames[self.frame_count]
            self.src = self.ov_anim[self.eType] + key

    def setResistance(self, r):
        self.resistance = r

    def update(self, dt):
        if not GamePause:
            if self.timer == 0:
                self.timer = 200
                self.posX = random.choice([7, -7, 0])
                if self.posX != 0:
                    self.posY = random.choice([7, -7, 0])
                else:
                    self.posY = random.choice([7, -7])

            else:
                self.timer -= 1

            self.pos = ((self.pos[0] + self.posX), (self.pos[1] + self.posY))

    def collision(self, height, width):
        if not self.dead:
            if self.pos[1] < 0 or (self.pos[1] + self.size[1]) > height:
                if self.pos[1] > height / 2:
                    self.pos = (self.pos[0], height - self.size[1] - 5)
                else:
                    self.pos = (self.pos[0], 5)
                self.posY *= -1
            if self.pos[0] < 0 or (self.pos[0] + self.size[0]) > width:
                if self.pos[0] > width / 2:
                    self.pos = (width - self.size[0] - 5, self.pos[1])
                else:
                    self.pos = (5, self.pos[1])
                self.posX *= -1

    def gotShot(self, e2):
        r1x = self.pos[0]
        r1y = self.pos[1]
        r2x = e2.pos[0]
        r2y = e2.pos[1]
        r1w = self.size[0]
        r1h = self.size[1]
        r2w = e2.size[0]
        r2h = e2.size[1]

        if (r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y):
            return True
        return False

    def isDead(self):
        return self.dead

    def dShield(self):
        if self.resistance > 0:
            self.resistance -= 1
            self.size = (self.size[0] - 20, self.size[1] - 20)
        else:
            self.kill()

    def kill(self):
        self.size = (0, 0)
        self.dead = True
        self.disabled = True


class Player(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    ov_anim = 'atlas://playerAnim.atlas/'
    src = StringProperty('atlas://playerAnim.atlas/frame1')
    frames = []
    for i in range(1, 99):
        frames.append('frame' + str(i))
    frame_count = 0

    def animate(self, dt):
        self.frame_count += 1
        if self.frame_count >= len(self.frames):
            self.frame_count = 0
        key = self.frames[self.frame_count]
        self.src = self.ov_anim + key

    def collides(self, e2):
        r1x = self.pos[0]
        r1y = self.pos[1]
        r2x = e2.pos[0]
        r2y = e2.pos[1]
        r1w = self.size[0] / 2
        r1h = self.size[1] / 2
        r2w = e2.size[0] / 2
        r2h = e2.size[1] / 2

        if (r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y):
            return True
        else:
            return False

    def move(self):
        global GamePause
        if not GamePause:
            self.pos = Vector(self.velocity) + self.pos

    def reset(self):
        self.pos = ((Window.width / 2) - 50, 200)


class Bullet(Rectangle):
    bullet_speed = 15
    velocity_x = 0
    velocity_y = 0
    dead = False

    def setDirection(self, type_n):
        if type_n == 0:
            self.velocity_x = self.bullet_speed - 5
            self.velocity_y = self.bullet_speed
        elif type_n == 1:
            self.velocity_x = self.bullet_speed - 10
            self.velocity_y = self.bullet_speed
        elif type_n == 2:
            self.velocity_x = 0
            self.velocity_y = self.bullet_speed
        elif type_n == 3:
            self.velocity_x = -self.bullet_speed + 10
            self.velocity_y = self.bullet_speed
        elif type_n == 4:
            self.velocity_x = -self.bullet_speed + 5
            self.velocity_y = self.bullet_speed

    def shoot(self, height):
        self.pos = (self.pos[0] + self.velocity_x, self.pos[1] + self.velocity_y)

    def kill(self):
        self.size = (0, 0)
        self.dead = True

    def isDead(self):
        return self.dead


class GameWidget(Widget):
    player = ObjectProperty(None)
    go_string = StringProperty('')
    step_timer = 0
    Window.clearcolor = (0, 0, 1, 100)
    bullets = []
    enemyList = []
    e_level = NumericProperty(1)
    allDead = False
    bg_texture = ObjectProperty(None)
    hint_text = StringProperty('Press Space to Begin')
    up_k = False
    down_k = False
    left_k = False
    right_k = False

    def scroll_texture(self, time_passed):
        global GamePause
        if not GamePause:
            self.bg_texture.uvpos = (self.bg_texture.uvpos[0], (self.bg_texture.uvpos[1]) % Window.height - time_passed)
            # redraw the image.
            texture = self.property('bg_texture')
            texture.dispatch(self)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._keyboard = Window.request_keyboard(self._on_keyboard_close, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)
        self.bg_texture = Image(source='star_bg.png').texture
        self.bg_texture.wrap = 'repeat'
        self.bg_texture.uvsize = (1, -1)
        self.player.pos = ((Window.width / 2) - 50, 200)
        self.gun1shoot = SoundLoader.load('laser6.mp3')
        with self.canvas:
            for i in range(0, self.e_level):
                self.enem = self.generateEnemy()
                Clock.schedule_interval(self.enem.update, 1.0 / 60.0)
                self.enemyList.append(self.enem)

        Clock.schedule_interval(self.player.animate, 1.0 / 10.0)

    def GunShoot(self, type_n):
        if type_n == 0:
            with self.canvas.before:
                self.bull = Bullet(source='bullet.png',
                                   pos=((self.player.x + 0.5 * self.player.width), self.player.y + self.player.height),
                                   size=(10, 40))
                self.bull.setDirection(2)
                self.bullets.append(self.bull)

        elif type_n == 1:
            with self.canvas.before:
                self.bull1 = Bullet(source='bullet.png',
                                    pos=(
                                        (self.player.x + 0.5 * self.player.width) - 10,
                                        self.player.y + self.player.height),
                                    size=(10, 40))
                self.bull2 = Bullet(source='bullet.png',
                                    pos=(
                                        (self.player.x + 0.5 * self.player.width) + 10,
                                        self.player.y + self.player.height),
                                    size=(10, 40))
                self.bull2.setDirection(2)
                self.bull1.setDirection(2)
                self.bullets.append(self.bull1)
                self.bullets.append(self.bull2)

        elif type_n == 2:
            with self.canvas.before:
                self.bull1 = Bullet(source='bullet.png', pos=(
                    (self.player.x + 0.5 * self.player.width) - 5, self.player.y + self.player.height),
                                    size=(10, 40))
                self.bull2 = Bullet(source='bullet.png',
                                    pos=((self.player.x + 0.5 * self.player.width), self.player.y + self.player.height),
                                    size=(10, 40))
                self.bull3 = Bullet(source='bullet.png',
                                    pos=(
                                        (self.player.x + 0.5 * self.player.width) + 5,
                                        self.player.y + self.player.height),
                                    size=(10, 40))
                self.bull1.setDirection(3)
                self.bull2.setDirection(2)
                self.bull3.setDirection(1)
                self.bullets.append(self.bull1)
                self.bullets.append(self.bull2)
                self.bullets.append(self.bull3)

        elif type_n == 3:
            with self.canvas.before:
                indent = -20
                for bType in range(0, 5):
                    self.bull = Bullet(source='bullet.png',
                                       pos=((self.player.x + 0.5 * self.player.width) - indent,
                                            self.player.y + self.player.height),
                                       size=(10, 40))
                    self.bull.setDirection(bType)
                    indent += 10
                    self.bullets.append(self.bull)

    def generateEnemy(self):
        randW = random.randint(200, Window.width - 200)
        randH = random.randint(500, Window.height - 200)
        if self.e_level > 8:
            char = self.e_level % 8 + 1
        else:
            char = self.e_level
        if self.e_level > 3:
            res = 3
        else:
            res = self.e_level

        if self.e_level > 5:
            self.var = random.choice([1, 2, 3, 4, 5, 6, 7])
        else:
            self.var = self.e_level

        self.enem = Invader(self.var)
        self.enem.setPos(randW, randH)
        Clock.schedule_interval(self.enem.animate, 0.2)
        self.enem.setResistance(res)

        return self.enem

    def _on_keyboard_close(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_up(self, keyboard, keycode):
        if keycode[1] == 'w':
            self.up_k = False
        if keycode[1] == 's':
            self.down_k = False
        if keycode[1] == 'a':
            self.left_k = False
        if keycode[1] == 'd':
            self.right_k = False
        pass

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        global GamePause

        if text == ' ':

            if not GamePause or self.go_string != 'GAME OVER':
                self.gun1shoot.play()
                if self.e_level > 6:
                    self.GunShoot(3)
                elif self.e_level > 4:
                    self.GunShoot(2)
                elif self.e_level > 2:
                    self.GunShoot(1)
                else:
                    self.GunShoot(0)

            if self.go_string == 'GAME OVER':
                self.restart()
                self.player.reset()
            if self.go_string == 'YOU WON!':
                self.levelUp()
                self.player.reset()
            self.hint_text = ''
            self.go_string = ''
            GamePause = False

        if not GamePause:
            if text == 'w':
                if self.left_k or self.right_k:
                    self.player.velocity = Vector(self.player.velocity_x, steps)

                else:
                    self.player.velocity = Vector(0, steps)
                    self.up_k = True
            if text == 's':
                if self.left_k or self.right_k:
                    self.player.velocity = Vector(self.player.velocity_x, -steps)
                else:
                    self.player.velocity = Vector(0, -steps)
                    self.down_k = True
            if text == 'a':
                if self.up_k or self.down_k:
                    self.player.velocity = Vector(-steps, self.player.velocity_x)
                else:
                    self.player.velocity = Vector(-steps, 0)
                    self.left_k = True
            if text == 'd':
                if self.up_k or self.down_k:
                    self.player.velocity = Vector(steps, self.player.velocity_x)
                else:
                    self.player.velocity = Vector(steps, 0)
                    self.right_k = True

    def restart(self):
        for eac in self.enemyList:
            eac.kill()
        for eax in self.bullets:
            eax.kill()
        self.enemyList.clear()
        self.bullets.clear()
        self.allDead = False
        self.e_level = 1
        self.go_string = ''
        with self.canvas:
            for i in range(0, self.e_level):
                self.enem = self.generateEnemy()
                Clock.schedule_interval(self.enem.update, 1.0 / 60.0)
                self.enemyList.append(self.enem)

    def levelUp(self):
        for eac in self.enemyList:
            eac.kill()
        for eax in self.bullets:
            eax.kill()
        self.enemyList.clear()
        self.bullets.clear()
        self.e_level += 1
        self.allDead = False
        with self.canvas:
            print('Enemey: ' + str(self.e_level))
            for i in range(0, self.e_level):
                self.enem = self.generateEnemy()
                Clock.schedule_interval(self.enem.update, 1.0 / 60.0)
                self.enemyList.append(self.enem)
                print('(' + str(self.enem.f_index) + ', ' + str(self.enem.f_end) + ')')

    def checkPlayerBoundaries(self):
        if self.player.y <= 2 or (self.player.y + self.player.height) - 2 >= self.height:
            if self.player.pos[1] > Window.height / 2:
                self.player.pos = (self.player.pos[0], Window.height - 105)
            else:
                self.player.pos = (self.player.pos[0], 5)
            self.player.velocity_y *= -1
            self.player.velocity_y /= 10
            return True
        if self.player.x <= 2 or (self.player.x + self.player.width) - 2 >= self.width:
            if self.player.pos[0] > Window.width / 2:
                self.player.pos = (Window.width - 105, self.player.pos[1])
            else:
                self.player.pos = (5, self.player.pos[1])

            self.player.velocity_x *= -1
            self.player.velocity_x /= 10
            return True
        return False

    def update(self, dt):

        if not self.checkPlayerBoundaries():
            self.player.move()
        for enemy in self.enemyList:
            enemy.collision(self.height, self.width)
        for i in self.bullets:
            i.shoot(self.height)
            for enemy in self.enemyList:
                if enemy.gotShot(i):
                    if not i.isDead():
                        enemy.dShield()
                        i.kill()
            if i.pos[1] > self.height:
                self.remove_widget(i)
        self.checkPlayerBoundaries()

        counter = 0
        for e in self.enemyList:
            if e.isDead():
                counter += 1
        if counter == len(self.enemyList):
            self.allDead = True

        global GamePause
        if self.allDead:
            GamePause = True
            self.go_string = 'YOU WON!'
            self.hint_text = 'Press Space to Enter Next Level'

        for eac in self.enemyList:
            if self.player.collides(eac):
                if not eac.isDead():
                    GamePause = True
                    self.go_string = 'GAME OVER'
                    self.hint_text = 'Press Space to Restart'


class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        game = GameWidget()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        Clock.schedule_interval(game.scroll_texture, 1.0 / 40.0)
        return game

    pass


if __name__ == '__main__':
    app = MyApp()
    app.run()
