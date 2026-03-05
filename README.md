# Agro Tomato — Tomato Leaf Disease Classification

## Aim of the project

**Agro Tomato** aims to build a deep learning system that can **recognize tomato leaf diseases from images**.

Given a photo of a tomato leaf, the model predicts whether the leaf is healthy or affected by a specific disease. The goal is to support:
- **early detection** of diseases in tomato crops,
- faster and more consistent **field monitoring**,
- a reproducible pipeline for **training and evaluation**.

Dataset source: Kaggle — `kaustubhb999/tomatoleaf`.

> Note: the repo is named `agro_tomato`, but the current project/package name in `pyproject.toml` and Weights & Biases logging is `agro_niger`. You can rename later if you want everything consistent.

---

## Classes (model outputs)

### Recommended normalized labels (for documentation + code)

- `Tomato_Healthy`
- `Tomato_Bacterial_spot`
- `Tomato_Early_blight`
- `Tomato_Late_blight`
- `Tomato_Leaf_mold`
- `Tomato_Septoria_leaf_spot`
- `Tomato_Spider_mites`
- `Tomato_Target_spot`
- `Tomato_Yellow_leaf_curl_virus`
- `Tomato_Mosaic_virus`

### Mapping from your original labels

| Original label | Recommended normalized label |
|---|---|
| `Tomato_Healthy` | `Tomato_Healthy` |
| `Tomato_Bacterial_spot` | `Tomato_Bacterial_spot` |
| `Tomato_Early_blight` | `Tomato_Early_blight` |
| `Tomato_late_bright` | `Tomato_Late_blight` |
| `tomato_leaf_mold` | `Tomato_Leaf_mold` |
| `Tomato_Septoria_leaf_spot` | `Tomato_Septoria_leaf_spot` |
| `Tomato_Spider_mites` | `Tomato_Spider_mites` |
| `Tomato_Target_Spot` | `Tomato_Target_spot` |
| `Tomato_Yellow_Leaf_Curl_Virus` | `Tomato_Yellow_leaf_curl_virus` |
| `Tomato_mosaic_virus` | `Tomato_Mosaic_virus` |

---

## Dataset (Kaggle)

This project is trained on the Kaggle dataset:

- Kaggle page: `kaustubhb999/tomatoleaf`

### Download (Kaggle API)

1) Install Kaggle CLI:
```bash
pip install kaggle
```

2) Configure Kaggle credentials:
- Download `kaggle.json` from your Kaggle account (API token)
- Place it here:
  - Linux/macOS: `~/.kaggle/kaggle.json`
  - Windows: `%USERPROFILE%\.kaggle\kaggle.json`

3) Download + unzip into `data/raw`:
```bash
kaggle datasets download -d kaustubhb999/tomatoleaf -p data/raw --unzip
```

### Expected data layout (recommended)

After download/unzip, organize data in a folder-per-class format, e.g.:

```
data/
  raw/
    tomatoleaf/
      Tomato_Healthy/
      Tomato_Bacterial_spot/
      Tomato_Early_blight/
      Tomato_Late_blight/
      Tomato_Leaf_mold/
      Tomato_Septoria_leaf_spot/
      Tomato_Spider_mites/
      Tomato_Target_spot/
      Tomato_Yellow_leaf_curl_virus/
      Tomato_Mosaic_virus/
```

> Your training code currently imports dataset/data module from a hard-coded path (see Training section).  
> If needed, update the path(s) to point to `data/raw/...` on your machine.

---

## Model

- Architecture: **DenseNet-121** (ImageNet pretrained)
- Classifier: updated to output **10 classes**
- Framework: **PyTorch Lightning**
- Metrics: accuracy, precision, recall, F1
- Experiment tracking: Weights & Biases (W&B)

Model implementation:
- `models/model.py`

---

## Setup

### Requirements
- Python 3.10.x (see `pyproject.toml`)

Install dependencies:
```bash
pip install -r requirements.txt
pip install -e .
```

If you use W&B logging:
```bash
wandb login
```

---

## Training

Training is launched via:

```bash
python models/runner.py
```

What it does (current behavior):
- trains on GPU (`accelerator='gpu'`) for up to 50 epochs
- logs metrics to W&B
- saves the best checkpoint to:
  - `models/ckpt/`

> ⚠️ Note about paths:  
> `models/runner.py` currently uses:
> `sys.path.append("/teamspace/studios/this_studio/agro_niger/data")`  
> You may need to edit this so it works on your local machine.

---

## Export / Save weights

To save model weights to a `.pth` file:

```bash
python models/test.py
```

It saves:
- `agro_model.pth` (PyTorch `state_dict`)

A copy is already in the repo:
- `models/agro_model.pth`

---

## Author

- Mamane Argi Malam Bawa
