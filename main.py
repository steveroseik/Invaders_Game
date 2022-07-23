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
    gap_delimeter = 0
    size_x = 0
    size_y = 0
    timer = 300
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
        self.opacity = 0.3
        self.reset(e)
        self.frame_count = self.f_index
        for i in range(self.f_index, self.f_index + self.f_end):
            self.frames.append('frame' + str(i))
        self.ready = True

    def reset(self, e):
        randY = random.choice([1.5, 1.7, 1.9, 2.1, 2.2])
        self.velocity = (0, -randY)
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
        self.pos = (random.randrange(200, Window.width - 150), Window.height)

    def setSize(self, w, h):
        self.size_x = w
        self.size_y = h
        self.size = (w, h)

    def animate(self, dt):
        self.gap_delimeter += dt
        if self.gap_delimeter > 0.1:
            self.gap_delimeter = 0
            self.frame_count += 1
            if self.frame_count >= (self.f_index + self.f_end) - 1:
                self.frame_count = self.f_index

            key = self.frames[self.frame_count]
            self.src = self.ov_anim[self.eType] + key

    def move(self):
        if self.pos[1] <= -200:
            self.reset(random.randrange(0, 6))
        self.pos = Vector(self.velocity) + self.pos

    def isDead(self):
        return self.dead

## ENEMY CLASS
#
#
class Invader(Widget):
    image_path = StringProperty()

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
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
    time_limit = 0
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def reset(self, e, r, x, y):
        self.ready = False
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

        self.frames.clear()
        self.frame_count = self.f_index
        for i in range(self.f_index, self.f_index + self.f_end):
            self.frames.append('frame' + str(i))
        self.resistance = r
        self.setPos(x, y)
        self.ready = True

    def setPos(self, x, y):
        self.pos = (x, y)

    def setSize(self, w, h):
        self.size_x = w
        self.size_y = h
        self.size = (w, h)

    def hide(self):
        self.opacity = 0

    def show(self):
        self.opacity = 1

    def animate(self, dt):
        if self.time_limit > 0:
            self.time_limit -= dt * 20
        else:
            self.time_limit = 3

            if self.ready:
                self.frame_count += 1
                if self.frame_count >= (self.f_index + self.f_end) - 1:
                    self.frame_count = self.f_index - 1
                key = self.frames[self.frame_count]
                self.src = self.ov_anim[self.eType] + key


    def setResistance(self, r):
        self.resistance = r

    def move(self, dt):
        if not GamePause:
            if self.timer < 0:
                self.timer = 40
                self.velocity_x = random.choice([7, -7, 0])
                if self.velocity_x != 0:
                    self.velocity_y = random.choice([7, -7, 0])
                else:
                    self.velocity_y = random.choice([7, -7])
            else:
                self.timer -= dt * 10

            self.pos = Vector(self.velocity) + self.pos
            self.collision()

    def collision(self):
        if not self.dead:
            if self.pos[1] < 0 or (self.pos[1] + self.size[1]) > Window.height:
                if self.pos[1] > Window.height / 2:
                    self.pos = (self.pos[0], Window.height - self.size[1] - 5)
                else:
                    self.pos = (self.pos[0], 5)
                self.velocity_y *= -1
            if self.pos[0] < 0 or (self.pos[0] + self.size[0]) > Window.width:
                if self.pos[0] > Window.width / 2:
                    self.pos = (Window.width - self.size[0] - 5, self.pos[1])
                else:
                    self.pos = (5, self.pos[1])
                self.velocity_x *= -1

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
        self.hide()
        me = self.animate

    def revive(self):
        self.show()
        self.dead = False
        self.setSize(self.size_x, self.size_y)




## Player CLASS
#
#
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

    # enemy collision
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
            self.updatePlayerBoundaries()
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

    # lock player inbound with window

    def updatePlayerBoundaries(self):
        if self.y <= 2 or (Window.height - 2) <= self.y + self.height:
            if self.pos[1] > Window.height / 2:
                self.pos = (self.pos[0], Window.height - 205)
            else:
                self.pos = (self.pos[0], 5)
            self.velocity_y *= -1
            self.velocity_y /= 10

        if self.x <= 2 or (Window.width - 2) <= self.x + self.width:
            if self.pos[0] > Window.width / 2:
                self.pos = (Window.width - 205, self.pos[1])
            else:
                self.pos = (5, self.pos[1])

            self.velocity_x *= -1
            self.velocity_x /= 10

