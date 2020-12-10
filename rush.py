# Rush - Collect as many coins as fast as possible!
# Optimal screen resolution: 1280x720

# Pause key: esc
# Boss key: B
# Disable boss key: X
# Cheat key (increases level score): U
# Default character movement keys: WASD

# Imports required libraries
from tkinter import Tk, PhotoImage, Canvas, Label, Button, ttk, \
                    messagebox
import random
import os

window = Tk()


# Defines the default properties of the window
def configure_window():
    window.title("Rush")
    window.geometry("1280x720")
    window.configure(background="#0E2F44")


# Resets and initiates game
def start_game():
    global t, g_score, s_score, b_score, paused, cur_lvl, in_game
    paused = False
    in_game = True
    if not paused:
        tally["text"] = "Lvl 1 score:" + str(0)
        tally2["text"] = "Lvl 2 score: " + str(0)
        tally3["text"] = "Lvl 3 score: " + str(0)
        g_score = 0
        s_score = 0
        b_score = 0
        t = 60
        cur_lvl = 1
        pause_canvas.forget()
        save_menu_canvas.forget()
        menu_canvas.pack_forget()
        game_over_canvas.forget()
        lvl_two_canvas.forget()
        lvl_three_canvas.forget()
        victory_canvas.forget()
        lvl_one_canvas.pack()
        lvl_one_canvas.coords(goblin, 330, 330)
        countdown()


# Updates and packs the leaderboard canvas
def view_ldb():
    global totalscore
    save_menu_canvas.forget()
    victory_canvas.forget()
    menu_canvas.pack_forget()
    ldb_canvas.pack(pady=15, padx=15)
    totalscore = g_score + s_score + b_score


# Reads player statistics and sorts rankings when triggered
def view_scores():
    ldb_tree.delete(*ldb_tree.get_children())
    if os.path.isfile("ldb.txt"):
        with open("ldb.txt", "r") as file:
            player_list = []
            for line in file:
                inner_player_list = [elt.strip() for elt in line.split(',')]
                inner_player_list.sort(reverse=True)
                player_list.append(inner_player_list)
    player_list.sort(key=lambda e: int(e[1]), reverse=True)

    for i, (name, score) in enumerate(player_list, start=1):
        levelled_score = score.zfill(2)
        ldb_tree.insert("", "end", values=(i, name, levelled_score))


# Allows user to confirm whether they want to exit the game
def quit_game():
    quit_prompt = messagebox.askquestion("Quit",
                                         "Are you sure you want to quit?")
    if quit_prompt == "yes":
        window.destroy()


# Closes all other canvasses and takes the user back to the menu
def back_to_menu():
    global paused, in_game
    paused = False
    in_game = False
    howtoplay_canvas.forget()
    lvl_one_canvas.forget()
    lvl_two_canvas.forget()
    lvl_three_canvas.forget()
    ldb_canvas.forget()
    pause_canvas.forget()
    game_over_canvas.forget()
    settings_canvas.forget()
    victory_canvas.forget()
    menu_canvas.pack()


# Updates the leaderboard when game is saved and takes the user back
# to the menu
def back_to_save_menu():
    global paused, in_game, totalscore
    paused = False
    in_game = False
    totalscore = g_score + s_score + b_score
    with open("ldb.txt", "a+") as f:
        f.write(os.getlogin() + "," + str(totalscore) + "\n")
    howtoplay_canvas.forget()
    lvl_one_canvas.forget()
    lvl_two_canvas.forget()
    lvl_three_canvas.forget()
    ldb_canvas.forget()
    pause_canvas.forget()
    game_over_canvas.forget()
    menu_canvas.forget()
    settings_canvas.forget()
    victory_canvas.forget()
    save_menu_canvas.pack(pady=15, padx=15)


# Saves the user's current statistics, updates the leaderboard and takes the
# user back to the menu when they lose
def game_loss_menu():
    global paused, g_score, b_score, s_score, t, cur_lvl, in_game, totalscore
    paused = False
    in_game = False
    totalscore = g_score + s_score + b_score
    with open("ldb.txt", "a+") as f:
        f.write(os.getlogin() + "," + str(totalscore) + "\n")
    g_score = 0
    s_score = 0
    b_score = 0
    t = 60
    cur_lvl = 1
    with open("save.txt", "w+") as f:
        f.writelines(str(cur_lvl) + "\n")
        f.writelines(str(t) + "\n")
        f.writelines(str(g_score) + "\n")
        f.writelines(str(s_score) + "\n")
        f.writelines(str(b_score))
    howtoplay_canvas.forget()
    lvl_one_canvas.forget()
    lvl_two_canvas.forget()
    lvl_three_canvas.forget()
    ldb_canvas.forget()
    pause_canvas.forget()
    game_over_canvas.forget()
    menu_canvas.forget()
    settings_canvas.forget()
    victory_canvas.forget()
    save_menu_canvas.pack(pady=15, padx=15)


