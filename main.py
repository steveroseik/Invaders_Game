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
Window.size = (1280, 720)
Window.top = 50
Window.left = 50

class Planet(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    image_path = StringProperty()
    posX = 0
    posY = 0
    size_x = 0
    size_y = 0
    timer = 0
    resistance = 1
    dead = False
    ov_anim = ['atlas://p1Anim.atlas/',
               'atlas://p2Anim.atlas/',
               'atlas://p3Anim.atlas/',
               'atlas://p4Anim.atlas/',
               'atlas://p5Anim.atlas/']
    eType = 0
    src = StringProperty(ov_anim[eType] + 'frame0')
    frames = []
    frame_count = 0
    f_index = 0
    f_end = 50
    ready = False

    def __init__(self, e, **kwargs):
        super().__init__(**kwargs)
        randY = random.choice([1.5, 2, 2.5, 3, 3.5, 4])
        self.velocity = (0, -randY)
        self.opacity = 0.3
        if e == 1:
            self.eType = 0
            self.setSize(100, 100)
        elif e == 2:
            self.eType = 1
            self.setSize(100, 100)
        elif e == 3:
            self.eType = 2
            self.setSize(150, 150)
        elif e == 4:
            self.eType = 3
            self.setSize(100, 100)

        elif e == 5:
            self.eType = 4
            self.setSize(75, 75)

        self.pos = (random.randrange(200, Window.width) - 100, Window.height)

        self.frame_count = self.f_index
        for i in range(self.f_index, self.f_index + self.f_end):
            self.frames.append('frame' + str(i))
        self.ready = True

    def setSize(self, w, h):
        self.size_x = w
        self.size_y = h
        self.size = (w, h)

    def animate(self, dt):
        if self.ready:
            self.frame_count += 1
            if self.frame_count >= (self.f_index + self.f_end) - 1:
                self.frame_count = self.f_index

            key = self.frames[self.frame_count]
            self.src = self.ov_anim[self.eType] + key

    def move(self):
        if self.pos[1] <= -200:
            self.size = (0, 0)
            self.dead = True
        self.pos = Vector(self.velocity) + self.pos

    def isDead(self):
        return self.dead


class Invader(Widget):
    image_path = StringProperty()
    posX = 0
    posY = 0
    size_x = 0
    size_y = 0
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
        self.size_x = w
        self.size_y = h
        self.size = (w, h)

    def hide(self):
        self.size = (0, 0)

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
    ov_anim = 'atlas://playerAnim3.atlas/'
    src = StringProperty('atlas://playerAnim.atlas/frame1')
    frames = []
    for i in range(0, 100):
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

    def kill(self):
        # self.pos = (0, 0)
        self.velocity = Vector(0, 0)
        self.size = (0, 0)
        self.disabled = True

    def hide(self):
        self.opacity = 0

    def show(self):
        self.opacity = 1

class Bullet(Widget):
    bullet_speed = 15
    velocity_x = 0
    velocity_y = 0
    dead = False
    srcList = ['bullet.png',
               'bullet2.png',
               'bullet3.png']
    src = StringProperty('bullet.png')

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

    def setType(self, e):
        self.src = self.srcList[e]

class GameWidget(Widget):
    player = ObjectProperty(None)
    go_string = StringProperty('')
    title_s = StringProperty('SELECT YOUR SHIP \n arrow right or left')
    step_timer = 0
    Window.clearcolor = (0, 0, 0, 100)
    menuSelect = []
    menuBtns = []
    bullets = []
    enemyList = []
    planets = []
    e_level = NumericProperty(0)
    allDead = False
    bg_texture = ObjectProperty(None)
    hint_text = StringProperty('')
    up_k = False
    down_k = False
    left_k = False
    right_k = False
    shipSelect = True
    planetGen = 0

    def scroll_texture(self, time_passed):
        self.bg_texture.uvpos = (self.bg_texture.uvpos[0], (self.bg_texture.uvpos[1]) % Window.height - time_passed/10)
        # redraw the image.
        texture = self.property('bg_texture')
        texture.dispatch(self)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._keyboard = Window.request_keyboard(self._on_keyboard_close, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)
        self.bg_texture = Image(source='starfield.png').texture
        self.bg_texture.wrap = 'repeat'
        self.bg_texture.uvsize = (2, 2)
        self.go_string = ''
        self.hint_text = ''
        self.player.pos = ((Window.width / 2) - 50, 200)
        self.player.size = (0, 0)
        self.gun1shoot = SoundLoader.load('laser6.mp3')
        self.shipMenu()

        Clock.schedule_interval(self.player.animate, 0.05)

    def showSelectMenu(self):
        global GamePause
        GamePause = True
        self.shipSelect = True
        self.hint_text = ''
        self.go_string = ''
        self.title_s = 'SELECT YOUR SHIP'
        for eac in self.menuSelect:
            eac.show()
        for eax in self.menuBtns:
            eax.size = (100, 100)

    def hideSelectMenu(self):
        self.title_s = 'Level ' + str(self.e_level)
        for eac in self.menuSelect:
            eac.hide()
        for eax in self.menuBtns:
            eax.size = (0, 0)

    def shipMenu(self):
        global GamePause
        GamePause = True
        self.shipSelect = True
        self.hint_text = ''
        self.go_string = ''
        self.title_s = 'SELECT YOUR SHIP'
        with self.canvas.before:
            self.ship1 = Player()
            self.ship1.src = 'atlas://playerAnim3.atlas/frame0'
            self.ship1.center_x = Window.width / 2 + 100
            self.ship1.center_y = (Window.height / 2)
            self.ship1.size = (300, 300)
            self.ship1.ov_anim = 'atlas://playerAnim3.atlas/'
            self.ship2 = Player()
            rect1 = Rectangle(source="arrowLeft.png")
            rect1.pos = (self.ship1.pos[0] + 100, self.ship1.pos[1] - 100)
            rect1.size = (100, 100)

            self.ship2.src = 'atlas://playerAnim2.atlas/frame0'
            self.ship2.center_x = Window.width / 2 + 650
            self.ship2.center_y = (Window.height / 2)
            self.ship2.ov_anim = 'atlas://playerAnim2.atlas/'
            self.ship2.size = (300, 300)
            rect2 = Rectangle(source="arrowRight.png")
            rect2.pos = (self.ship2.pos[0] + 100, self.ship2.pos[1] - 100)
            rect2.size = (100, 100)
            Clock.schedule_interval(self.ship1.animate, 0.05)
            Clock.schedule_interval(self.ship2.animate, 0.05)
            self.menuSelect.append(self.ship1)
            self.menuSelect.append(self.ship2)
            self.menuBtns.append(rect1)
            self.menuBtns.append(rect2)

    def generatePlanets(self):
        if self.planetGen < 20000:
            self.planetGen += random.randrange(0, 250, 5)
        else:
            self.planetGen = 0
            with self.canvas.before:
                self.p1 = Planet(random.choice([1, 2, 3, 4, 5]))
                Clock.schedule_interval(self.p1.animate, 1.0 / 7.0)
                self.planets.append(self.p1)

    def switch_bg(self):
        self.bg_texture.uvsize = (self.bg_texture.uvsize[0] * -1, self.bg_texture.uvsize[1] * -1)

    def GunShoot(self, type_n):
        if type_n == 0:
            with self.canvas.before:
                self.bull = Bullet()
                self.bull.pos = ((self.player.x + 0.5 * self.player.width), self.player.y + self.player.height)
                self.bull.src = self.bull.srcList[0]
                self.bull.size = (10, 40)
                self.bull.setDirection(2)
                self.bullets.append(self.bull)

        elif type_n == 1:
            with self.canvas.before:
                self.bull1 = Bullet()
                self.bull1.pos=((self.player.x + 0.5 * self.player.width) - 10, self.player.y + self.player.height)
                self.bull1.size = (10, 40)
                self.bull2 = Bullet()
                self.bull2.pos= ((self.player.x + 0.5 * self.player.width) + 10, self.player.y + self.player.height)
                self.bull2.size = (10, 40)
                self.bull2.setDirection(2)
                self.bull1.setDirection(2)
                self.bull1.setType(0)
                self.bull2.setType(0)
                self.bullets.append(self.bull1)
                self.bullets.append(self.bull2)

        elif type_n == 2:
            with self.canvas.before:
                self.bull1 = Bullet()
                self.bull1.pos =((self.player.x + 0.5 * self.player.width) - 5, self.player.y + self.player.height)
                self.bull1.size = (10, 40)
                self.bull2 = Bullet()
                self.bull2.pos = ((self.player.x + 0.5 * self.player.width), self.player.y + self.player.height)
                self.bull2.size = (10, 40)
                self.bull3 = Bullet()
                self.bull3.pos = ((self.player.x + 0.5 * self.player.width) + 5, self.player.y + self.player.height)
                self.bull3.size = (10, 40)
                self.bull1.setDirection(3)
                self.bull2.setDirection(2)
                self.bull3.setDirection(1)
                self.bull1.setType(1)
                self.bull2.setType(1)
                self.bull3.setType(1)
                self.bullets.append(self.bull1)
                self.bullets.append(self.bull2)
                self.bullets.append(self.bull3)

        elif type_n == 3:
            with self.canvas.before:
                indent = -20
                for bType in range(0, 5):
                    self.bull = Bullet()
                    self.bull.pos=((self.player.x + 0.5 * self.player.width) - indent,  self.player.y + self.player.height)
                    self.bull.size=(10, 40)
                    self.bull.setDirection(bType)
                    self.bull.setType(2)
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

    def showEnemies(self):
        for eac in self.enemyList:
            eac.setSize(eac.size_x, eac.size_y)

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
        if text == 'c':
            if not self.shipSelect:
                for eac in self.enemyList:
                    eac.hide()
                self.switch_bg()
                self.showSelectMenu()
                self.player.kill()


        if keycode == (32, 'spacebar') and not self.shipSelect:

            if not GamePause and self.go_string == '':

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
                GamePause = False

            if self.go_string == 'YOU WON!':

                self.levelUp()
                self.player.reset()
                GamePause = False


        if not GamePause and not self.shipSelect:
            if text == 'w' or keycode == (273, 'up'):
                if self.left_k or self.right_k:
                    self.player.velocity = Vector(self.player.velocity_x, steps)

                else:
                    self.player.velocity = Vector(0, steps)
                    self.up_k = True
            if text == 's' or keycode == (274, 'down'):
                if self.left_k or self.right_k:
                    self.player.velocity = Vector(self.player.velocity_x, -steps)
                else:
                    self.player.velocity = Vector(0, -steps)
                    self.down_k = True
            if text == 'a' or keycode == (276, 'left'):
                if self.up_k or self.down_k:
                    self.player.velocity = Vector(-steps, self.player.velocity_x)
                else:
                    self.player.velocity = Vector(-steps, 0)
                    self.left_k = True
            if text == 'd' or keycode == (275, 'right'):
                if self.up_k or self.down_k:
                    self.player.velocity = Vector(steps, self.player.velocity_x)
                else:
                    self.player.velocity = Vector(steps, 0)
                    self.right_k = True
        else:
            if self.shipSelect:
                if text == 'a' or keycode == (276, 'left'):
                    self.switch_bg()
                    self.player.src = 'atlas://playerAnim3.atlas/frame0'
                    self.player.ov_anim = 'atlas://playerAnim3.atlas/'
                    self.player.size = (200, 200)
                    self.shipSelect = False
                    GamePause = False
                    self.hideSelectMenu()

                if text == 'd' or keycode == (275, 'right'):
                    self.switch_bg()
                    self.player.src = 'atlas://playerAnim2.atlas/frame0'
                    self.player.ov_anim = 'atlas://playerAnim2.atlas/'
                    self.player.size = (200, 200)
                    self.shipSelect = False
                    GamePause = False
                    self.hideSelectMenu()
                if not self.shipSelect:
                    self.showEnemies()
                    if self.e_level == 0:
                        self.levelUp()

    def restart(self):

        for eac in self.enemyList:
            Clock.unschedule(eac.animate)
            eac.kill()
            self.remove_widget(eac)
        for eax in self.bullets:
            Clock.unschedule(eax.shoot)
            eax.kill()
            self.remove_widget(eax)
        self.allDead = False
        self.e_level = 1
        self.title_s = 'Level ' + str(self.e_level)
        self.go_string = ''
        self.hint_text = ''
        with self.canvas:
            for i in range(0, self.e_level):
                self.enem = self.generateEnemy()
                Clock.schedule_interval(self.enem.update, 1.0 / 60.0)
                self.enemyList.append(self.enem)

    def levelUp(self):
        for eac in self.enemyList:
            Clock.unschedule(eac.animate)
            eac.kill()
            self.remove_widget(eac)
        # for eax in self.bullets:
        #     Clock.unschedule(eax.shoot)
        #     # eax.kill()
        #     # self.remove_widget(eax)
        self.e_level += 1
        self.hint_text = ''
        self.go_string = ''
        self.title_s = 'Level ' + str(self.e_level)
        self.allDead = False
        self.enemyList.clear()
        # self.bullets.clear()
        with self.canvas:
            for i in range(0, self.e_level):
                self.enem = self.generateEnemy()
                self.enem.dead = False
                Clock.schedule_interval(self.enem.update, 1.0 / 60.0)
                self.enemyList.append(self.enem)

    def checkPlayerBoundaries(self):
        if self.player.y <= 2 or (self.player.y + self.player.height) - 2 >= self.height:
            if self.player.pos[1] > Window.height / 2:
                self.player.pos = (self.player.pos[0], Window.height - 205)
            else:
                self.player.pos = (self.player.pos[0], 5)
            self.player.velocity_y *= -1
            self.player.velocity_y /= 10
            return True
        if self.player.x <= 2 or (self.player.x + self.player.width) - 2 >= self.width:
            if self.player.pos[0] > Window.width / 2:
                self.player.pos = (Window.width - 205, self.player.pos[1])
            else:
                self.player.pos = (5, self.player.pos[1])

            self.player.velocity_x *= -1
            self.player.velocity_x /= 10
            return True
        return False

    def update(self, dt):

        self.generatePlanets()
        for planet in self.planets:
            if planet.isDead():
                planet.size = (0, 0)
                Clock.unschedule(planet.move)
                self.remove_widget(planet)
                self.planets.remove(planet)
            else:
                planet.move()
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

        counter = 0
        for e in self.enemyList:
            if e.isDead():
                counter += 1
        if counter == len(self.enemyList):
            self.allDead = True

        global GamePause
        if self.allDead and not self.shipSelect:
            GamePause = True
            self.go_string = 'YOU WON!'
            self.hint_text = 'PRESS SPACE FOR NEXT LEVEL'

        for eac in self.enemyList:
            if self.player.collides(eac):
                if not eac.isDead():
                    GamePause = True
                    self.go_string = 'GAME OVER'
                    self.hint_text = 'PRESS SPACE TO RESTART'


class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        game = GameWidget()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        Clock.schedule_interval(game.scroll_texture, 1.0 / 60.0)
        return game

    pass


if __name__ == '__main__':
    app = MyApp()
    app.run()
