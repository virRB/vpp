import os
import pyautogui
import time
import tkinter as tk
from tkinter import messagebox
#An example program
root = tk.Tk()
root.geometry('100x200+100+100')
#Creates a window named root with the above dimensions and coordinates
newLabel = tk.Label(root, text='Hi!')
newLabel.pack()
#Creates a text newLabel with the text "Hi!"
num = 1
#creates a number variable named num with a value of 1
txt = 'HelloWorld'
#Creates a text variable named txt with a value of HelloWorld (Note
def Hi():
    #Starts a function named Hi
    newLabel.config(text='HelloWorld')
    #Changes the text in our "newLabel" to HelloWorld
#end of function
#Ends the function
btn1 = tk.Button(root, text='ClickMe', command=Hi)
btn1.pack()
#Creates a button named btn1 with the text ClickMe, that calls our function "Hi" when clicked
def Bye():
    global num
    #Makes the variable num global so that this statement can edit its value
    if num == 1:
        #Checks if our variable num is equal to 1
        num += 1
        #Edits the value of our variable num to increase by 1
        messagebox.showinfo('Message', 'ThisIsAMessage')
        #Sends a fixed Message
        messagebox.showinfo('Message', str(txt))
        #Sends a message with the value of the variable txt
        pyautogui.moveTo(500, 500)
        #Should move your mouse to the coordinates x=500, y=500
        pyautogui.click(500, 500)
        #Should click in the same spot
#end if statement
    #Ends the if statements
#end of function
btn2 = tk.Button(root, text='ClickMeAsWell', command=Bye)
btn2.pack()
root.mainloop()
#If you are using a window make sure to put this at the end of your code