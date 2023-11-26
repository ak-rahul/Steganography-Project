import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox 
from tkinter.font import Font
import os
import cv2
from PIL import Image, ImageTk
import numpy as np
import math


bgColor = "#3d6466"
buttonColor = "#28293a"

files = {}

def showImage1():
    global fileName
    fileName = filedialog.askopenfilename(initialdir=os.getcwd,
                                          title = "Select Image File: ",
                                          filetype=(("PNG file",".png"),
                                                    ("JPG file",".jpg"),
                                                    ("All file",".txt")))
    img = Image.open(fileName)
    img = ImageTk.PhotoImage(img.resize((300,300)))
    imgWidget = tk.Label(imageFrame,
                         image=img,
                         bg=bgColor,
                         width=300,
                         height=300)
    imgWidget.image = img
    imgWidget.place(x=245,y=60)
        
def inputWidgets1():
    pwdLabel = tk.Label(inputFrame,
                        text="Enter password: ",
                        font=("Times New Roman",15),
                        bg=bgColor,
                        fg="white")
    pwdLabel.place(x=30,y=400)
    pwdInput = tk.Entry(inputFrame,
                        width=30,
                        fg="black",
                        bg="white")
    pwdInput.place(x=180,y=405)
    textLabel = tk.Label(inputFrame,
                         text="Enter text to hide: ",
                         font=("Times New Roman",15),
                         bg=bgColor,
                         fg="white")
    textLabel.place(x=30,y=440)
    textInput = tk.Text(inputFrame,
                         width=40,
                         height=2,
                         fg="black",
                         bg="white",
                         wrap="word")
    textInput.place(x=180,y=445)
    submitButton = tk.Button(inputFrame,
                             text="Submit",
                             bd=3,
                             bg=buttonColor,
                             fg="white",
                             cursor="hand2",
                             activebackground="#badee2",
                             activeforeground="grey",
                             font=("Times New Roman",15),
                             width=10,
                             pady=0,
                             command=lambda:hideText(fileName,textInput.get(1.0, "end-1c"),pwdInput.get(),[pwdLabel,pwdInput,textInput,textLabel,textInput,submitButton]))
    submitButton.place(x=170,y=490)
    
def hideText(fileName,msg,pwd,labels):
    global files
    data = msg
    img = cv2.imread(fileName)
    data = [format(ord(i), '08b') for i in data]
    _, width, _ = img.shape
    # algorithm to encode the image
    PixReq = len(data) * 3
    RowReq = PixReq/width
    RowReq = math.ceil(RowReq)
    count = 0
    charCount = 0
    # Step 3
    for i in range(RowReq + 1):
        # Step 4
        while(count < width and charCount < len(data)):
            char = data[charCount]
            charCount += 1
            # Step 5
            for index_k, k in enumerate(char):
                if((k == '1' and img[i][count][index_k % 3] % 2 == 0) or (k == '0' and img[i][count][index_k % 3] % 2 == 1)):
                    img[i][count][index_k % 3] -= 1
                if(index_k % 3 == 2):
                    count += 1
                if(index_k == 7):
                    if(charCount*3 < PixReq and img[i][count][2] % 2 == 1):
                        img[i][count][2] -= 1
                    if(charCount*3 >= PixReq and img[i][count][2] % 2 == 0):
                        img[i][count][2] -= 1
                    count += 1
        count = 0
    newFile = "encryptedImage"+str(len(files)+1)+".png"
    files[newFile] = [fileName,pwd,len(msg)]
    cv2.imwrite(newFile,img)
    messagebox.showinfo("Encryption", "Encryption Successfull")
    for i in labels:
        i.place(x=30,y=1000)
        

def showImage2():
    global fileName
    fileName = filedialog.askopenfilename(initialdir=os.getcwd,
                                          title = "Select Image File: ",
                                          filetype=(("PNG file",".png"),
                                                    ("JPG file",".jpg"),
                                                    ("All file",".txt")))
    if fileName.split("/")[-1] not in files:
        messagebox.showerror("Error", "File not encrypted..")
    else:
        img = Image.open(fileName)
        img = ImageTk.PhotoImage(img.resize((300,300)))
        imgWidget = tk.Label(imageFrame,
                            image=img,
                            bg=bgColor,
                            width=300,
                            height=300)
        imgWidget.image = img
        imgWidget.place(x=245,y=60)
        inputWidgets2()


