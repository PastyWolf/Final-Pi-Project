###########################################################################################
# Name: Matthew Tures
# Date:
# Description: Group project
###########################################################################################
from random import randint
from Tkinter import*
from pygame import*
import time
mixer.init()
###########################################################################################
# the blueprint for a room
class Room(object):
      # the constructor
      def __init__(self, name):
            # rooms have a name, an image(the name of a file), exits (e.g., south), exit locations (e.g., to the south is room n),
            # items (e.g., table), item descriptions (for each item), and grabbables (things that can
            # be taken into inventory)
            self.name = name
            self.image = image
            self.exits = {}
            self.items = {}
            self.characters = {}
            self.Characters = []
            self.grabbables = []

      # getters and setters for the instance variables
      @property
      def name(self):
            return self._name

      @name.setter
      def name(self, value):
            self._name = value

      @property
      def image(self):
                return self._image
      @image.setter
      def image(self, value):
              self._image = value

      @property
      def exits(self):
            return self._exits

      @exits.setter
      def exits(self, value):
            self._exits = value

      @property
      def characters(self):
            return self._characters

      @characters.setter
      def characters(self, value):
            self._characters = value

      @property
      def Characters(self):
            return self._Characters

      @Characters.setter
      def Characters(self, value):
            self._Characters = value


      @property
      def items(self):
            return self._items

      @items.setter
      def items(self, value):
            self._items = value

      @property
      def grabbables(self):
            return self._grabbables

      @grabbables.setter
      def grabbables(self, value):
            self._grabbables = value

      # adds an exit to the room
      # the exit is a string (e.g., north)
      # the room is an instance of a room
      def addExit(self, exit, room):
            # append the exit and room to the appropriate lists
            #dictionary
            self._exits[exit] = room

      def addChar(self, character):
            self._Characters.append(character)

      def delChar(self, character):
            self._Characters.remove(character)


      # adds an item to the room
      # the item is a string (e.g., table)
      # the desc is a string that describes the item (e.g., it is made of wood)
      def addItem(self, item, desc):
            # append the item and description to the appropriate lists
            # dictionary
            self._items[item] = desc


      # adds a grabbable item to the room
      # the item is a string (e.g., key)
      def addGrabbable(self, item):
            # append the item to the list
            self._grabbables.append(item)

      # removes a grabbable item from the room
      # the item is a string (e.g., key)
      def delGrabbable(self, item):
            # remove the item from the list
            self._grabbables.remove(item)

      # returns a string description of the room
      def __str__(self):
            # first, the room name
            s = "You are in {}.\n".format(self.name)

            # next, the items in the room
            s += "You see: "
            for item in self.items:
                  s += item + " "
            s += "\n"

            # next, the exits from the room
            s += "Exits: "
            for exit in self.exits:
                  s += exit + " "

            return s
###########################################################################################

global boss_hp
boss_hp = 90
global user_hp
user_hp = 20


