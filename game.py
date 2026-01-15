import gi 
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

import sdl2
import sdl2.sdlmixer as mix

from character import Character

class Game:
    def __init__(self):
        self.characters = init_characters()
        self.character = None

def init_game(box):
    game = Game()
    game.character = game.characters[0]

    sdl2.SDL_Init(sdl2.SDL_INIT_AUDIO)
    mix.Mix_OpenAudio(44100, mix.MIX_DEFAULT_FORMAT, 2, 2048)

    character_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
    box.append(character_box)
    
    left_arrow = Gtk.Picture()
    left_arrow.set_filename("assets/left_arrow.png")
    gesture_left = Gtk.GestureClick()
    left_arrow.add_controller(gesture_left)
    gesture_left.connect("pressed", clicked_left_arrow, game)
    left_arrow.set_margin_top(60)
    left_arrow.set_margin_bottom(60)
    character_box.append(left_arrow)

    image = Gtk.Picture()
    image.set_filename(game.character.cartoon)
    character_box.append(image)
    
    rigth_arrow = Gtk.Picture()
    rigth_arrow.set_filename("assets/rigth_arrow.png")
    gesture_rigth = Gtk.GestureClick()
    rigth_arrow.add_controller(gesture_rigth)
    gesture_rigth.connect("pressed", clicked_rigth_arrow, game)
    rigth_arrow.set_margin_top(60)
    rigth_arrow.set_margin_bottom(60)
    character_box.append(rigth_arrow)

    vt_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
    character_box.append(vt_box)

    stats_box = create_display_stats(game)
    vt_box.append(stats_box)

    gesture_left.image = image
    gesture_left.stats = stats_box
    gesture_rigth.image = image
    gesture_rigth.stats = stats_box

    button = Gtk.Button(label="PLAY")
    button.get_style_context().add_class("btn-play")
    vt_box.append(button)


def init_characters():
    return [
            Character("José Sócrates", 0, 0.75, 0.60, 0.70, 0.50, "assets/jose_socrates.png", "assets/socrates.mp3"),
            Character("Luís Montenegro", 1, 0.55, 0.40, 0.70, 0.60, "assets/luis_montenegro.png", "assets/montenegro.mp3"),
            Character("André Ventura", 2, 0.70, 0.90, 0.50, 0.50, "assets/andre_ventura.png", "assets/ventura.mp3")
            ]


def create_display_stats(game):
    stats_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

    label = Gtk.Label(label=game.character.name)
    label.get_style_context().add_class("title")
    stats_box.append(label)

    stats = game.character.get_stats()   

    for i in stats:
        label = Gtk.Label(label=i)
        label.get_style_context().add_class("stats-label")
        stats_box.append(label)

        bar = Gtk.ProgressBar()
        bar.set_fraction(stats[i])
        bar.get_style_context().add_class("progressbar")
        stats_box.append(bar)

    return stats_box

def update_display_stats(game, box):

    while child := box.get_first_child():
        box.remove(child)

    label = Gtk.Label(label=game.character.name)    
    label.get_style_context().add_class("title")
    box.append(label)

    stats = game.character.get_stats()   

    for i in stats:
        label = Gtk.Label(label=i)       
        label.get_style_context().add_class("stats-label")
        box.append(label)

        bar = Gtk.ProgressBar()
        bar.set_fraction(stats[i])
        bar.get_style_context().add_class("progressbar")
        box.append(bar)

    sound = mix.Mix_LoadWAV(bytes(game.character.sound, "utf-8"))
    mix.Mix_PlayChannel(-1, sound, 0)

def clicked_left_arrow(gesture, n_press, x, y, game):
    index = (game.character.index - 1) % len(game.characters)
    
    game.character = game.characters[index]

    gesture.image.set_filename(game.character.cartoon)
    update_display_stats(game, gesture.stats) 

def clicked_rigth_arrow(gesture, n_press, x, y, game):
    index = (game.character.index + 1) % len(game.characters)
    
    game.character = game.characters[index]
    
    gesture.image.set_filename(game.character.cartoon)
    update_display_stats(game, gesture.stats) 

