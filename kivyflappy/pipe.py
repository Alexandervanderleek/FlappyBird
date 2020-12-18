from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.uix.image import Image
from kivy.clock import Clock




class Pipe(Widget):
    """docstring for ."""
    Gap_size = NumericProperty(120)
    cap_size = NumericProperty(20)
    pipe_center = NumericProperty(0)
    bottom_body_pos = NumericProperty(0)
    bottom_cap_pos = NumericProperty(0)
    top_body_pos = NumericProperty(0)
    top_cap_pos = NumericProperty(0)

    # Texture
    pipe_body_texture = ObjectProperty(None)
    lower_pipe_texcord = ListProperty((0,0,1,0,1,1,0,1))
    top_pipe_texcord = ListProperty((0,0,1,0,1,1,0,1))


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pipe_body_texture = Image(source="pipe_body.png").texture
        self.pipe_body_texture.wrap = 'repeat'

    def on_size(self, *args):
        lower_body_size = self.bottom_cap_pos - self.bottom_body_pos

        self.lower_pipe_texcord[5] = lower_body_size/20.
        self.lower_pipe_texcord[7] = lower_body_size/20.

        top_body_size = self.top - self.top_body_pos
        self.top_pipe_texcord[5] = lower_body_size/20.
        self.top_pipe_texcord[7] = lower_body_size/20.


    def on_pipe_center(self, *args):
        Clock.schedule_once(self.on_size, 0)