# Hides the canvas of the current level and stops the countdown function to
# pause the game
def pause_game(self):
    global paused, cur_lvl, guard_generated
    paused = True
    guard_generated = False
    if cur_lvl == 1:
        lvl_one_canvas.forget()
    elif cur_lvl == 2:
        lvl_two_canvas.forget()
    elif cur_lvl == 3:
        lvl_three_canvas.forget()
    pause_canvas.pack(pady=15, padx=15)


# Recontinues functions and resets the position of the goblin so that the
# user can continue playing with no unfair advantage
def unpause_game():
    global paused, cur_lvl, guard_generated
    paused = False
    pause_canvas.forget()
    guard_generated = True
    if cur_lvl == 1:
        lvl_one_canvas.pack()
        lvl_one_canvas.coords(goblin, 330, 330)
    elif cur_lvl == 2:
        guard_generated = True
        lvl_two_canvas.pack()
        lvl_two_canvas.coords(goblin2, 330, 330)
    elif cur_lvl == 3:
        lvl_three_canvas.pack()
        lvl_three_canvas.coords(goblin3, 330, 330)
    goblin_directions()
    guard_movement()
    countdown()


# Saves the game by writing the player's statistics to an external file
def save_game():
    with open("save.txt", "w+") as f:
        f.writelines(str(cur_lvl) + "\n")
        f.writelines(str(t) + "\n")
        f.writelines(str(g_score) + "\n")
        f.writelines(str(s_score) + "\n")
        f.writelines(str(b_score))
    back_to_save_menu()


# Reads local save file and lets the user play from where they last left off
def load_game():
    global t, g_score, s_score, b_score, cur_lvl, in_game
    in_game = True
    try:
        with open("save.txt", "r") as f:
            cur_lvl = int(f.readline())
            t = int(f.readline())
            g_score = int(f.readline())
            b_score = int(f.readline())
            s_score = int(f.readline())
    except:
        nosave_prompt = messagebox.showinfo("You can't do that!",
                                            "You need to play before you "
                                            "can load a save file.")
    howtoplay_canvas.forget()
    pause_canvas.forget()
    menu_canvas.pack_forget()
    game_over_canvas.forget()
    victory_canvas.forget()
    save_menu_canvas.forget()
    tally["text"] = "Lvl 1 score: " + str(g_score)
    tally2["text"] = "Lvl 2 score: " + str(s_score)
    tally3["text"] = "Lvl 3 score: " + str(b_score)
    if cur_lvl == 1:
        lvl_two_canvas.forget()
        lvl_three_canvas.forget()
        lvl_one_canvas.pack()
        lvl_one_canvas.coords(goblin, 330, 330)
    elif cur_lvl == 2:
        lvl_one_canvas.forget()
        lvl_three_canvas.forget()
        lvl_two_canvas.pack()
        lvl_two_canvas.coords(goblin2, 330, 330)
    elif cur_lvl == 3:
        lvl_one_canvas.forget()
        lvl_two_canvas.forget()
        lvl_three_canvas.pack()
        lvl_three_canvas.coords(goblin3, 330, 330)
    countdown()


# Closes all other potentially open canvasses and packs
# the 'how to play' canvas
def view_howtoplay():
    howtoplay_canvas.forget()
    pause_canvas.forget()
    menu_canvas.pack_forget()
    game_over_canvas.forget()
    save_menu_canvas.forget()
    victory_canvas.forget()
    howtoplay_canvas.pack()


# Closes all other potentially open canvasses and packs the settings canvas
def view_settings():
    howtoplay_canvas.forget()
    pause_canvas.forget()
    menu_canvas.pack_forget()
    game_over_canvas.forget()
    save_menu_canvas.forget()
    victory_canvas.forget()
    settings_canvas.pack()


# Defines the goblin's default movement & borders
def goblin_movement(event):
    global loop, direction, paused
    direction = event.char
    if not paused:
        if loop == 1:
            goblin_directions()
            loop = 0


# Default keybinds
up_key = "w"
left_key = "a"
right_key = "s"
down_key = "d"


# Lets user control the goblin with WASD keys
def set_wasd_keys():
    global up_key, left_key, right_key, down_key
    up_key = "w"
    left_key = "a"
    right_key = "s"
    down_key = "d"


