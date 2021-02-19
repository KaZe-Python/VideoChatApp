import cv2
import socket

class Client:
    def __init__(self) -> None:
        self.HOST = "localhost"
        self.PORT = 5555
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cap = cv2.VideoCapture(2)
        self.start()

    def start(self) -> None:
        while True:
            ret, frame = self.cap.read()
            mirrored = cv2.flip(frame,1)
            self.sock.connect((self.HOST, self.PORT))
            self.sock.sendall(mirrored)
            cv2.imshow('Cam', mirrored)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    client = Client()
    client()