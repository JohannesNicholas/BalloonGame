"""
Created by Joey Nicholas (joeyn.dev)
for Junior Engineers tutor application
24/9/2022


Requirements:
Develop a shooting game using Python. You can use any development environment that
you like. The goal is to shoot the balloon down. The player can move the cannon up and
down using the arrow keys, to fire a bullet the player will press the space key.

● The Balloon should move up and down randomly.
● The player can shoot one bullet at a time or multiple bullets at a time. DONE
● The game ends when the balloon is shot down, please show the number of missed
shots.
● The bullet speed should be 10 times the speed of the balloon.
● If you have to use pyGame, then make it obvious which version you
are using. DONE, I used tkinter
● Do not submit anything other than a single py file and the assets
you need to use. 
● Do not submit it in anything other than a zip file, no .rar etc.
● Do not submit it using Jupyter or any other fancy way of distributing
software.
● If I can’t download it in one go and need to install anything else,
then I will not look at it.
● If you don’t use relative paths for assets and I have to download and
move the assets around to make it work then I will not look at it.
● Do not plagiarize a copy from the internet, and if you do at least go
to the effort of modifying it significantly.
● File name convention: FirstName_LastName_balloon.py, that way I
always know which one is yours.
● You can make it as fancy as you like, but it has to work.
"""

#import required modules
import tkinter as tk #using tkinter for GUI as it is built into python while pygame is not
import random #for randomising balloon movement
import time #for time.sleep() function, used to create 60fps

#set up the window
window = tk.Tk() #create the window
window.title("Joey Nicholas's Balloon Shooter") #set window title
window.geometry("800x600") #set window size
window.resizable(False, False) #disable resizing of window

#set up the canvas
canvas = tk.Canvas(window, width=800, height=600, bg="white") #create the canvas
canvas.pack() #pack the canvas into the window

#set up the cannon
cannon = canvas.create_rectangle(50, 275, 75, 325, fill="black") #create the cannon
cannon_speed = 0 #set the cannon speed to 0

#set up the balloon
balloon = canvas.create_oval(700, 275, 725, 325, fill="red") #create the balloon
balloon_speed = 3
balloon_direction = 1 
balloon_change_counter = 0 #create a countdown for how many frames the balloon should move in the same direction

#set up the bullet
bullets = [] #create a list to store the bullets
bullet_speeds = [] #create a list to store the bullet speeds


#set up the score
missed = 0 #set the missed to 0, this is the number of missed shots
missed_text = canvas.create_text(400, 50, text="Missed: " + str(missed), font=("Arial", 20)) #create the score text

gameOver = False #true when the balloon is popped


#function when button is pressed
def key_down(event):
    #if the key pressed is up arrow
    if event.keysym == "Up":
        #move the cannon up
        global cannon_speed
        cannon_speed = -5

    #if the key pressed is down arrow
    if event.keysym == "Down":
        #move the cannon down
        cannon_speed = 5

    #if the key pressed is space
    if event.keysym == "space":
        #get the position of the cannon
        cannon_pos = canvas.coords(cannon)[1] + 25
        #create a bullet at the end of the cannon
        bullets.append(canvas.create_rectangle(75, cannon_pos, 100, cannon_pos + 5, fill="black")) #create the bullet
        #set the bullet speed
        bullet_speeds.append(10 * balloon_speed)



#function when button is released
def key_up(event):
    #if the key released is up arrow
    if event.keysym == "Up":
        #stop moving the cannon up
        global cannon_speed
        cannon_speed = 0

    #if the key released is down arrow
    if event.keysym == "Down":
        #stop moving the cannon down
        cannon_speed = 0




#bind the functions to the window
window.bind("<KeyPress>", key_down) 
window.bind("<KeyRelease>", key_up) 


#update function that is called 60 times a second
def update():

    #don't update if the game is over
    if gameOver:
        return

    global missed
    global balloon_change_counter
    global balloon_direction


    bullets_to_remove = [] #create a list to store the bullets to remove

    #move the bullets
    for i in range(len(bullets)):
        canvas.move(bullets[i], bullet_speeds[i], 0)

        #if the bullet is off the screen
        if canvas.coords(bullets[i])[0] > 800:
            #add the bullet to the list of bullets to remove
            bullets_to_remove.append(i)

        #if the bullet is touching the balloon
        if canvas.coords(bullets[i])[0] > 700 and \
            canvas.coords(bullets[i])[0] < 725 and \
            canvas.coords(bullets[i])[1] > canvas.coords(balloon)[1] and \
            canvas.coords(bullets[i])[3] < canvas.coords(balloon)[3]:

            #end the game
            end_game()

        
    
    #remove the bullets
    for i in bullets_to_remove:
        canvas.delete(bullets[i])
        del bullets[i]
        del bullet_speeds[i]
        missed += 1 #add 1 to the missed score

        #update the missed score
        canvas.itemconfig(missed_text, text="Missed: " + str(missed)) #update the score text







    #decrement the balloon change counter
    balloon_change_counter -= 1
    #if the balloon change counter is less than 0
    if balloon_change_counter < 0:
        #reset the balloon change counter to a random number between 60 and 120
        balloon_change_counter = random.randint(60, 120)
        #change the balloon direction
        balloon_direction *= -1

    #if the balloon is at the top of the screen
    if canvas.coords(balloon)[1] <= 0:
        #set the balloon direction to down
        balloon_direction = 1
    #if the balloon is at the bottom of the screen
    if canvas.coords(balloon)[3] >= 600:
        #set the balloon direction to up
        balloon_direction = -1

    #move the balloon
    canvas.move(balloon, 0, balloon_speed * balloon_direction)


    #move the cannon
    canvas.move(cannon, 0, cannon_speed) #move the cannon
    
    #clamp the cannon to the screen
    if canvas.coords(cannon)[1] < 0: #if the cannon is off the top of the screen
        canvas.move(cannon, 0, -canvas.coords(cannon)[1]) #move the cannon back to the top of the screen
    if canvas.coords(cannon)[3] > 600: #if the cannon is off the bottom of the screen
        canvas.move(cannon, 0, 600 - canvas.coords(cannon)[3]) #move the cannon back to the bottom of the screen
    


    #Update the visuals
    canvas.update()
    
    window.after(16, update) #schedule the next update

#called when the balloon is popped
def end_game():
    global gameOver
    gameOver = True
    #create the end game text
    canvas.create_text(400, 300, text="Game Over", font=("Arial", 50))

    #thank the user for playing
    canvas.create_text(400, 350, text="Thank you for playing", font=("Arial", 20))

    #credit the author
    canvas.create_text(400, 400, text="By: Joey Nicholas - joeyn.dev", font=("Arial", 11))

#start the update function
update()

#tkinter mainloop
window.mainloop()
