import socket
import cv2
import pickle
import struct
import imutils
from tkinter import *
import _thread

import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 9000
server_addr = ("", port)
server_socket.bind(server_addr)
server_socket.listen(2)
sockets = []


def recv_msg(sock, iswaiting, isended):
    if not iswaiting and not isended:
        iswaiting = True
        while iswaiting:
            data = sock.recv(1024).decode()

            if data == "q":
                iswaiting = False
                isended = True
                print("프로그램이 종료되었습니다.")
                break
            send_msg(sock, data)
            print("클라이언트로부터 받은 메세지", data)


def send_msg(sock, addr):
    print(sock)
    print(addr)
    msg = input("서버, 보내는 메세지:")
    sock.sendto(msg.encode(), addr)
    print("보낸 메세지:", msg)


def send_video(client_socket, addr):
    _thread.start_new_thread(send_msg, (client_socket, addr))
    if client_socket:
        sockets.append({"socket": client_socket, "iswaiting": False, "isended": False})
        for socket_info in sockets:
            if not socket_info["iswaiting"] and not socket_info["isended"]:
                _thread.start_new_thread(
                    recv_msg,
                    (
                        socket_info["socket"],
                        socket_info["iswaiting"],
                        socket_info["isended"],
                    ),
                )
        vid = cv2.VideoCapture(0)
        if vid.isOpened():
            print(vid.get(3), vid.get(4))
            while vid.isOpened():
                img, frame = vid.read()
                frame = imutils.resize(frame, width=640)
                frame_bytes = pickle.dumps(frame)
                msg = struct.pack("Q", len(frame_bytes)) + frame_bytes
                client_socket.sendall(msg)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
            client_socket, addr = server_socket.accept()


while True:
    client_socket, addr = server_socket.accept()
    print(addr, "와 연결됨")
    _thread.start_new_thread(send_video, (client_socket, addr))
    print("새로운 스레드 만들고 실행")
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