## BULLET CLASS
#
#
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

    def outOfBounds(self):
        if self.x < 0 or self.x > Window.width or self.y > Window.height:
            return True
        return False

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
    planetIndex = 0

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
        self.bg_texture.uvsize = (2, -2)
        self.go_string = ''
        self.hint_text = ''
        self.player.size = (0, 0)
        self.player.reset()
        self.gun1shoot = SoundLoader.load('laser6.mp3')
        self.shipMenu()

        Clock.schedule_interval(self.updateGlobal, 1.0 / 60.0)
        Clock.schedule_interval(self.enemyMovement, 1.0 / 60.0)
        Clock.schedule_interval(self.scroll_texture, 1.0 / 60.0)
        # generate stack of planets
        for i in range(0, 10):
            plan = Planet(random.choice([1, 2, 3, 4, 5]))
            plan.y = Window.height + i*500
            self.planets.append(plan)
            self.add_widget(plan)


        # set player spritesheet animation
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

        self.ship1 = Player()
        self.ship1.src = 'atlas://playerAnim3.atlas/frame0'
        self.ship1.center_x = Window.width / 2 + 100
        self.ship1.center_y = (Window.height / 2)
        self.ship1.size = (300, 300)
        self.ship1.ov_anim = 'atlas://playerAnim3.atlas/'
        self.ship2 = Player()


        self.ship2.src = 'atlas://playerAnim2.atlas/frame0'
        self.ship2.center_x = Window.width / 2 + 650
        self.ship2.center_y = (Window.height / 2)
        self.ship2.ov_anim = 'atlas://playerAnim2.atlas/'
        self.ship2.size = (300, 300)
        Clock.schedule_interval(self.ship1.animate, 0.05)
        Clock.schedule_interval(self.ship2.animate, 0.05)
        self.menuSelect.append(self.ship1)
        self.menuSelect.append(self.ship2)
        self.add_widget(self.ship1)
        self.add_widget(self.ship2)
        with self.canvas:
            rect1 = Rectangle(source="arrowLeft.png")
            rect1.pos = (self.ship1.pos[0] + 100, self.ship1.pos[1] - 100)
            rect1.size = (100, 100)
            rect2 = Rectangle(source="arrowRight.png")
            rect2.pos = (self.ship2.pos[0] + 100, self.ship2.pos[1] - 100)
            rect2.size = (100, 100)
            self.menuBtns.append(rect1)
            self.menuBtns.append(rect2)

    def generatePlanets(self, dt):
        for planet in self.planets:
            if not planet.isDead():
                planet.move()
                planet.animate(dt)


    def GunShoot(self, type_n):
        if type_n == 0:
            self.bull = Bullet()
            self.bull.pos = ((self.player.x + 0.5 * self.player.width), self.player.y + self.player.height)
            self.bull.src = self.bull.srcList[0]
            self.bull.size = (10, 40)
            self.bull.setDirection(2)
            self.bullets.append(self.bull)
            self.add_widget(self.bull)

        elif type_n == 1:
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
            self.add_widget(self.bull1)
            self.add_widget(self.bull2)

        elif type_n == 2:
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
            self.add_widget(self.bull1)
            self.add_widget(self.bull2)
            self.add_widget(self.bull3)


        elif type_n == 3:
            indent = -20
            for bType in range(0, 5):
                self.bull = Bullet()
                self.bull.pos = ((self.player.x + 0.5 * self.player.width) - indent,  self.player.y + self.player.height)
                self.bull.size = (10, 40)
                self.bull.setDirection(bType)
                self.bull.setType(2)
                indent += 10
                self.bullets.append(self.bull)
                self.add_widget(self.bull)

    def generateEnemies(self):
        for enemy in self.enemyList:

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
                var = random.choice([1, 2, 3, 4, 5, 6, 7])
            else:
                var = self.e_level

            enemy.reset(var, res, randW, randH)
            enemy.revive()




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
                GamePause = False

            if self.go_string == 'YOU WON!':

                self.levelUp()
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
                    self.player.src = 'atlas://playerAnim3.atlas/frame0'
                    self.player.ov_anim = 'atlas://playerAnim3.atlas/'
                    self.player.size = (200, 200)
                    self.shipSelect = False
                    GamePause = False
                    self.hideSelectMenu()

                if text == 'd' or keycode == (275, 'right'):
                    self.player.src = 'atlas://playerAnim2.atlas/frame0'
                    self.player.ov_anim = 'atlas://playerAnim2.atlas/'
                    self.player.size = (200, 200)
                    self.shipSelect = False
                    GamePause = False
                    self.hideSelectMenu()
                if not self.shipSelect:
                    for enemy in self.enemyList:
                        if not enemy.isDead():
                            enemy.show()
                    if self.e_level == 0:
                        self.levelUp()

    def restart(self):
        for enemy in self.enemyList:
            self.remove_widget(enemy)
        self.enemyList.clear()
        self.e_level = 0
        self.levelUp()

    def levelUp(self):

        self.player.reset()
        self.e_level += 1
        self.hint_text = ''
        self.go_string = ''
        self.title_s = 'Level ' + str(self.e_level)
        self.allDead = False
        self.enemyList.append(Invader())
        self.add_widget(self.enemyList[-1])
        self.generateEnemies()

    # move each enemy if alive
    def enemyMovement(self, dt):
        # manage enemy status
        for enemy in self.enemyList:
            if not enemy.isDead() and not GamePause:
                enemy.move(dt)

    def clear_oldBullets(self):
        for bullet in self.bullets:
            if bullet.isDead() or bullet.outOfBounds():
                self.remove_widget(bullet)
                self.bullets.remove(bullet)

    def updateGlobal(self, dt):
        global GamePause
        self.generatePlanets(dt)
        self.player.move()
        self.clear_oldBullets()

        for enemy in self.enemyList:
            enemy.animate(dt)

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
        return game

    pass


if __name__ == '__main__':
    app = MyApp()
    app.run()
