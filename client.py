import client_socket as cs
from tkinter import *
from PIL import Image
from PIL import ImageTk
import _thread
import cv2
import socket


def changeLabel():
    img = make_img([])


def make_img(img_arr):  # path 경로의 이미지를 레이블에 출력
    # opencv 이미지
    img_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)
    src = cv2.resize(img_arr, (640, 400))
    # 넘파이 배열을 필로우 이미지 변환
    img = Image.fromarray(img_arr)  # 넘파이 배열을 이미지로 변환
    # tkinter에서 사용할 수 있는 이미지로 변환
    # self.src = 이미지
    floated = ImageTk.PhotoImage(image=img)
    return floated


root = Tk()
root.title("우리의 세계")
root.geometry("300x500+300+300")
root.resizable(True, True)

label = Label(root, text="나만의 세계")
label.grid(column=0, sticky=W)

msgLabel = Label(text="hi wrold\n")
msgLabel.grid(column=1, row=0)


def send_msg(event):
    global client_socket, host_ip, port
    cs.client_socket_send_msg(client_socket, (host_ip, port), entry.get())


entry = Entry(root, width=48)
entry.bind("<Return>", send_msg)
entry.grid(column=1, sticky=W)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = "localhost"
port = 9000
client_socket.connect((host_ip, port))
_thread.start_new_thread(cs.client_socket_start, (client_socket, make_img, label))

root.mainloop()
