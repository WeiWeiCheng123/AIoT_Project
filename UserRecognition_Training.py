import argparse
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms
from tqdm import tqdm

from utils.data_loading import UserDataset
from model import Net

img_dir = 'image'
model_path = './user_recognition.pth'


def training(net, device, epoch, batch_size, learning_rate, transform):
    dataset = UserDataset(img_dir, transform)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
    model = net.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    record_loss = []
    record_acc = []
    for epoch in range(epoch):
        model.train()
        running_loss = []
        running_acc = []
        for batch in tqdm(dataloader):
            data, label = batch
            label = label.to(device)
            data = data.to(device)
            output = model(data)
            loss = criterion(output, label)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            acc = (output.argmax(dim=-1) == label).float().mean()
            running_loss.append(loss.item())
            running_acc.append(acc.item())
        res_loss = sum(running_loss)/len(running_loss)
        res_acc = sum(running_acc)/len(running_acc)
        print('epoch', epoch+1, '/', args.epoch, 'loss: ', res_loss,
              ' acc: ', res_acc)
        record_loss.append(res_loss)
        record_acc.append(res_acc)
    torch.save(model.state_dict(), model_path)
    plt.plot(record_loss, label='loss')
    plt.plot(record_acc, label='acc')
    plt.legend(loc='best', fontsize=20)
    plt.xlabel('Epoch')
    plt.ylabel('Loss / Accuracy')
    plt.savefig('record.png')


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch_size', type=int, default=8)
    parser.add_argument('--epoch', type=int, default=40)
    parser.add_argument('--lr', type=float, default=0.001)

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    transform = transforms.Compose([
        transforms.Resize((512, 512)),
        transforms.ToTensor()])

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print('use', device)

    training(Net(), device, args.epoch, args.batch_size, args.lr, transform)