# Lets user control the goblin with ESDF keys
def set_esdf_keys():
    global up_key, left_key, right_key, down_key
    up_key = "e"
    left_key = "s"
    right_key = "d"
    down_key = "f"


# Defines movement of goblin and allows for transition between levels
def goblin_directions():
    global paused, direction, cur_lvl, t, g_score, s_score, b_score, \
           guard_generated
    if cur_lvl == 1:
        goblin_pos = lvl_one_canvas.coords(goblin)
        if not paused:
            if direction == up_key:
                lvl_one_canvas.move(goblin, 0, -10)
            elif direction == left_key:
                lvl_one_canvas.move(goblin, -10, 0)
            elif direction == right_key:
                lvl_one_canvas.move(goblin, 0, 10)
            elif direction == down_key:
                lvl_one_canvas.move(goblin, 10, 0)
            # Prevents the user from leaving the predefined borders
            if goblin_pos[1] < 0:
                lvl_one_canvas.move(goblin, 0, 10)
            elif goblin_pos[1] > 720:
                lvl_one_canvas.move(goblin, 0, -75)
            elif goblin_pos[0] < 0:
                    lvl_one_canvas.move(goblin, 10, 0)
            elif goblin_pos[0] > 720:
                    lvl_one_canvas.move(goblin, -75, 0)
            inc_g_score()
            # Moves user to second level if they reach the required score
            if g_score >= 20:
                lvl_one_canvas.forget()
                cur_lvl = 2
                t = 30
                s_score = 0
                tally2["text"] = "Lvl 2 score: " + str(s_score)
                guard_generated = True
                lvl_two_canvas.pack()
                lvl_two_canvas.coords(goblin2, 330, 330)
            window.after(delay, goblin_directions)
            if guard_generated:
                guard_movement()

    elif cur_lvl == 2:
        goblin_pos = lvl_two_canvas.coords(goblin3)
        if not paused:
            if direction == up_key:
                lvl_two_canvas.move(goblin2, 0, -15)
            elif direction == left_key:
                lvl_two_canvas.move(goblin2, -15, 0)
            elif direction == right_key:
                lvl_two_canvas.move(goblin2, 0, 15)
            elif direction == down_key:
                lvl_two_canvas.move(goblin2, 15, 0)
            # Prevents the user from leaving the predefined borders
            if goblin_pos[1] < 0:
                lvl_two_canvas.move(goblin2, 0, 75)
            elif goblin_pos[1] > 720:
                lvl_two_canvas.move(goblin2, 0, -75)
            elif goblin_pos[0] < 0:
                    lvl_two_canvas.move(goblin2, 75, 0)
            elif goblin_pos[0] > 720:
                    lvl_two_canvas.move(goblin2, -75, 0)
            inc_s_score()
            # Moves user to third level if they reach the required score
            if s_score >= 25:
                lvl_two_canvas.forget()
                cur_lvl = 3
                t = 30
                b_score = 0
                tally3["text"] = "Lvl 3 score: " + str(b_score)
                guard_generated = True
                lvl_three_canvas.pack()
                lvl_three_canvas.coords(goblin3, 330, 330)
            window.after(delay, goblin_directions)

    elif cur_lvl == 3:
        goblin_pos = lvl_three_canvas.coords(goblin3)
        if not paused:
            if direction == up_key:
                lvl_three_canvas.move(goblin3, 0, -20)
            elif direction == left_key:
                lvl_three_canvas.move(goblin3, -20, 0)
            elif direction == right_key:
                lvl_three_canvas.move(goblin3, 0, 20)
            elif direction == down_key:
                lvl_three_canvas.move(goblin3, 20, 0)
            # Prevents the user from leaving the predefined borders
            if goblin_pos[1] < 0:
                lvl_three_canvas.move(goblin3, 0, 75)
            elif goblin_pos[1] > 720:
                lvl_three_canvas.move(goblin3, 0, -75)
            elif goblin_pos[0] < 0:
                    lvl_three_canvas.move(goblin3, 75, 0)
            elif goblin_pos[0] > 720:
                    lvl_three_canvas.move(goblin3, -75, 0)

            inc_b_score()
            # Moves user to final victory screen if they reach the required
            # score
            if b_score >= 30:
                lvl_two_canvas.forget()
                lvl_three_canvas.forget()
                t = 60
                victory_canvas.pack()
                with open("ldb.txt", "a+") as f:
                    f.write(os.getlogin() + "," + str(totalscore) + "\n")
                g_score = 0
                s_score = 0
                b_score = 0
                t = 60
                cur_lvl = 1
                with open("save.txt", "w+") as f:
                    f.writelines(str(cur_lvl) + "\n")
                    f.writelines(str(t) + "\n")
                    f.writelines(str(g_score) + "\n")
                    f.writelines(str(s_score) + "\n")
                    f.writelines(str(b_score))
            window.after(delay, goblin_directions)


