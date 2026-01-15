import gi 
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

import sdl2
import sdl2.sdlmixer as mix

import random

from character import Character
from options import Option

class Game:
    def __init__(self):
        self.characters = init_characters()
        self.character = None
        self.options = [
                Option("rock", "assets/rock.png"), 
                Option("scissor", "assets/scissor.png"),
                Option("paper", "assets/paper.png")
                ]
        self.rounds = 1
        self.wins = 0 
        self.loses = 0 

def init_menu(stack):
    game = Game()
    game.character = game.characters[0]

    sdl2.SDL_Init(sdl2.SDL_INIT_AUDIO)
    mix.Mix_OpenAudio(44100, mix.MIX_DEFAULT_FORMAT, 2, 2048)

    character_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
    stack.add_named(character_box, "menu")

    left_arrow = Gtk.Picture()
    left_arrow.set_filename("assets/left_arrow.png")
    left_arrow.get_style_context().add_class("arrow")
    gesture_left = Gtk.GestureClick()
    left_arrow.add_controller(gesture_left)
    gesture_left.connect("pressed", clicked_left_arrow, game)
    left_arrow.set_size_request(width=50, height=50)
    left_arrow.set_margin_top(200)
    left_arrow.set_margin_end(30)
    left_arrow.set_margin_start(30)
    left_arrow.set_margin_bottom(200)
    character_box.append(left_arrow)

    image = Gtk.Picture()
    image.set_filename(game.character.cartoon)
    character_box.append(image)
    
    rigth_arrow = Gtk.Picture()
    rigth_arrow.set_filename("assets/rigth_arrow.png")    
    rigth_arrow.get_style_context().add_class("arrow")
    gesture_rigth = Gtk.GestureClick()
    rigth_arrow.add_controller(gesture_rigth)
    gesture_rigth.connect("pressed", clicked_rigth_arrow, game)
    rigth_arrow.set_size_request(width=50, height=50)
    rigth_arrow.set_margin_top(200)
    rigth_arrow.set_margin_end(30)
    rigth_arrow.set_margin_start(30)
    rigth_arrow.set_margin_bottom(200)
    character_box.append(rigth_arrow)
    
    vt_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=50)
    vt_box.set_valign(Gtk.Align.CENTER)
    character_box.append(vt_box)
    
    stats_box = create_display_stats(game)
    stats_box.set_valign(Gtk.Align.CENTER)
    vt_box.append(stats_box)

    gesture_left.image = image
    gesture_left.stats = stats_box
    gesture_rigth.image = image
    gesture_rigth.stats = stats_box

    button = Gtk.Button(label="PLAY")
    button.get_style_context().add_class("btn-play")
    button.connect("clicked", clicked_play, game)
    button.stack = stack
    vt_box.append(button)

