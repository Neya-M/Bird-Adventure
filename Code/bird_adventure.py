import os
import sys
import math

# TODO: add more commands


# functions
class Game_engine():
    days_left = 14
    time_until_sunset = 12  # this will change by at least .25 for most actions
    player_pos = [10, 10]
    map_size = [25, 15]
    player_icon = "&"
    map_storage = ["~~~..~~~~~~..**TTTTTT^TTT",
                   "~o.**.~~~~...**TTTTT/#\\TT",
                   "~~.*V*.~~~....**TTT/###\\T",
                   "~~~.**.~~~....**TT/#####\\",
                   "~~~~..t~~~...***T/####O##",
                   "~~~~~~~~....**T*TTTTTTTTT",
                   "~~~~~~~...T*******T*T*T*T",
                   "...~~~...****~~~**TTTTT*T",
                   "......********~~~***TTTTT",
                   "*****T**TTTT**~~~~~**TTTT",
                   "~~~*****TTYTT**~~~~~**TTT",
                   "**~~~~****T*TT*****~~*TTT",
                   "Tf**~~~**T*TTTTTT*******T",
                   "TTT***~~~**T*TTT**TTTTTTT",
                   "TTTT***~~~**TTTTTTTTT*TTT"]
    map_display = [bytearray(x, 'utf-8') for x in map_storage]

    prev_player = [0, 0]

    # command lists
    valid_commands = ["north", "south", "east", "west", "help", "look", "take",
                      "inventory", "examine", "sleep", "speak", "make",
                      "enter", "l", "m", "x", "t", "i", "n", "s", "e", "w"]
    commands_up = ["north", "n"]
    commands_down = ["south", "s"]
    commands_left = ["west", "w"]
    commands_right = ["east", "e"]
    look = {"T": "Tall trees tower over you, filtering light through their" +
            " leaves. They remind you of your nest not too far away.",
            "*": "The foliage is shorter than deep in the forest and there are"
            + " many small bushes and wildflowers. You notice some blueberries"
            + " on a nearby bush.",
            "~": "Below you is a large body of water. It sparkles in the " +
            "morning sun.",
            "#": "A rocky mountain lies below you. You can see a glimmer of" +
            " snow at its peak.",
            "O": "In front of you is a very dark cave. You can't tell what's" +
            " inside.",
            ".": "You see a sandy beach. Some crabs scuttle around, and the " +
            "waves slowly lap against the shore. You notice a bottle wash up" +
            " on shore.",
            "/": "A rocky mountain lies below you. You can see a glimmer of" +
            " snow at its peak.",
            "\\": "A rocky mountain lies below you. You can see a glimmer of" +
            " snow at its peak.",
            "^": "You land in some soft snow on the very peak of the mountain."
            + " You can see all the way to the ocean. You notice a small " +
            "patch of green in the middle of the water.",
            "Y": "You are standing below your nest. Your mother will be home" +
            " by sunset, and she'll be mad if she realizes you've left alone.",
            "V": "You see a volcano below you oozing lava.",
            "o": "There is a sea otter in the water below.",
            "f": "You see a small tree frog next to the river.",
            "t": "There is a turtle next to you in the ocean.",
            "b": "There is a baby turtle stuck in the rocks."}
    examine_dbl = {"ground": {"T": "You see a pretty leaf on the ground.",
                              "Y": "Seems sturdy enough.",
                              "*": "There are a few sticks here and there.",
                              "~": "What ground?",
                              "o": "What ground?",
                              "#": "There are a few rocks on the ground",
                              "/": "Pretty solid.",
                              "\\": "Why are you staring at the ground?",
                              "O": "A loamy mixture of clay, sand, and silt.",
                              ".": "Much sand. Very sand.",
                              "^": "The ground is covered in fresh snow. You" +
                              " notice a sparkly and blue gem stuck in the " +
                              "snow",
                              "V": "The floor is lava!"}}
    examine = {"self": "You are a bird.",
               "inventory": "Run 'i' or 'inventory' to see your inventory."}
    examine_here = {"rock": "A pretty blue rock.",
                    "leaf": "A red, orange, and yellow maple leaf.",
                    "stick": "I am a stick.",
                    "flower": "A small branch of blue, pink, and white forget "
                    + "me not flowers.",
                    "bottle": "A metal insulated water bottle.",
                    "gem": "Ooh shiny!",
                    "blueberries": "Berries that are blue.",
                    "water": "Should be fine to drink.",
                    "baby turtle": "Aww it's so cute >u<",
                    "popsicle": "Cold.",
                    "torch": "AHHH IT BURNS!!",
                    "door": "The door has 3 slots, and it reads: find 3 gems" +
                    " to enter."}
    items = {"snow": "^", "bottle": ".", "water": "~", "stick": "*",
             "blue gem": "^", "blueberries": "*", "leaf": "T", "flower": "*",
             "sand": ".", "rock": "#", "door": "O", "nil": ""}
    make = {"flower crown": "You weave sticks and flowers into a flower crown,"
            + " and add the leaf on as a finishing touch. Then, you notice the"
            + " flowers starting to wilt. You need a way to keep it fresh unti"
            + "l Mother's Day!",
            "torch": "You dip the stick into the lava and wait for it to catch"
            " fire.",
            "popsicle": "You mold some snow into a rectangle and squeeze some "
            + "blueberry juice into it. Then you pour water on it, add a " +
            "stick, and wait for it to freeze into a solid popsicle. You store"
            + " it in an insulated bottle to stop it from melting."}
    convos = {"o": ["hi there :)", "You: hi!", "do you have any rocks?",
                    "You: uh what?", "I like pretty rocks, I have this green" +
                    " gem but I like blue more. I could trade if you have " +
                    "one!"],
              "f": ["ugghh it's so hot... I wish I had a popsicle...",
                    "You: sorry, I don't have any :(", "You: I have one I " +
                    "could give you!", "thanks! Oh by the way, I saw a baby " +
                    "turtle get stuck in between some rocks, could you help me"
                    + " get it out?", "You: maybe, where is it?", "Just " +
                    "southeast of here."],
              "b": ["help me! I'm stuck!", "You: are you ok?", "yeah", "You: "
                    + "ok I'll get you out of there.", "thank you! My mom is" +
                    " near the island, can you take me there?",
                    "You: of course!"],
              "t": ["have you seen my baby anywhere? She disappeared a few " +
                    "days ago and I'm worried!", "no, sorry.",
                    "yes, I found her stuck in between some rocks in the river"
                    + ".", "thank you!! Here, take this gem."]}
    inventory = []

    def clear_screen_and_line(self):
        # Clear the entire screen
        os.system('cls' if os.name == 'nt' else 'clear')

        # Clear the current input line
        sys.stdout.write('\033[K')
        sys.stdout.flush()

    def stretch_coords(self, coords):
        return coords[1] * self.map_size[0] + coords[0]

    def stretch_list(self, mylist):
        return mylist.join()

    def generate_map(self, map_array):
        map_array = [bytearray(x, 'utf-8') for x in self.map_storage]
        map_array[
            self.player_pos[1]][self.player_pos[0]] = ord(self.player_icon)
        return map_array

    def print_map(self):
        to_print = []
        for i in range(9):
            x = (i % 3) + self.player_pos[0] - 1
            y = (i // 3) + self.player_pos[1] - 1
            if 0 <= x < self.map_size[0] and 0 <= y < self.map_size[1]:
                byte_value = self.map_display[y][x]
                char = chr(byte_value)
                to_print.append(char)
            else:
                to_print.append(' ')  # out-of-bounds placeholder

        print(" ".join(to_print[0:3]))
        print(" ".join(to_print[3:6]))
        print(" ".join(to_print[6:9]))
        print("\n")

    def get_curr_tile(self):
        return self.map_storage[self.player_pos[1]][self.player_pos[0]]

    def in_list(self, item, lst):
        return any(key.lower() in item.lower() for key in lst)

    def list_idx(self, item, lst):
        return next(
            (key for key in lst if key.lower() in item.lower()),
            "nil"
        )

    def other_command(self, player_command):
        # spaceless commands
        if player_command == 'speak':
            self.talk()
            return
        if player_command[0] == 'l':
            print(self.look[self.get_curr_tile()])
            return
        if player_command[0] == 'i':
            print("You have: " + ", ".join(self.inventory))
            return
        if player_command == "sleep":
            if self.get_curr_tile() == "Y":
                self.time_until_sunset = 12
                self.days_left -= 1
                print("You drift off in your cozy nest...")
            else:
                print("You need to return to your nest first!")
            return
        if player_command == "enter" and self.get_curr_tile() == 'O':
            if 'torch' in self.inventory:
                gems = ['red gem', 'blue gem', 'green gem']
                if all(i in self.inventory for i in gems):
                    return
                else:
                    print("A large metal door blocks the way.")
                    return
            else:
                print("It's too dark to see and you're not taking any chances."
                      )
                return
        # command + item
        self.adv_command(player_command)
        return

    def adv_command(self, player_command):
        if ' ' in player_command:
            cmd_item = player_command.split(' ', 1)[1]
        else:
            print('please specify an item')
            return
        itms_key = self.list_idx(cmd_item, self.items)
        if player_command[0] == 'x' or player_command[1] == 'x':
            self.examine_cmd(cmd_item)
            return
        if player_command[0] == 't':
            if self.in_list(cmd_item,
                            self.items) and self.items[
                                itms_key] == self.get_curr_tile():
                if itms_key == 'water' and 'bottle' not in self.inventory:
                    print("You need something to store it in.")
                    return
                if itms_key == 'door':
                    print("You can't take that.")
                    return
                if itms_key not in self.inventory:
                    self.inventory.append(itms_key)
                print(itms_key + " added to inventory.")
                return
        if player_command[0] == 'm':
            self.make_cmd(cmd_item)
            return
        print("I don't know what a(n) " + str(cmd_item) + " is.")

    def examine_cmd(self, itm):
        if self.in_list(itm, self.examine):
            print(self.examine[self.list_idx(itm, self.examine)])
            return
        if self.in_list(itm, self.examine_dbl):
            dbl_key = self.list_idx(itm, self.examine_dbl)
            if self.get_curr_tile() in self.examine_dbl[dbl_key]:
                print(self.examine_dbl[dbl_key][
                    self.get_curr_tile()])
                return
        if self.in_list(itm, self.inventory) or (
            self.in_list(itm, self.items) and self.items[
                self.list_idx(itm, self.items)] == self.get_curr_tile()):
            if self.in_list(itm, self.examine_here):
                print(self.examine_here[self.list_idx(itm, self.examine_here)])
                return
        print("I don't see a(n) " + str(itm) + " here.")

    def talk(self):
        if self.get_curr_tile() == 'o':
            self.otter()
        if self.get_curr_tile() == 'f':
            self.frog()
        if self.get_curr_tile() == 'b':
            with open('baby_turtle.txt') as f:
                contents = f.read()
                for sentence in self.convos['b']:
                    self.clear_screen_and_line()
                    print(contents)
                    input("\n" + sentence)
                f.close()
            self.map_storage[14] = "TTTT***~~~**TTTTTTTTT*TTT"
            self.inventory.append("baby turtle")
        if self.get_curr_tile() == 't':
            with open('turtle.txt') as f:
                contents = f.read()
                self.clear_screen_and_line()
                print(contents)
                input("\n" + self.convos['t'][0])
                if 'baby turtle' in self.inventory:
                    for sentence in self.convos['t'][2:5]:
                        self.clear_screen_and_line()
                        print(contents)
                        input("\n" + sentence)
                    self.inventory.append("red gem")
                    self.inventory.remove("baby turtle")
                else:
                    print(self.convos['t'][1])
                f.close()

    def otter(self):
        with open('otter.txt') as f:
            contents = f.read()
            for sentence in self.convos['o']:
                self.clear_screen_and_line()
                print(contents)
                input("\n" + sentence)
            f.close()
            if 'rock' in self.inventory:
                give_rock = input("give rock? Y/N: ")
                if 'y' in give_rock or "Y" in give_rock:
                    self.inventory.remove('rock')
                    self.inventory.append('green gem')
                    print("Thank you :D")

    def frog(self):
        with open('frog.txt') as f:
            contents = f.read()
            self.clear_screen_and_line()
            print(contents)
            input("\n" + self.convos['f'][0])
            if 'popsicle' in self.inventory:
                give_popsicle = input("give popsicle? Y/N: ")
                if 'y' in give_popsicle or 'Y' in give_popsicle:
                    self.inventory.remove('popsicle')
                    self.inventory.append('bottle')
                    self.map_storage[14] = "TTTT**b~~~**TTTTTTTTT*TTT"
                    for sentence in self.convos['f'][2:6]:
                        self.clear_screen_and_line()
                        print(contents)
                        input("\n" + sentence)
                        f.close()
                    return
            self.clear_screen_and_line()
            print(contents)
            print(self.convos['f'][1])
            f.close()

    def make_cmd(self, cmd_item):
        parts1 = ["stick", "leaf", "flower"]
        parts2 = ["blueberries", "water", "stick", "bottle"]
        if cmd_item == "flower crown" and all(i in self.inventory for i in
                                              parts1):
            print(self.make[cmd_item])
            self.inventory.append("flower crown (wilted)")
            self.inventory.remove("stick")
            self.inventory.remove("leaf")
            self.inventory.remove("flower")
        elif cmd_item == "torch" and "stick" in self.inventory:
            if self.get_curr_tile() == "V":
                print(self.make['torch'])
                self.inventory.append('torch')
                self.inventory.remove('stick')
            else:
                print("nothing to light the stick.")
        elif cmd_item == 'popsicle' and all(i in self.inventory for i in
                                            parts2) and self.get_curr_tile(
        ) == '^':
            self.inventory.remove('water')
            self.inventory.remove('bottle')
            self.inventory.remove('blueberries')
            self.inventory.remove('stick')
            self.inventory.append('popsicle')
            print(self.make['popsicle'])
        else:
            print("You can't make that right now.")
        return

    def move_player(self, player_command):
        if player_command in self.commands_up:
            if self.player_pos[1] != 0:
                self.player_pos[1] -= 1
            return True
        if player_command in self.commands_down:
            if self.player_pos[1] != (self.map_size[1] - 1):
                self.player_pos[1] += 1
            return True
        if player_command in self.commands_left:
            if self.player_pos[0] != 0:
                self.player_pos[0] -= 1
            return True
        if player_command in self.commands_right:
            if self.player_pos[0] != (self.map_size[0] - 1):
                self.player_pos[0] += 1
            return True

    def print_time(self):
        with open('sun_positions.txt') as f:
            contents = f.read()
            start_read = (12 - math.ceil(self.time_until_sunset)) * 136
            print(contents[start_read:start_read + 136])
            f.close()
        print(str(self.days_left) + " days left.\n")

    def get_move(self):
        while 1 == 1:
            print("Enter command")
            player_command = input("> ")
            if any(cmd in player_command for cmd in self.valid_commands):
                if not player_command.isspace() and not player_command == "":
                    if player_command == "help":
                        print(", ".join(self.valid_commands))
                        continue
                    self.prev_player = self.player_pos
                    if self.move_player(player_command):
                        self.time_until_sunset -= 0.20
                    else:
                        self.other_command(player_command)
                        input("press enter to continue")
                    break

            else:
                print("That is not a valid command. Use 'help' to see a list "
                      + "of valid commands.")
                continue

    def game_loop(self):
        self.clear_screen_and_line()
        self.print_time()
        self.map_display = self.generate_map(self.map_display)
        self.print_map()
        self.get_move()
        if not self.get_curr_tile == 'Y' and self.time_until_sunset < 0.1:
            print("Your mother calls out: Where are you!? Oh no! You'll be " +
                  "grounded at least until Mother's Day!\n\n---Game Over---")
            sys.exit()


# game loop
game = Game_engine()
os.system('cls' if os.name == 'nt' else 'clear')
sys.stdout.write('\033[K')
sys.stdout.flush()
input("Welcome to Bird Adventure! You are a small bird, and Mother's Day is " +
      "coming soon. You have 2 weeks to find a gift for your Mom, and you have"
      + " to be back at sunset each day or she'll realize you were gone! " +
      "\n---Press enter to start---")
while 1 == 1:
    game.game_loop()


"""✅bird wants gift for mom
✅bird makes flower crown out of stick, leaf, flower
✅flower crown wilts before bird gets home
✅bird searches for a potion to stop wilting
✅bird can go to island, cave, river, or summit.
✅island: volcano helps you turn stick into torch. Turtle lost baby turtle.
✅find it and you get gem 2
cave: torch to go in, 3 gemstones needed to unlock door inside
✅summit: get snow
✅river: It's hot in may and the frog wants a popsicle. give popsicle, frog saw
✅baby turtle go downstream and get stuck in between rocks. frog is not strong
✅enough to help...
✅otter: give rock for gem 1"""