# Creates and places the gold coin for the first level
def generate_gold_coin():
    global g_coin
    g_coin_x = float(random.randint(0, 500))
    g_coin_y = float(random.randint(0, 500))
    g_coin = lvl_one_canvas.create_oval(g_coin_x, g_coin_y, g_coin_x+20,
                                        g_coin_y+20, fill="gold")


# Creates and places the silver coin for the second level
def generate_silver_coin():
    global s_coin
    s_coin_x = float(random.randint(0, 500))
    s_coin_y = float(random.randint(0, 500))
    s_coin = lvl_two_canvas.create_oval(s_coin_x, s_coin_y, s_coin_x+20,
                                        s_coin_y+20, fill="silver")


# Creates and places the bronze coin for the third level
def generate_bronze_coin():
    global b_coin
    b_coin_x = float(random.randint(0, 500))
    b_coin_y = float(random.randint(0, 500))
    b_coin = lvl_three_canvas.create_oval(b_coin_x, b_coin_y, b_coin_x+20,
                                          b_coin_y+20, fill="brown")


# Detects sprite collision & increments first level's score
def inc_g_score():
    global g_score, g_coin
    a = lvl_one_canvas.bbox(goblin)
    b = lvl_one_canvas.bbox(g_coin)
    if b[0] in range(a[0], a[2]) and b[2] in range(a[0], a[2]) and \
       b[1] in range(a[1], a[3]) and b[3] in range(a[1], a[3]):
        lvl_one_canvas.delete(g_coin)
        g_score += 2
        tally["text"] = "Lvl 1 score: " + str(g_score)
        generate_gold_coin()


# Detects sprite collision & increments second level's score
def inc_s_score():
    global s_score, s_coin
    a = lvl_two_canvas.bbox(goblin2)
    b = lvl_two_canvas.bbox(s_coin)
    if b[0] in range(a[0], a[2]) and b[2] in range(a[0], a[2]) and \
       b[1] in range(a[1], a[3]) and b[3] in range(a[1], a[3]):
        lvl_two_canvas.delete(s_coin)
        s_score += 1
        tally2["text"] = "Lvl 2 score: " + str(s_score)
        generate_silver_coin()


# Detects sprite collision & increments third level's score
def inc_b_score():
    global b_score, b_coin
    a = lvl_three_canvas.bbox(goblin3)
    b = lvl_three_canvas.bbox(b_coin)
    if b[0] in range(a[0], a[2]) and b[2] in range(a[0], a[2]) and \
       b[1] in range(a[1], a[3]) and b[3] in range(a[1], a[3]):
        lvl_three_canvas.delete(b_coin)
        b_score += 1
        tally3["text"] = "Lvl 3 score: " + str(b_score)
        generate_bronze_coin()


# Initialises a countdown that forces user to accumulate points within
# the desired time
def countdown():
    global t, cur_lvl, in_game, totalscore
    totalscore = g_score + s_score + b_score
    if cur_lvl == 1:
        if not paused and in_game:
            if t > 0:
                print(t)
                t -= 1
                timer["text"] = "Time remaining: " + str(t)
                window.after(1000, countdown)
            elif t == 0:
                lvl_one_canvas.forget()
                # Forces user to lose the game if they run out of time
                game_over_canvas.itemconfig(game_over_text,
                                            text=f"You lost! Your final score "
                                            f"was {totalscore}!")
                game_over_canvas.pack(pady=15, padx=15)
    elif cur_lvl == 2:
        if not paused and in_game:
            if t > 0:
                print(t)
                t -= 1
                timer2["text"] = "Time remaining: " + str(t)
                window.after(1000, countdown)
            elif t == 0:
                lvl_two_canvas.forget()
                # Forces user to lose the game if they run out of time
                game_over_canvas.itemconfig(game_over_text,
                                            text=f"You lost! Your final score "
                                            f"was {totalscore}!")
                game_over_canvas.pack(pady=15, padx=15)
    elif cur_lvl == 3:
        if not paused and in_game:
            if t > 0:
                print(t)
                t -= 1
                timer3["text"] = "Time remaining: " + str(t)
                window.after(1000, countdown)
            elif t == 0:
                lvl_three_canvas.forget()
                # Forces user to lose the game if they run out of time
                game_over_canvas.itemconfig(game_over_text,
                                            text=f"You lost! Your final score "
                                            f"was {totalscore}!")
                game_over_canvas.pack(pady=15, padx=15)


