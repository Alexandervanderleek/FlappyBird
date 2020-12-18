from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from random import randint
from kivy.properties import NumericProperty

from pipe import Pipe

class Backround(Widget):
    cloud_texture = ObjectProperty(None)
    floor_texture = ObjectProperty(None)

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        #create textures
        self.cloud_texture = Image(source="cloud.png").texture
        self.cloud_texture.wrap = 'repeat'
        self.cloud_texture.uvsize = (Window.width / self.cloud_texture.width, -1)


        self.floor_texture = Image(source="floor.png").texture
        self.floor_texture.wrap = 'repeat'
        self.floor_texture.uvsize = (Window.width / self.floor_texture.width, -1)

    def scroll_texture(self, time_passed):
        #update uv pos texture
        self.cloud_texture.uvpos = ((self.cloud_texture.uvpos[0] + time_passed/2)%Window.width,self.cloud_texture.uvpos[1])
        self.floor_texture.uvpos = ((self.cloud_texture.uvpos[0] + time_passed)%Window.width,self.floor_texture.uvpos[1])

        #redraw the texture
        texture = self.property('cloud_texture')
        texture.dispatch(self)

        texture = self.property('floor_texture')
        texture.dispatch(self)

class Bird(Image):
    velocity = NumericProperty(0)

    def on_touch_down(self, touch):
        self.source = "bird2.png"
        self.velocity = 150
        super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.source = "bird1.png"
        super().on_touch_up(touch)

class MainApp(App):
    pipes = []
    GRAVITY = 300
    was_colliding = False



    def check_collisions(self):
        is_colliding = False
        bird = self.root.ids.bird
        for pipe in self.pipes:
            if pipe.collide_widget(bird): # check if widgets collide
                is_colliding = True
                if bird.y < (pipe.pipe_center - pipe.Gap_size/2):
                    self.game_over()
                if bird.top > (pipe.pipe_center + pipe.Gap_size/2):
                    self.game_over()
        if bird.y < 96:
            self.game_over()
        if bird.top > Window.height:
            self.game_over()
        if self.was_colliding and not is_colliding:
            self.root.ids.score.text = str(int(self.root.ids.score.text) + 1)
        self.was_colliding = is_colliding

    def next_frame(self, time_passed):
        self.move_bird(time_passed)
        self.move_pipes(time_passed)
        self.root.ids.backround.scroll_texture(time_passed)



    def game_over(self):
        self.root.ids.bird.pos = (20, (self.root.height -96)/2)
        for pipe in self.pipes:
            self.root.remove_widget(pipe)
        self.frames.cancel()
        self.root.ids.button.disabled = False
        self.root.ids.button.opacity = 1

    def move_bird(self,time_passed):
        bird = self.root.ids.bird
        bird.y = bird.y + bird.velocity * time_passed
        bird.velocity = bird.velocity - self.GRAVITY * time_passed
        self.check_collisions()


    def start_game(self):
        self.root.ids.score.text = "0"
        self.was_colliding = False
        self.pipes = []
        #Clock.schedule_interval(self.move_bird, 1/60)
        self.frames = Clock.schedule_interval(self.next_frame, 1/60)

        #create pipe
        num_pipes = 5
        distance_between_pipes = Window.width / (num_pipes - 1)
        for i in range(num_pipes):
            pipe = Pipe() #from our pipe class
            pipe.pipe_center = randint(96 + 100, self.root.height - 100)
            pipe.size_hint = (None,None)
            pipe.pos = (Window.width +i*distance_between_pipes, 96) #y is the second
            pipe.size = (64, self.root.height-96)

            self.pipes.append(pipe)
            self.root.add_widget(pipe)

        #Clock.schedule_interval(self.move_pipes, 1/60)

    def move_pipes(self, time_passed):
        for pipe in self.pipes:
            pipe.x -= time_passed * 100

        #repositioning
        num_pipes = 5
        distance_between_pipes = Window.width / (num_pipes - 1)

        pipe_xs = list(map(lambda pipe: pipe.x,self.pipes)) #get all pipe.xs from the list of pipes
        right_most_x = max(pipe_xs)

        if right_most_x <= Window.width - distance_between_pipes:
            most_left_pipe = self.pipes[pipe_xs.index(min(pipe_xs))]
            most_left_pipe.x = Window.width




MainApp().run()
