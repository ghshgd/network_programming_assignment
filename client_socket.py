import socket
import cv2
import pickle
import struct
import _thread


def client_socket_send_msg(client_socket, addr, msg):
    client_socket.sendto(msg.encode(), addr)
    print("클라이언트, 보낸 메세지:", msg)


def client_socket_recv_msg(client_socket):
    while True:
        data = client_socket.recv(1024).decode()
        print("클라이언트, 서버로부터 받은 메세지:", data)


def client_socket_start(client_socket, float_img, label):
    data = b""
    payload_size = struct.calcsize("Q")

    _thread.start_new_thread(client_socket_recv_msg, (client_socket,))
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(1024 * 4)
            if not packet:
                break
            else:
                data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            hi = client_socket.recv(4 * 1024)
            data += hi
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)
        frame = float_img(frame)
        label.config(image=frame)
        label.image = frame
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    client_socket.close()