# Defines the movement and limitations of the guards for the second and third
# level respectively
def guard_movement():
    global paused, delay, guard_generated
    guard_generated = True
    guard_pos = lvl_two_canvas.coords(guard)
    guard2_pos = lvl_three_canvas.coords(guard2)
    guard_collision()
    # Defines the movement of the guard in the second level
    if cur_lvl == 2:
        if not paused and guard_generated:
            if guard_pos[1] < 0:
                lvl_two_canvas.move(guard, 0, 30)
            elif guard_pos[1] > 0 and guard_pos[1] < 720:
                lvl_two_canvas.move(guard, 0, 2)
            elif guard_pos[1] >= 720:
                lvl_two_canvas.move(guard, 0, -600)
            window.after(delay, guard_movement)
    # Defines the movement of the guard in the third level
    elif cur_lvl == 3:
        if not paused and guard_generated:
            if guard2_pos[0] > 0:
                lvl_three_canvas.move(guard2, -8, 8)
            elif guard2_pos[0] <= 0 and guard2_pos[1] >= 490:
                lvl_three_canvas.move(guard2, 200, -200)
            window.after(delay, guard_movement)


# Ends the game when player collides with any guard
def guard_collision():
    global totalscore
    totalscore = g_score + s_score + b_score
    if cur_lvl == 2:
        d = lvl_two_canvas.bbox(guard)
        collision = lvl_two_canvas.find_overlapping(*d)
        if len(collision) == 2:
            lvl_two_canvas.forget()
            game_over_canvas.itemconfig(game_over_text,
                                        text=f"You lost! Your final score "
                                        f"was {totalscore}!")
            game_over_canvas.pack(pady=15, padx=15)
    if cur_lvl == 3:
        e = lvl_three_canvas.bbox(guard2)
        collision2 = lvl_three_canvas.find_overlapping(*e)
        if len(collision2) == 2:
            lvl_three_canvas.forget()
            game_over_canvas.itemconfig(game_over_text,
                                        text=f"You lost! Your final score was "
                                        f"{totalscore}!")
            game_over_canvas.pack(pady=15, padx=15)


# Creates a boss key that overlays a fake photo of the Google Chrome home page
# and redefines window title
def boss_key(self):
    global work
    window.title("Google Chrome")
    window.config(bg="#fff")
    menu_canvas.config(bg="#fff")
    save_menu_canvas.config(bg="#fff")
    ldb_canvas.config(bg="#fff")
    pause_canvas.config(bg="#fff")
    game_over_canvas.config(bg="#fff")
    lvl_one_canvas.config(bg="#fff")
    lvl_two_canvas.config(bg="#fff")
    lvl_three_canvas.config(bg="#fff")
    howtoplay_canvas.config(bg="#fff")
# Photo source:
# https://commons.wikimedia.org/wiki/File:Google_Chrome_Interface_Home_Page.png
    work_pic = PhotoImage(file="./assets/chrome.png")
    work = Label(image=work_pic)
    work.image = work_pic
    work.place(x=0, y=0)


# Restores canvas colours and window title when the boss key is disabled
def disable_boss_key(self):
    global work
    work.destroy()
    window.title("Rush")
    window.config(bg="#0E2F44")
    menu_canvas.config(bg="#0E2F44")
    save_menu_canvas.config(bg="#0E2F44")
    ldb_canvas.config(bg="#0E2F44")
    pause_canvas.config(bg="#0E2F44")
    game_over_canvas.config(bg="#0E2F44")
    lvl_one_canvas.config(bg="#0E2F44")
    lvl_two_canvas.config(bg="#6699ff")
    lvl_three_canvas.config(bg="#6600ff")
    howtoplay_canvas.config(bg="#0E2F44")


# Increments score on demand (cheat key)
def cheat_score(self):
    global g_score, b_score, s_score, totalscore
    if cur_lvl == 1:
        g_score += 5
    elif cur_lvl == 2:
        s_score += 5
    elif cur_lvl == 3:
        b_score += 2
    totalscore = g_score + s_score + b_score
    tally["text"] = "Lvl 1 score: " + str(g_score)
    tally2["text"] = "Lvl 2 score: " + str(s_score)
    tally3["text"] = "Lvl 3 score: " + str(b_score)

configure_window()

# Window & canvas variables
h = 2560
w = 1440
x = w/2
y = h/2
# Movement variables
delay = 30
loop = 1
# Initialises variables
g_coin_x = g_coin_y = 0
s_coin_x = s_coin_y = 0
b_coin_x = b_coin_y = 0
t = 60
g_score = 0
s_score = 0
b_score = 0
cur_lvl = 1
# Conditional variables
in_game = False
paused = False
guard_generated = False