def init_game(stack, game):
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
    stack.add_named(box, "game")

    label_round = Gtk.Label(label="ROUND 1")
    label_round.get_style_context().add_class("label-round")
    label_round.set_halign(Gtk.Align.CENTER)
    box.append(label_round)
    
    ht_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
    ht_box.set_margin_start(50)
    ht_box.set_margin_end(50)
    box.append(ht_box)

    vt_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    ht_box.append(vt_box)
    
    label = Gtk.Label(label="Your Score")
    label.get_style_context().add_class("label-score")
    label.set_halign(Gtk.Align.CENTER)
    vt_box.append(label)

    image_1 = Gtk.Picture()
    update_stars(game.wins, image_1)
    image_1.set_size_request(width=120, height=40)
    image_1.set_halign(Gtk.Align.CENTER)
    vt_box.append(image_1)
    
    spacer = Gtk.Box()
    spacer.set_hexpand(True)
    ht_box.append(spacer)

    vt_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    ht_box.append(vt_box)
    
    label = Gtk.Label(label=game.character.name)
    label.get_style_context().add_class("label-score")
    label.set_halign(Gtk.Align.CENTER)
    vt_box.append(label)

    image_2 = Gtk.Picture()        
    update_stars(game.loses, image_2)
    image_2.set_size_request(width=120, height=40)
    image_2.set_margin_start(30)
    image_2.set_margin_end(30)
    image_2.set_halign(Gtk.Align.CENTER)
    vt_box.append(image_2)

    game_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=150)
    game_box.set_size_request(width=-1, height=300)
    game_box.set_margin_start(50)
    game_box.set_margin_end(50)
    box.append(game_box)
    
    plays_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    plays_box.set_margin_start(50)
    plays_box.set_margin_end(50)
    box.append(plays_box)

    rock = Gtk.Picture()
    rock.set_filename("assets/rock.png")
    rock.get_style_context().add_class("rock")
    gesture = Gtk.GestureClick()
    gesture.player = image_1
    gesture.enime = image_2
    gesture.rounds = label_round
    gesture.box = game_box
    gesture.stack = stack
    rock.add_controller(gesture)
    gesture.connect("pressed", clicked_rock, game)
    rock.set_size_request(width=50, height=50)
    plays_box.append(rock)

    paper = Gtk.Picture()
    paper.set_filename("assets/paper.png")
    paper.get_style_context().add_class("paper")
    gesture = Gtk.GestureClick()  
    gesture.player = image_1
    gesture.enime = image_2
    gesture.rounds = label_round
    gesture.box = game_box
    gesture.stack = stack
    paper.add_controller(gesture)
    gesture.connect("pressed", clicked_paper, game)
    paper.set_size_request(width=50, height=50)
    plays_box.append(paper)    

    scissor = Gtk.Picture()
    scissor.set_filename("assets/scissor.png")
    scissor.get_style_context().add_class("scissor")
    gesture = Gtk.GestureClick()
    gesture.player = image_1
    gesture.enime = image_2
    gesture.rounds = label_round
    gesture.box = game_box
    gesture.stack = stack
    scissor.add_controller(gesture)
    gesture.connect("pressed", clicked_scissor, game)
    scissor.set_size_request(width=50, height=50)
    plays_box.append(scissor)



def init_characters():
    return [
            Character("José Sócrates", 0, 0.75, 0.60, 0.70, 0.50, "assets/jose_socrates.png", "assets/socrates.mp3"),
            Character("Luís Montenegro", 1, 0.55, 0.40, 0.70, 0.60, "assets/luis_montenegro.png", "assets/montenegro.mp3"),
            Character("André Ventura", 2, 0.70, 0.90, 0.50, 0.50, "assets/andre_ventura.png", "assets/ventura.mp3")
            ]


def create_display_stats(game):
    
    main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    
    grid = Gtk.Grid()
    grid.set_row_spacing(10)
    main_box.append(grid)
    
    label_box = Gtk.Box()
    grid.attach(label_box, 0, 0, 2, 1)

    label = Gtk.Label(label=game.character.name)
    label.get_style_context().add_class("title")
    label_box.append(label)

    
    stats_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
    grid.attach(stats_box, 0, 1, 1, 1)

    stats = game.character.get_stats()   

    for i in stats:
        label = Gtk.Label(label=i)
        label.get_style_context().add_class("stats-label")
        label.set_hexpand(False)
        stats_box.append(label)

        bar = Gtk.ProgressBar()
        bar.set_fraction(stats[i])
        bar.get_style_context().add_class("progressbar")
        bar.set_hexpand(False)
        stats_box.append(bar)

    return main_box

def update_display_stats(game, box):

    while child := box.get_first_child():
        box.remove(child)
    
    grid = Gtk.Grid()
    grid.set_row_spacing(10)
    box.append(grid)
    
    label_box = Gtk.Box()
    grid.attach(label_box, 0, 0, 2, 1)

    label = Gtk.Label(label=game.character.name)
    label.get_style_context().add_class("title")
    label_box.append(label)
    
    stats_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
    grid.attach(stats_box, 0, 1, 1, 1)
    
    stats = game.character.get_stats()   

    for i in stats:
        label = Gtk.Label(label=i)       
        label.get_style_context().add_class("stats-label")
        label.set_hexpand(False)
        stats_box.append(label)
        
        bar = Gtk.ProgressBar()
        bar.set_fraction(stats[i])
        bar.get_style_context().add_class("progressbar")
        bar.set_hexpand(False)
        stats_box.append(bar)


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

def clicked_play(button, data):
    init_game(button.stack, data)

    sound = mix.Mix_LoadWAV(bytes(data.character.sound, "utf-8"))
    mix.Mix_PlayChannel(-1, sound, 0)
    
    button.stack.set_visible_child_name("game")


