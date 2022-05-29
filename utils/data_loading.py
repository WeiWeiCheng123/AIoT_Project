import os
from pathlib import Path
from typing import Dict, List, Tuple
from PIL import Image
from torch.utils.data import Dataset


def make_dataset(direction, class_to_idx) -> List[Tuple[str, int]]:
    instances = []
    for i in (class_to_idx.keys()):
        class_index = class_to_idx[i]
        target_dir = os.path.join(direction, i)
        for root, _, fnames in (os.walk(target_dir)):
            for fname in fnames:
                path = os.path.join(root, fname)
                item = str(path), class_index
                instances.append(item)
    return instances


def find_class(direction) -> Dict[str, int]:
    classes = Path(direction)
    class_to_idx = {}
    j = 0
    for name in os.listdir(classes):
        class_to_idx[name] = j
        j += 1
    return class_to_idx


class UserDataset(Dataset):
    def __init__(self, root, transform):
        self.transform = transform
        self.root = root
        class_to_idx = self.find_class(self.root)
        samples = self.make_dataset(self.root, class_to_idx)
        self.samples = samples

    def __getitem__(self, index):
        path, target = self.samples[index]
        img = Image.open(path)
        if self.transform is not None:
            img = self.transform(img)
        return img, target
 
    def __len__(self):
        return len(self.samples)
    
    def find_class(self, direction):
        return find_class(direction)

    def make_dataset(self, direction, class_to_idx):
        return make_dataset(direction, class_to_idx)