# Displays main menu screen
menu_canvas = Canvas(window, width=x, height=y, bg="#0E2F44",
                     highlightthickness=0)
menu_canvas.pack(pady=15, padx=15)
title_text = Label(menu_canvas, text="Welcome to Rush!", bg="#0E2F44",
                   fg="white", font=('Verdana', 25))
title_text.pack(pady=15, padx=15)
start_game_btn = Button(menu_canvas, font=('Verdana', 20), text="Start",
                        relief="raised", borderwidth=3, command=start_game)
start_game_btn.pack(pady=15, padx=15)
load_game_btn = Button(menu_canvas, font=('Verdana', 20), text="Load",
                       relief="raised", borderwidth=3, command=load_game)
load_game_btn.pack(pady=15, padx=15)
instructions_btn = Button(menu_canvas, font=('Verdana', 20),
                          text="How to play", relief="raised", borderwidth=3,
                          command=view_howtoplay)
instructions_btn.pack(pady=15, padx=15)
leaderboards_btn = Button(menu_canvas, font=('Verdana', 20),
                          text="View leaderboard", relief="raised",
                          borderwidth=3, command=view_ldb)
leaderboards_btn.pack(pady=15, padx=15)
settings_btn = Button(menu_canvas, font=('Verdana', 20), text="Settings",
                      relief="raised", borderwidth=3, command=view_settings)
settings_btn.pack(pady=15, padx=15)
quit_game_btn = Button(menu_canvas, font=('Verdana', 20), text="Quit",
                       relief="raised", borderwidth=3, command=quit_game)
quit_game_btn.pack(pady=15, padx=15)

# Displays a menu after the user saves the game
save_menu_canvas = Canvas(window, width=x, height=y, bg="#0E2F44",
                          highlightthickness=0)
title_text = Label(save_menu_canvas, text="Game saved!", bg="#0E2F44",
                   fg="white", font=('Verdana', 25))
title_text.pack(pady=15, padx=15)
start_game_btn = Button(save_menu_canvas, font=('Verdana', 20), text="Start",
                        relief="raised", borderwidth=3, command=start_game)
start_game_btn.pack(pady=15, padx=15)
load_game_btn = Button(save_menu_canvas, font=('Verdana', 20), text="Load",
                       relief="raised", borderwidth=3, command=load_game)
load_game_btn.pack(pady=15, padx=15)
instructions_btn = Button(save_menu_canvas, font=('Verdana', 20),
                          text="How to play", relief="raised", borderwidth=3,
                          command=view_howtoplay)
instructions_btn.pack(pady=15, padx=15)
leaderboards_btn = Button(save_menu_canvas, font=('Verdana', 20),
                          text="View leaderboard", relief="raised",
                          borderwidth=3, command=view_ldb)
leaderboards_btn.pack(pady=15, padx=15)
settings_btn = Button(save_menu_canvas, font=('Verdana', 20), text="Settings",
                      relief="raised", borderwidth=3, command=view_settings)
settings_btn.pack(pady=15, padx=15)
quit_game_btn = Button(save_menu_canvas, font=('Verdana', 20), text="Quit",
                       relief="raised", borderwidth=3, command=quit_game)
quit_game_btn.pack(pady=15, padx=15)

# Displays a canvas that teaches the user how to play
howtoplay_canvas = Canvas(window, width=w, height=h, bg="#0E2F44",
                          highlightthickness=0)
howtoplay_title_text = Label(howtoplay_canvas, text="How To Play",
                             bg="#0E2F44", fg="white", font=('Verdana', 25))
howtoplay_title_text.pack(pady=15, padx=15)
howtoplay_text = Label(howtoplay_canvas, text="Welcome to Rush.",
                       bg="#0E2F44", fg="white", font=('Verdana', 15))
howtoplay_text.pack(pady=25, padx=15)
howtoplay_text_2 = Label(howtoplay_canvas,
                         text="Use WASD (default) to move your goblin and "
                         "collect all the coins before time runs out (or you "
                         "hit a guard)!",
                         bg="#0E2F44", fg="white", font=('Verdana', 15))
howtoplay_text_2.pack(pady=25, padx=15)
howtoplay_text_3 = Label(howtoplay_canvas, text="Click the 'Esc' key at any "
                         "time in-game to pause the game! You can also save "
                         "and exit at the top right of each level!",
                         bg="#0E2F44", fg="white", font=('Verdana', 15))
howtoplay_text_3.pack(pady=25, padx=15)
howtoplay_text_4 = Label(howtoplay_canvas, text="There is a boss key if "
                         "you're ever playing at work and need to hide the "
                         "game from your boss! Just click 'B' to enable work "
                         "mode and 'X' to disable it!",
                         bg="#0E2F44", fg="white", font=('Verdana', 10))
