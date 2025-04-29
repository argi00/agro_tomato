import torch 
import pytorch_lightning as L
import wandb
import torchvision
import torchmetrics
from pytorch_lightning.loggers import WandbLogger
import sys
sys.path.append("/teamspace/studios/this_studio/agro_niger/data")
from data import DataModule
from RetrieveData import dataset
from model import Model
from pytorch_lightning.callbacks  import EarlyStopping,ModelCheckpoint

if __name__ == "__main__":
    # Créer une instance de DataModule
    data_module = DataModule(dataset=dataset, batch_size=64)
    model = Model(lr=0.001)

    early_stop_callback = EarlyStopping(monitor="val/f1", 
                                        min_delta=1e-4, 
                                        patience=10, 
                                        verbose=False, 
                                        mode="max")
    wandb_logger = WandbLogger(project='agro_niger', name="densenet121_test", log_model=False)

    checkpoint_callback = ModelCheckpoint(
    save_top_k=1,
    monitor="val/f1",
    mode="max",
    dirpath="../models/ckpt",
    filename="sample-mnist-{epoch:02d}-{val/f1:.2f}",
    )

    callbacks = [early_stop_callback,checkpoint_callback]

    trainer = L.Trainer(max_epochs=50, 
                        max_steps=-1,
                        accelerator='gpu',
                        num_sanity_val_steps=2, 
                        logger=wandb_logger,
                        precision='16-mixed',
                        deterministic=False,
                        reload_dataloaders_every_n_epochs=3,
                        callbacks = callbacks
                        )

    #trainer.test(model, data_module,ckpt_path="/teamspace/studios/this_studio/agro_niger/models/ckpt/sample-mnist-epoch=08-val/f1=1.00.ckpt")
    torch.save(model.state_dict(), 'agro_model.pth')