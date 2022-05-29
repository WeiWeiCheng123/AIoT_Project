import cv2
from PIL import Image
from pynput.keyboard import Controller
from time import sleep
import torch
from torchvision import transforms
import serial
from model import Net

model_path = './user_recognition.pth'

keyboard = Controller()

COM_PORT = 'COM9'
BAUD_RATES = 9600
s = serial.Serial(COM_PORT, BAUD_RATES)

transform = transforms.Compose([
    transforms.Resize((512, 512)),
    transforms.ToTensor()])

model = Net()
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval()

User = {}
User[0] = ['a1', 'b3']
User[1] = ['a2', 'b1']
User[2] = ['a3', 'b2']


def image_loader(x):
    img = transform(x).float()
    res = img.unsqueeze(0)
    return res


if __name__ == '__main__':
    try:
        while True:
            wake = False
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            while True:
                ret, frame = cap.read()
                cv2.imshow('frame', frame)
                key = cv2.waitKey(1)
                while s.in_waiting:
                    data = s.readline().rstrip().decode()
                    if data == 'wake':
                        wake = True                        
                if wake:
                    keyboard.press('a')
                if key == ord('a'):
                    print('capture')
                    keyboard.release('a')
                    break
            cap.release()
            cv2.destroyAllWindows()
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            image = image_loader(img)
            outputs = model(image).argmax(dim=-1).item()
            print('user', outputs)
            print(User[outputs])
            if outputs == 0:
                s.write(b'0\n')
                sleep(0.5)
            if outputs == 1:
                s.write(b'1\n')
                sleep(0.5)
            if outputs == 2:
                s.write(b'2\n')
                sleep(0.5)
            while s.in_waiting:
                data = s.readline().decode()
                print('arduino = ', data)

    except KeyboardInterrupt:
        s.close()