howtoplay_text_4.pack(pady=20, padx=15)
howtoplay_text_5 = Label(howtoplay_canvas, text="Want a little more fun? "
                         "Click 'U' and watch your score effortlessly "
                         "increase as you move!", bg="#0E2F44", fg="white",
                         font=('Verdana', 10))
howtoplay_text_5.pack(pady=20, padx=15)

back_to_menu_btn = Button(howtoplay_canvas, font=('Verdana', 20),
                          text="Back to menu", relief="raised", borderwidth=3,
                          command=back_to_menu)
back_to_menu_btn.pack(pady=80, padx=15)

# Displays the leaderboard canvas
ldb_canvas = Canvas(window, width=2560, height=1440, bg="#0E2F44",
                    highlightthickness=0)
ldb_title_text = Label(ldb_canvas, text="Leaderboard", bg="#0E2F44",
                       fg="white",
                       font=("Arial", 25)).grid(row=0, columnspan=4)
cols = ('Rank', 'OS Name', 'Score')
ldb_tree = ttk.Treeview(ldb_canvas, columns=cols, show='headings')
for col in cols:
    ldb_tree.heading(col, text=col)
ldb_tree.grid(row=1, column=0, columnspan=2)

ldb_view_scores_btn = Button(ldb_canvas, text="Show / Update", width=15,
                             command=view_scores).grid(row=4, column=0)
back_to_menu_btn = Button(ldb_canvas, text="Close", width=15,
                          command=back_to_menu).grid(row=4, column=1)


# Displays the settings screen where user can define the keys for the
# goblin's movement
settings_canvas = Canvas(window, width=w, height=h, bg="#0E2F44",
                         highlightthickness=0)
settings_title_text = Label(settings_canvas, text="Settings", bg="#0E2F44",
                            fg="white", font=('Verdana', 25))
settings_title_text.pack(pady=15, padx=15)
settings_text = Label(settings_canvas, text="Welcome to settings, where you "
                      "can configure your keybinds.", bg="#0E2F44",
                      fg="white", font=('Verdana', 15))
settings_text.pack(pady=25, padx=15)
back_to_menu_btn = Button(settings_canvas, font=('Verdana', 10),
                          text="Set to WASD keys", relief="raised",
                          borderwidth=3, command=set_wasd_keys)
back_to_menu_btn.pack(pady=10, padx=15)
back_to_menu_btn = Button(settings_canvas, font=('Verdana', 10),
                          text="Set to ESDF keys", relief="raised",
                          borderwidth=3, command=set_esdf_keys)
back_to_menu_btn.pack(pady=0, padx=15)
back_to_menu_btn = Button(settings_canvas, font=('Verdana', 20),
                          text="Back to menu", relief="raised", borderwidth=3,
                          command=back_to_menu)
back_to_menu_btn.pack(pady=150, padx=15)

# FIRST LEVEL CANVAS
lvl_one_canvas = Canvas(window, width=x, height=y, bg="#0E2F44")

tally = Label(window, text="Lvl 1 score: " + str(g_score))
tally.pack()
lvl_one_canvas.create_window(670, 10, window=tally)

timer = Label(window, text="Get ready!", bg="#0E2F44", fg="white")
timer.pack()
lvl_one_canvas.create_window(70, 15, window=timer)

lvl_one_text = lvl_one_canvas.create_text((340, 15),
                                          text="LEVEL ONE - 20 points "
                                          "to move on!", fill="white")

# Free goblin icon made by Freepik:
# https://www.flaticon.com/free-icon/goblin_3408641
goblin_pic = PhotoImage(file="./assets/goblin.png")
goblin = lvl_one_canvas.create_image(330, 330, anchor="nw", image=goblin_pic)

save_and_exit_btn = Button(lvl_one_canvas, font=('Verdana', 8), text="Save "
                           "and Exit", relief="raised",
                           borderwidth=3, command=save_game)
save_and_exit_btn.place(x=615, y=40)

# SECOND LEVEL CANVAS
lvl_two_canvas = Canvas(window, width=x, height=y, bg="#6699ff")

tally2 = Label(window, text="Lvl 2 score: " + str(s_score))
tally2.pack()
lvl_two_canvas.create_window(670, 10, window=tally2)

timer2 = Label(window, text="Get ready!", bg="#6699ff", fg="white")
timer2.pack()
lvl_two_canvas.create_window(70, 15, window=timer2)

lvl_two_text = lvl_two_canvas.create_text((340, 15), text="LEVEL TWO "
                                          "- 25 points to move on!",
                                          fill="white")