def clicked_rock(gesture, n_press, x, y, game):

    while child := gesture.box.get_first_child():
        gesture.box.remove(child)
    
    image = Gtk.Picture()
    image.set_filename("assets/rock.png")
    image.set_size_request(width=50, height=50)
    gesture.box.append(image)

    option = random.choice(game.options)
    
    image = Gtk.Picture()
    image.set_filename(option.image)
    image.set_size_request(width=50, height=50)
    gesture.box.append(image)

    if option.option == "scissor":
        game.wins += 1    
        game.rounds += 1
        update_stars(game.wins, gesture.player)
        update_round(game.rounds, gesture.rounds)
    elif option.option == "paper":
        game.loses += 1 
        game.rounds += 1
        update_stars(game.loses, gesture.enime)
        update_round(game.rounds, gesture.rounds)
    else:
        game.rounds += 1 
        update_round(game.rounds, gesture.rounds)

    if game.wins == 3 or game.loses == 3:
        GLib.timeout_add(3000, delay)
        
        game.wins = 0 
        game.loses = 0 
        game.rounds = 1

        gesture.stack.set_visible_child_name("menu")
        GLib.timeout_add(1000, delay)
        gesture.stack.remove(gesture.stack.get_child_by_name("game"))


def clicked_scissor(gesture, n_press, x, y, game):
    
    while child := gesture.box.get_first_child():
        gesture.box.remove(child)
    
    image = Gtk.Picture()
    image.set_filename("assets/scissor.png")
    image.set_size_request(width=50, height=50)
    gesture.box.append(image)

    option = random.choice(game.options)
    
    image = Gtk.Picture()
    image.set_filename(option.image)
    image.set_size_request(width=50, height=50)
    gesture.box.append(image)

    if option.option == "paper":
        game.wins += 1    
        game.rounds += 1
        update_stars(game.wins, gesture.player)
        update_round(game.rounds, gesture.rounds)
    elif option.option == "rock":
        game.loses += 1 
        game.rounds += 1
        update_stars(game.loses, gesture.enime)
        update_round(game.rounds, gesture.rounds)
    else:
        game.rounds += 1 
        update_round(game.rounds, gesture.rounds)
    
    if game.wins == 3 or game.loses == 3:
        GLib.timeout_add(3000, delay)
        
        game.wins = 0 
        game.loses = 0 
        game.rounds = 1

        gesture.stack.set_visible_child_name("menu")       
        GLib.timeout_add(1000, delay)
        gesture.stack.remove(gesture.stack.get_child_by_name("game"))


def clicked_paper(gesture, n_press, x, y, game):
    
    while child := gesture.box.get_first_child():
        gesture.box.remove(child)
    
    image = Gtk.Picture()
    image.set_filename("assets/paper.png")
    image.set_size_request(width=50, height=50)
    gesture.box.append(image)

    option = random.choice(game.options)
    
    image = Gtk.Picture()
    image.set_filename(option.image)
    image.set_size_request(width=50, height=50)
    gesture.box.append(image)

    if option.option == "rock":
        game.wins += 1 
        game.rounds += 1
        update_stars(game.wins, gesture.player)
        update_round(game.rounds, gesture.rounds)
    elif option.option == "scissor":
        game.loses += 1
        game.rounds += 1
        update_stars(game.loses, gesture.enime)   
        update_round(game.rounds, gesture.rounds)
    else:
        game.rounds += 1 
        update_round(game.rounds, gesture.rounds)

    if game.wins == 3 or game.loses == 3:
        GLib.timeout_add(3000, delay)

        game.wins = 0 
        game.loses = 0 
        game.rounds = 1 

        gesture.stack.set_visible_child_name("menu")
        GLib.timeout_add(1000, delay)
        gesture.stack.remove(gesture.stack.get_child_by_name("game"))


def update_stars(score, image):

    if score == 0:
        image.set_filename("assets/stars_0.png")
    elif score == 1:
        image.set_filename("assets/stars_1.png")
    elif score == 2:
        image.set_filename("assets/stars_2.png")
    elif score == 3:
        image.set_filename("assets/stars_3.png")    
        
        
def update_round(rounds, label):
    text = f"ROUND {rounds}"
    label.set_text(text)

def delay():
    return False
