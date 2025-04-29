import pytorch_lightning as L
import torchvision
import torchmetrics
import torch
import wandb
import numpy as np

class Model ( L.LightningModule):
    def __init__(self, lr):
        super().__init__()
        self.save_hyperparameters()
        self.model = torchvision.models.densenet121(weights=torchvision.models.DenseNet121_Weights.IMAGENET1K_V1)
        self.model.classifier = torch.nn.Linear(self.model.classifier.in_features,10)
        self.lr = lr


        self.train_accuracy = torchmetrics.Accuracy(task='multiclass', num_classes=10)
        self.val_accuracy = torchmetrics.Accuracy(task='multiclass', num_classes=10)
        self.test_accuracy = torchmetrics.Accuracy(task='multiclass', num_classes=10)


        self.val_precision = torchmetrics.Precision(task='multiclass', num_classes=10)
        self.test_precision = torchmetrics.Precision(task='multiclass', num_classes=10)

        self.val_recall = torchmetrics.Recall(task='multiclass', num_classes=10)
        self.test_recall = torchmetrics.Recall(task='multiclass', num_classes=10)

        self.val_f1 = torchmetrics.F1Score(task='multiclass', num_classes=10)
        self.test_f1 = torchmetrics.F1Score(task='multiclass', num_classes=10)

    


        # loss function
        self.criterion = torch.nn.CrossEntropyLoss()

        self.valPred = []
        self.valTrue = []

    def forward(self, x):
        return self.model(x)



    def shared_step(self, batch,stage:str, batch_idx):
        image,label = batch
        pred = self(image)
        label = label.long()

        loss = self.criterion(pred, label)
        probs = torch.softmax(pred, dim=1)

        if stage == "train":
            self.train_accuracy(pred, label.int())
            self.log("train/loss", loss, prog_bar=True,on_epoch = True, on_step=False)
            self.log("train/accuracy", self.train_accuracy, prog_bar=True,on_epoch = True, on_step=False)

        elif stage == "val":
            #mise a jour des metrics
            self.val_accuracy(pred, label.int())
            self.val_precision(pred, label.int())
            self.val_recall(pred, label.int())
            self.val_f1(pred, label.int())

            # log des metrics
            self.log("val/loss", loss, prog_bar=True,on_epoch = True, on_step=False)
            self.log("val/accuracy", self.val_accuracy, prog_bar=True,on_epoch = True, on_step=False)
            self.log("val/precision", self.val_precision, prog_bar=True,on_epoch = True, on_step=False)
            self.log("val/recall", self.val_recall, prog_bar=True,on_epoch = True, on_step=False)
            self.log("val/f1", self.val_f1, prog_bar=True,on_epoch = True, on_step=False)
            self.log("val/recall", self.val_recall, prog_bar=True,on_epoch = True, on_step=False)

            # save predictions and labels for confusion matrix
            self.valPred.append(torch.argmax(probs, dim=1).cpu())
            self.valTrue.append(label.cpu())

        elif stage == "test":
            #mise a jour des metrics
            self.test_accuracy(pred, label.int())
            self.test_precision(pred, label.int())
            self.test_recall(pred, label.int())
            self.test_f1(pred, label.int())

            # log des metrics
            self.log("test/loss", loss, prog_bar=True,on_epoch = True, on_step=False)
            self.log("test/accuracy", self.test_accuracy, prog_bar=True,on_epoch = True, on_step=False)
            self.log("test/precision", self.test_precision, prog_bar=True,on_epoch = True, on_step=False)
            self.log("test/recall", self.test_recall, prog_bar=True,on_epoch = True, on_step=False)
            self.log("test/f1", self.test_f1, prog_bar=True,on_epoch = True, on_step=False)
            self.log("test/recall", self.test_recall, prog_bar=True,on_epoch = True, on_step=False)
            # save predictions and labels for confusion matrix  
            #self.valPred.append((probs.cpu()>0.5).float())
            #self.valTrue.append(label.int().cpu())

        else: 
            raise NotImplementedError()

        return loss

    def training_step(self, batch, batch_idx):
        return self.shared_step(batch, "train", batch_idx)

    def validation_step(self, batch, batch_idx):
        return  self.shared_step(batch, "val", batch_idx)

    def test_step(self, batch, batch_idx):
        return self.shared_step(batch, "test", batch_idx)

    def on_validation_epoch_end(self):
            # get preds and labels
        preds = torch.cat(self.valPred).numpy().flatten().tolist()
        labels = torch.cat(self.valTrue).numpy().flatten().tolist()

        #print(preds.shape,labels.shape)
        if self.current_epoch % 10 == 0:
            wandb.log({f"conf_mat_{self.current_epoch}" : wandb.plot.confusion_matrix(preds=preds,
                            y_true=labels,
                            class_names=["Tomato_Healthy","Tomato_Bacterial_spot","Tomato_Early_blight","Tomato_late_bright","tomato_leaf_mold","Tomato_Septoria_leaf_spot","Tomato_Spider_mites","Tomato_Target_Spot","Tomato_Yellow_Leaf_Curl_Virus","Tomato_mosaic_virus"])})
        # clear
        self.valPred.clear()
        self.valTrue.clear()

    def on_validation_epoch_end(self):
            # get preds and labels
        preds = torch.cat(self.valPred).numpy().flatten().tolist()
        labels = torch.cat(self.valTrue).numpy().flatten().tolist()

        #print(preds.shape,labels.shape)
        if self.current_epoch:
            wandb.log({f"conf_mat_{self.current_epoch}" : wandb.plot.confusion_matrix(preds=preds,
                            y_true=labels,
                            class_names=["Tomato_Healthy","Tomato_Bacterial_spot","Tomato_Early_blight","Tomato_late_bright","tomato_leaf_mold","Tomato_Septoria_leaf_spot","Tomato_Spider_mites","Tomato_Target_Spot","Tomato_Yellow_Leaf_Curl_Virus","Tomato_mosaic_virus"])})
        # clear
        self.valPred.clear()
        self.valTrue.clear()

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(),lr=self.lr)
        return optimizer