#the game class
#inherits from the Frame class of Tkinter
class Game(Frame):
        # the constructor
        def __init__(self, parent):
                # call the constructor in the superclass
                Frame.__init__(self, parent)
                self.button1 = Button(parent, text = "ATTACK!", fg = "black", bg="green", command = self.attack)
                self.button1.pack(side = BOTTOM, fill=X)


        # sets up the GUI
        def setupGUI(self):
                # organize the GUI
                self.pack(fill=BOTH, expand=1)
                # setup the player input at the bottom of the GUI

                # create widget
                Game.player_input = Entry(self, bg="lightgrey")
                Game.player_input.bind("<Return>", self.process)
                Game.player_input.pack(side=TOP, fill=X)
                Game.player_input.focus()

                # setup the image to the left of the GUI
                # the widget is a Tkinter Label
                # don't let the image control the widget's size
                img = None
                Game.image = Label(self, width=WIDTH / 2, image=img)
                Game.image.image = img
                Game.image.pack(side=LEFT, fill=Y)
                Game.image.pack_propagate(False)

                # setup the text to the right of the GUI
                # first, the frame in which the text will be placed
                text_frame = Frame(self, width=WIDTH / 2)
                # the widget is a Tkinter Text
                # disable it by default
                # don't let the widget control the frame's size
                Game.text = Text(text_frame, bg="lightgrey", state=DISABLED)
                Game.text.pack(fill=Y, expand=1)
                text_frame.pack(side=RIGHT, fill=Y)
                text_frame.pack_propagate(False)



        def attack(self):
                Game.text.config(state = NORMAL)
                Game.text.delete("1.0", END)
                global x
                x = randint(0, 20)
                global boss_hp
                boss_hp -= x
                global y
                y = randint(0, 20)
                global user_hp
                user_hp -= y

                if (Game.currentRoom == r2):
                    Game.text.insert(END, "There is a boss in this room. It has 90 HP.")
                    if (user_hp > 0):
                        if (boss_hp > 0):
                            Game.text.insert(END, "The boss's HP went down to {}.\n".format(boss_hp))
                            Game.text.insert(END, "Your HP went down to {}.\n".format(user_hp))
                            if (x <= 5):
                                Game.text.insert(END, "You did {} damage to the enemy. What a piful luck.".format(x))
                            elif (x > 5 and x < 15):
                                Game.text.insert(END, "You did {} damage to the enemy. Hmm, medium damage.".format(x))
                            elif (x >= 15):
                                Game.text.insert(END, "You did {} damage to the enemy. Very Well, Now that's satisfying.".format(x))
                        else:
                            Game.text.insert(END, "You did {} damage.The boss's HP went down to 0.\n".format(x))
                            Game.text.insert(END, "The boss did {} damage. Your HP went down to {}.\n".format(y, user_hp))
                        Game.text.insert(END, "The boss did {} damage to you.\n".format(y))
                    if (user_hp <= 0):
                        # this DOES actually make the room change to death screen
                        Game.text.config(state = NORMAL)
                        Game.text.delete("1.0", END)
                        Game.currentRoom = None
                        self.setRoomImage()
                        Game.text.insert(END, " YOU DED!")
                        mixer.music.load('death.ogg')
                        mixer.music.play()
                else:
                    Game.text.insert(END, "Woah. Slow down stud, there's nothing to fight here.")


      # creates the rooms
        def createRooms(self):
                # r0 through r4 are the four settings in the game
                # currentRoom is the setting the player is currently in (which can be one of r0 through r4)
                # since it needs to be changed in the main part of the program, it must be global
                global currentRoom
                global menu
                global r0

                global r1
                global r2
                global r3
                global r4


                # create the rooms and give them meaningful names and an image in the ccurrent directory
                r0 = Room("Menu")
                r1 = Room("Forest")
                r2 = Room("Cave")
                r3 = Room("Ruins")
                r4 = Room("Cellar")


                r0.addExit("next", r1)
                r0.addChar("girl")
                r0.addChar("boy")
                r0.addChar("potato")

                # add exits to room 1
                r1.addExit("next", r2)

                # add grabbables to room 1
                r1.addGrabbable("key")
                # add items to room 1
                r1.addItem("chair", "It is made of wicker and no one is sitting on it.")
                r1.addItem("table", "It is made of oak.  A golden key rests on it.")

                # add exits to room 2
                r2.addExit("next", r3)
                # add items to room 2
                r2.addItem("rug", "It is nice and Indian.  It also needs to be vacuumed.")
                r2.addItem("fireplace", "It is full of ashes.")

                # add exits to room 3
                r3.addExit("next", r4)
                # add grabbables to room 3
                r3.addGrabbable("book")
                # add items to room 3
                r3.addItem("bookshelves", "They are empty.  Go figure.")
                r3.addItem("statue", "There is nothing special about it.")
                r3.addItem("desk", "The statue is resting on it.  So is a book.")

                # add exits to room 4
                r4.addExit("next", None) # DEATH!
                # add grabbables to room 4
                r4.addGrabbable("6-pack")
                # add items to room 4
                r4.addItem("brew_rig", "Gourd is brewing some sort of oatmeal stout on the brew rig.  A 6-pack is resting beside it.")



                # set room 1 as the current room at the beginning of the game
                Game.currentRoom = r0

                #intitialize the player's inventory
                Game.inventory= []
                Game.youare = []




        # set the current room image
        def setRoomImage(self):
                if (Game.currentRoom == None):
                      # if dead, set the wasted image
                      Game.img = PhotoImage(file="skull.gif")

                elif (Game.currentRoom == r0):
                      Game.img = PhotoImage(file="menu.gif")

                elif (Game.currentRoom == r1):
                      Game.img = PhotoImage(file="room1.gif")
                      if (Game.currentRoom == r1 and Game.youare[0] == "girl"):
                            Game.img = PhotoImage(file="room1withgirl.gif")
                      if (Game.currentRoom == r1 and Game.youare[0] == "boy"):
                            Game.img = PhotoImage(file="room1withman.gif")
                      if (Game.currentRoom == r1 and Game.youare[0] == "potato"):
                            Game.img = PhotoImage(file="room1withpotat.gif")

                elif (Game.currentRoom == r2):
                      Game.img = PhotoImage(file="room2.gif")
                      if (Game.currentRoom == r2 and Game.youare[0] == "girl"):
                            Game.img = PhotoImage(file="room2withgirl.gif")
                      if (Game.currentRoom == r2 and Game.youare[0] == "boy"):
                            Game.img = PhotoImage(file="room2withman.gif")
                      if (Game.currentRoom == r2 and Game.youare[0] == "potato"):
                            Game.img = PhotoImage(file="room2withpotat.gif")

                elif (Game.currentRoom == r3):
                      Game.img = PhotoImage(file="room3.gif")
                      if (Game.currentRoom == r3 and Game.youare[0] == "girl"):
                            Game.img = PhotoImage(file="room3withgirl.gif")
                      if (Game.currentRoom == r3 and Game.youare[0] == "boy"):
                            Game.img = PhotoImage(file="room3withman.gif")
                      if (Game.currentRoom == r3 and Game.youare[0] == "potato"):
                            Game.img = PhotoImage(file="room3withpotat.gif")

                elif (Game.currentRoom == r4):
                      Game.img = PhotoImage(file="room4.gif")
                      if (Game.currentRoom == r4 and Game.youare[0] == "girl"):
                            Game.img = PhotoImage(file="room4withgirl.gif")
                      if (Game.currentRoom == r4 and Game.youare[0] == "boy"):
                            Game.img = PhotoImage(file="room4withman.gif")
                      if (Game.currentRoom == r4 and Game.youare[0] == "potato"):
                            Game.img = PhotoImage(file="room4withpotat.gif")


                # display the image on the left of the GUI

                Game.image.config(image=Game.img)
                Game.image.image = Game.img

        # set the current room sound
        def setRoomSound(self):
              #if dead, play the death sound
              if (Game.currentRoom == None):
                    mixer.music.load('death.ogg')
                    mixer.music.play()

              elif (Game.currentRoom == r1):
                    mixer.music.load('forest.ogg')
                    mixer.music.play(-1)

              elif (Game.currentRoom == r2):
                    mixer.music.load('cave.ogg')
                    mixer.music.play(-1)

              elif (Game.currentRoom == r3):
                    mixer.music.load('ruins.ogg')
                    mixer.music.play(-1)

              elif (Game.currentRoom == r4):
                    mixer.music.load('moon.ogg')
                    mixer.music.play(-1)



        # sets the status displayed on the right of the GUI
        def setStatus(self, status):
                global boss_hp
                global x
                # enable the text widget, clear it, set it, and disabled it
                Game.text.config(state=NORMAL)
                Game.text.delete("1.0", END)
                if (Game.currentRoom == None):
                        # if dead, let the player know
                        Game.text.insert(END, "You are dead. The only thing you can do now is quit.\n")
                else:
                        # otherwise, display the appropriate status
                        Game.text.insert(END, str(Game.currentRoom) + "\nYou are carrying: " + str(Game.inventory) + "\n\n" + status)
                        if (boss_hp == 90 and Game.currentRoom == r2):
                              Game.text.insert(END, "There is a boss in this room and its health is 90.\n")

                        elif (boss_hp <= 0 and Game.currentRoom == r2):
                              Game.text.insert(END, "The boss now has 0 HP.\n")
                              Game.text.insert(END, "You may proceed to the next room.\n")

                        else:
                              Game.text.insert(END, "Look around. There might be clues.")

                Game.text.config(state=DISABLED)


        # play the game
        def play(self):
                # add the rooms to the game
                self.createRooms()
                # configure the GUI
                self.setupGUI()
                # set the current room
                self.setRoomImage()
                # set the current status
                self.setStatus("")


                #puts music on, the '-1' mean a loop.
                mixer.init()
                mixer.music.load('menu.ogg')
                mixer.music.play(-1)

        # processes the player's input
        def process(self, event):

                # grab the player's input from the input at the bottom of
                # the GUI
                action = Game.player_input.get()
                # set the user's input to lowercase to make it easier to
                # compare the verb and noun to known values
                action = action.lower()
                # set a default response
                response = "I don't understand. Try verb noun. Valid verbs are go, look, and take"

                # exit the game if the player wants to leave (supports quit, exit, and bye)
                if (action == "quit" or action == "exit" or action == "bye" or action == "sionara!"):
                        exit(0)

                # if the player is dead if goes/went south from room 4
                if (Game.currentRoom == None):
                        # clear the player's input
                        Game.player_input.delete(0, END)
                        return

                # split the user input into words (words are separated by spaces) and store the words in a list
                words = action.split()

                # the game only understands two word inputs
                if (len(words) == 2):
                        # isolate the verb and noun
                        verb = words[0]
                        noun = words[1]

                        # the verb is: go
                        if (verb == "go"):
                                # set a default response
                                response = "Invalid exit."

                                # check for valid exits in the current room
                                if (noun in Game.currentRoom.exits):
                                        # if one is found, change the current room to
                                        # the one that is associated with the
                                        # specified exit
                                        Game.currentRoom = Game.currentRoom.exits[noun]

                                        # set the response (success)
                                        response = "Room changed."

                        # the verb is: look
                        elif (verb == "look"):
                                # set a default response
                                response = "I don't see that item."

                                # check for valid items in the current room
                                if (noun in Game.currentRoom.items):
                                        # if one is found, set the response to the
                                        # item's description
                                        response = Game.currentRoom.items[noun]

                        elif (verb == "attack"):
                                # set a default response
                                response = "There is nothing to attack."

                                # check for valid targets in the current room
                                if (noun in Game.currentRoom.bosses):
                                        # if one is found, set the response to the
                                        # item's description
                                        damage=0
                                        #use randint here.
                                        response = "You did {} damage to the boss!".format(str(damage))

                        elif (verb == "select"):
                              #set default response
                              response = "You cannot select a character at this time."

                              for character in Game.currentRoom.Characters:
                                    # a valid character is found
                                    if (noun == character):
                                          if (character == "girl"):
                                                Game.youare.append("girl")
                                                Game.currentRoom.delChar("boy")
                                                Game.currentRoom.delChar("potato")
                                                response = "You are a girl."
                                          elif (character == "boy"):
                                                Game.youare.append("boy")
                                                Game.currentRoom.delChar("girl")
                                                Game.currentRoom.delChar("potato")
                                                response = "You are a boy."
                                          elif (character == "potato"):
                                                Game.youare.append("potato")
                                                Game.currentRoom.delChar("boy")
                                                Game.currentRoom.delChar("girl")
                                                response = "You are a potato."

                        # the verb is: take
                        elif (verb == "take"):
                              # set a default response
                              response = "I don't see that item."

                              # check for valid grabbable items in the current
                              # room
                              for grabbable in Game.currentRoom.grabbables:
                                    # a valid grabbable item is found
                                    if (noun == grabbable):
                                          # add the grabbable item to the player's inventory
                                          Game.inventory.append(grabbable)
                                          # remove the grabbable item from the room
                                          Game.currentRoom.delGrabbable(grabbable)
                                          # set the response (success)
                                          response = "Item grabbed."
                                          # no need to check any more grabbable items
                                          break
                # display the response on the right of the GUI
                # display the room's image on the left of the GUI
                # clear the player's input
                self.setStatus(response)
                self.setRoomImage()
                Game.player_input.delete(0, END)
                self.setRoomSound()







##########################################################
# the default size of the GUI is 800x600
WIDTH = 800
HEIGHT = 600
# create the window
window = Tk()
window.title("Room Adventure")
# create the GUI as a Tkinter canvas inside the window
g = Game(window)
# play the game
g.play()
# wait for the window to close
window.mainloop()
