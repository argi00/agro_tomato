import sys
from torch.utils.data import Dataset,DataLoader
import pytorch_lightning as L
from torchvision import transforms
import torch
# ajout du chemin d'acces du dossier data
sys.path.append("/teamspace/studios/this_studio/agro_niger/data")

# Recuperation de la variable contenant le dictionnaire de dataset
from RetrieveData import dataset


class CustomDataset(Dataset):
    def __init__(self, data,transform):
        self.data = data
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):

        image , label = self.data[idx]
        image =self.transform(image)
        return image, label

# lightning data module
class DataModule(L.LightningDataModule):
    def __init__(self, batch_size=64,
                 dataset = dataset ):
        super().__init__()
        self.dataset = dataset
        self.batch_size = batch_size
        self.dataset = dataset


        self.train_transform =  transforms.Compose ([
            transforms.ToTensor(), 
            transforms.Normalize(mean=[0.4495, 0.4651, 0.4002],std=[0.1656, 0.1448, 0.1832]),
            transforms.ConvertImageDtype(torch.float),
            transforms.Resize((224, 224)),
            transforms.RandomRotation(degrees=10)
        ])

        
        self.val_tranform =  transforms.Compose ([
            transforms.ToTensor(), 
            transforms.Normalize(mean=[0.4495, 0.4651, 0.4002],std=[0.1656, 0.1448, 0.1832]),
            transforms.ConvertImageDtype(torch.float),
            transforms.Resize((224, 224))
        ])

    def setup(self, stage=str):
        # Split the dataset into train and validation sets if needed

        if stage == "fit":
            train_data = dataset["train"]
            self.train_dataset = CustomDataset(train_data,self.train_transform) 
            val_data = dataset["val"]
            self.val_dataset = CustomDataset(val_data,self.val_tranform)

        if stage == "test":
            test_data = dataset["test"]
            self.test_dataset = CustomDataset(test_data,self.val_tranform)

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size)

    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size)






"""
if __name__ == "__main__":
    # Créer une instance de DataModule
    data_module = DataModule(dataset=dataset, batch_size=64)

    # Préparer les données
    data_module.setup(stage="fit")

    # Récupération des dataloaders
    train_loader = data_module.train_dataloader()

    it = iter(train_loader)
    first = next(it)
    image,label = first
    print(image)

"""