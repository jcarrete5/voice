#from pynput.mouse import Button, Controller
import pynput.mouse as ms
import time
import tkinter as tk



mouse = ms.Controller()

root=tk.Tk()

def newCoordiantes():
    Screen_Width= root.winfo_screenwidth()
    Screen_Height=root.winfo_screenheight()

    x= 1690/1920 *Screen_Width
    y=100/1080*Screen_Height
    newCoordiantes = (x, y)
    return newCoordiantes

def open():


    coordinates= mouse.position
    x= coordinates[0]
    y= coordinates[1]
    presentButtonCoordinates= newCoordiantes()

    xMovement= presentButtonCoordinates[0]-x
    yMovement=presentButtonCoordinates[1]-y
    mouse.move(xMovement,yMovement)

    mouse.click(ms.Button.left, 1)

if __name__ == '__main__':
    time.sleep(5)
    open()