def inputWidgets2():
    pwdLabel = tk.Label(inputFrame,
                        text="Enter password: ",
                        font=("Times New Roman",15),
                        bg=bgColor,
                        fg="white")
    pwdLabel.place(x=30,y=400)
    pwdInput = tk.Entry(inputFrame,
                        width=30,
                        fg="black",
                        bg="white")
    pwdInput.place(x=180,y=405)
    submitButton = tk.Button(inputFrame,
                             text="Submit",
                             bd=3,
                             bg=buttonColor,
                             fg="white",
                             cursor="hand2",
                             activebackground="#badee2",
                             activeforeground="grey",
                             font=("Times New Roman",15),
                             width=10,
                             pady=0,
                             command=lambda:extractText(fileName,pwdInput.get(),[pwdLabel,pwdInput,submitButton]))
    submitButton.place(x=170,y=475)
    
def extractText(fileName,pwd,labels):
    if files[fileName.split("/")[-1]][1] != pwd:
        messagebox.showerror("Error", "Incorrect password...")
    else:
        img = cv2.imread(fileName.split("/")[-1])
        data = []
        stop = False
        for index_i, i in enumerate(img):
            i.tolist()
            for index_j, j in enumerate(i):
                if((index_j) % 3 == 2):
                    # first pixel
                    data.append(bin(j[0])[-1])
                    # second pixel
                    data.append(bin(j[1])[-1])
                    # third pixel
                    if(bin(j[2])[-1] == '1'):
                        stop = True
                        break
                else:
                    # first pixel
                    data.append(bin(j[0])[-1])
                    # second pixel
                    data.append(bin(j[1])[-1])
                    # third pixel
                    data.append(bin(j[2])[-1])
            if(stop):
                break

        message = []
        # join all the bits to form letters (ASCII Representation)
        for i in range(int((len(data)+1)/8)):
            message.append(data[i*8:(i*8+8)])
        # join all the letters to form the message.
        message = [chr(int(''.join(i), 2)) for i in message]
        message = ''.join(message) 
        messagebox.showinfo("Decryption", "The message is: " + message)   
    for i in labels:
        i.place(x=30,y=1000)     
        
def encryption():
    showImage1()
    inputWidgets1()
    
def decryption():
    showImage2()
    

root = tk.Tk()
root.title("Steganography")
width = 600 # Width 
height = 600 # Height
screen_width = root.winfo_screenwidth()  # Width of the screen
screen_height = root.winfo_screenheight() # Height of the screen
 
# Calculate Starting X and Y coordinates for Window
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
 
root.geometry('%dx%d+%d+%d' % (width, height, x, y))
root["bg"] = bgColor
root.resizable(False,False)

headingFont = Font(family = "Times New Roman", 
                   size = 30,
                   weight = "bold")

header = tk.Label(root,
                  text = "Steganography",
                  bg = bgColor,
                  fg = "white",
                  font = headingFont,
                  justify = "center").place(x=160,y=0)

encryptButton = tk.Button(root,
                          text="Encrypt",
                          bg=buttonColor,
                          fg="white",
                          cursor="hand2",
                          activebackground="#badee2",
                          activeforeground="grey",
                          width=15,
                          font=("Times New Roman",15),
                          command= lambda:encryption(),
                          relief="groove").place(x=20,y=80)

decryptButton = tk.Button(root,
                          text="Decrypt",
                          bg=buttonColor,
                          fg="white",
                          cursor="hand2",
                          activebackground="#badee2",
                          activeforeground="grey",
                          width=15,
                          font=("Times New Roman",15),
                          command=lambda:decryption(),
                          relief="groove").place(x=20,y=120)

imageFrame = tk.Frame(root,
                      bg=bgColor,
                      width=350,
                      height=303,
                      bd=3,
                      relief="groove").place(x=220,y=60)

inputFrame = tk.Frame(root,
                      bg=bgColor, 
                      height=150,
                      width=560,
                      relief="groove",
                      bd=4).place(x=20,y=390)
root.mainloop()