# Free goblin icon made by Freepik:
# https://www.flaticon.com/free-icon/goblin_3408641
goblin_pic2 = PhotoImage(file="./assets/goblin.png")
goblin2 = lvl_two_canvas.create_image(530, 530, anchor="nw", image=goblin_pic2)

# Free guard icon made by Freepik:
# https://www.flaticon.com/free-icon/policeman_1022331
guard_pic = PhotoImage(file="./assets/guard.png")
guard = lvl_two_canvas.create_image(180, -100, anchor="nw", image=guard_pic)

save_and_exit_btn = Button(lvl_two_canvas, font=('Verdana', 8), text="Save "
                           "and Exit", relief="raised", borderwidth=3,
                           command=save_game)
save_and_exit_btn.place(x=615, y=40)

# THIRD LEVEL CANVAS
lvl_three_canvas = Canvas(window, width=x, height=y, bg="#6600ff")

tally3 = Label(window, text="Lvl 3 score: " + str(b_score))
tally3.pack()
lvl_three_canvas.create_window(670, 10, window=tally3)

timer3 = Label(window, text="Get ready!", bg="#6600ff", fg="white")
timer3.pack()
lvl_three_canvas.create_window(70, 15, window=timer3)

lvl_three_text = lvl_three_canvas.create_text((340, 15), text="LEVEL THREE "
                                              "- 30 points to win!",
                                              fill="white")

# Free goblin icon made by Freepik:
# https://www.flaticon.com/free-icon/goblin_3408641
goblin_pic3 = PhotoImage(file="./assets/goblin.png")
goblin3 = lvl_three_canvas.create_image(330, 330,
                                        anchor="nw", image=goblin_pic3)

# Free guard icon made by Freepik:
# https://www.flaticon.com/free-icon/policeman_1022331
guard_pic2 = PhotoImage(file="./assets/guard.png")
guard2 = lvl_three_canvas.create_image(480, 10, anchor="nw", image=guard_pic2)

save_and_exit_btn = Button(lvl_three_canvas, font=('Verdana', 8),
                           text="Save and Exit", relief="raised",
                           borderwidth=3, command=save_game)
save_and_exit_btn.place(x=615, y=40)

# Displays a canvas when the game is paused
pause_canvas = Canvas(window, width=x, height=y, bg="#0E2F44",
                      highlightthickness=0)
pause_text_border = pause_canvas.create_rectangle(280, 200, 420, 240,
                                                  fill="#dfe9d7")
pause_text = pause_canvas.create_text((350, 210), text="Game paused.")
unpause_btn = Button(pause_canvas, font=('Verdana', 5), text="Continue",
                     relief="flat", command=unpause_game)
unpause_btn.place(x=330, y=220)

# Displays a canvas when the game is lost
game_over_canvas = Canvas(window, width=x, height=y, bg="#0E2F44",
                          highlightthickness=0)
game_over_text_border = game_over_canvas.create_rectangle(180, 200, 520, 240,
                                                          fill="#dfe9d7")
game_over_text = game_over_canvas.create_text((350, 210), text=f"Game over!")
game_over_btn = Button(game_over_canvas, font=('Verdana', 6), text="Okay",
                       relief="flat", command=game_loss_menu)
game_over_btn.place(x=325, y=220)

# Displays a canvas when the game is won
victory_canvas = Canvas(window, width=w, height=h, bg="#0E2F44",
                        highlightthickness=0)
victory_title_text = Label(victory_canvas, text="Congratulations, you have "
                           "won the Rush!", bg="#0E2F44", fg="white",
                           font=('Verdana', 25))
victory_title_text.pack(pady=15, padx=15)
victory_text = Label(victory_canvas, text="Well done, you've made it all"
                     "the way through. You have proven that you have what it "
                     "takes to win.", bg="#0E2F44", fg="white",
                     font=('Verdana', 15))
victory_text.pack(pady=25, padx=15)
back_to_menu_btn = Button(victory_canvas, font=('Verdana', 20), text="I'm "
                          "happy, take me home", relief="raised",
                          borderwidth=3, command=back_to_menu)
back_to_menu_btn.pack(pady=150, padx=15)

# Generates the coins for each level
generate_gold_coin()
generate_silver_coin()
generate_bronze_coin()

# Binds the appropiate keys for the desired functions
window.bind("<Key>", goblin_movement)
window.bind("B", boss_key)
window.bind("b", boss_key)
window.bind("X", disable_boss_key)
window.bind("x", disable_boss_key)
window.bind("U", cheat_score)
window.bind("u", cheat_score)
window.bind("<Escape>", pause_game)
window.mainloop()
