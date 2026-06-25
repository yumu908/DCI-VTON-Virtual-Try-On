# DCI-VTON-Virtual-Try-On

This is the official repository for the following paper:

> **Taming the Power of Diffusion Models for High-Quality Virtual Try-On with Appearance Flow** [[arxiv]](https://arxiv.org/pdf/2308.06101.pdf)
>
> Junhong Gou, Siyu Sun, Jianfu Zhang, Jianlou Si, Chen Qian, Liqing Zhang
> Accepted by **ACM MM 2023**.

## News

- *2023-12-06* We have updated the selection strategy of inpainting mask similar to VITON-HD and HR-VTON in `cp_dataset_v2.py`. The pretrained model based
  on this new masking strategy is available from [Google Drive](https://drive.google.com/drive/folders/11BJo59iXVu2_NknKMbN0jKtFV06HTn5K?usp=sharing).

## Overview

![](assets/teaser.jpg)

> **Abstract:**
> Virtual try-on is a critical image synthesis task that aims to transfer clothes from one image to another while preserving the details of both humans and clothes.
> While many existing methods rely on Generative Adversarial Networks (GANs) to achieve this, flaws can still occur, particularly at high resolutions.
> Recently, the diffusion model has emerged as a promising alternative for generating high-quality images in various applications.
> However, simply using clothes as a condition for guiding the diffusion model to inpaint is insufficient to maintain the details of the clothes.
> To overcome this challenge, we propose an exemplar-based inpainting approach that leverages a warping module to guide the diffusion model's generation effectively.
> The warping module performs initial processing on the clothes, which helps to preserve the local details of the clothes.
> We then combine the warped clothes with clothes-agnostic person image and add noise as the input of diffusion model.
> Additionally, the warped clothes is used as local conditions for each denoising process to ensure that the resulting output retains as much detail as possible.
> Our approach effectively utilizes the power of the diffusion model, and the incorporation of the warping module helps to produce high-quality and realistic virtual try-on results.
> Experimental results on VITON-HD demonstrate the effectiveness and superiority of our method.

## Getting Started

### Installation

#### Diffusion Model

1. Clone the repository

```shell
git clone https://github.com/bcmi/DCI-VTON-Virtual-Try-On.git
cd DCI-VTON-Virtual-Try-On
```

1. Install Python dependencies

```shell
conda env create -f environment.yaml
conda activate dci-vton
```

1. Download the pretrained [vgg](https://drive.google.com/file/d/1rvow8jStPt8t2prDcSRlnf8yzXhrYeGo/view?usp=sharing) checkpoint and put it in `models/vgg/`

#### Warping Module

1. Clone the PF-AFN repository

```shell
git clone https://github.com/geyuying/PF-AFN.git
```

1. Move the code to the corresponding directory

```shell
cp -r DCI-VTON-Virtual-Try-On/warp/train/* PF-AFN/PF-AFN_train/
cp -r DCI-VTON-Virtual-Try-On/warp/test/* PF-AFN/PF-AFN_test/
```

### Data Preparation

#### VITON-HD

1. Download [VITON-HD](https://github.com/shadow2496/VITON-HD) dataset
2. Download pre-warped cloth image/mask from [Google Drive](https://drive.google.com/drive/folders/15cBiA0AoSCLSkg3ueNFWSw4IU3TdfXbO?usp=sharing) or [Baidu Cloud](https://pan.baidu.com/s/1ss8e_Fp3ZHd6Cn2JjIy-YQ?pwd=x2k9) and put it under your VITON-HD dataset

After these, the folder structure should look like this (the unpaired-cloth* only included in test directory):

```
├── VITON-HD
|   ├── test_pairs.txt
|   ├── train_pairs.txt
│   ├── [train | test]
|   |   ├── image
│   │   │   ├── [000006_00.jpg | 000008_00.jpg | ...]
│   │   ├── cloth
│   │   │   ├── [000006_00.jpg | 000008_00.jpg | ...]
│   │   ├── cloth-mask
│   │   │   ├── [000006_00.jpg | 000008_00.jpg | ...]
│   │   ├── cloth-warp
│   │   │   ├── [000006_00.jpg | 000008_00.jpg | ...]
│   │   ├── cloth-warp-mask
│   │   │   ├── [000006_00.jpg | 000008_00.jpg | ...]
│   │   ├── unpaired-cloth-warp
│   │   │   ├── [000006_00.jpg | 000008_00.jpg | ...]
│   │   ├── unpaired-cloth-warp-mask
│   │   │   ├── [000006_00.jpg | 000008_00.jpg | ...]
```

### Inference

#### VITON-HD

Please download the pretrained model from [Google Drive](https://drive.google.com/drive/folders/11BJo59iXVu2_NknKMbN0jKtFV06HTn5K?usp=sharing) or [Baidu Cloud](https://pan.baidu.com/s/13Rp_-Fbp1NUN41q0U6S4gw?pwd=6bfg).

###### Warping Module

To test the warping module, first move the `warp_viton.pth` to `checkpoints` directory:

```shell
mv warp_viton.pth PF-AFN/PF-AFN_test/checkpoints
```

Then run the following command:

```shell
cd PF-AFN/PF-AFN_test
sh test_VITON.sh
```

After inference, you can put the results in the VITON-HD for inference and training of the diffusion model.

###### Diffusion Model

To quickly test our diffusion model, run the following command:

```shell
python test.py --plms --gpu_id 0 \
--ddim_steps 100 \
--outdir results/viton \
--config configs/viton512.yaml \
--ckpt /CHECKPOINT_PATH/viton512.ckpt \
--dataroot /DATASET_PATH/ \
--n_samples 8 \
--seed 23 \
--scale 1 \
--H 512 \
--W 512 \
--unpaired
```

or just simply run:

```shell
sh test.sh
```

### Training

#### Warping Module

To train the warping module, just run following commands:

```shell
cd PF-AFN/PF-AFN_train/
sh train_VITON.sh
```

#### Diffusion Model

We utilize the pretrained Paint-by-Example as initialization, please download the pretrained models from [Google Drive](https://drive.google.com/file/d/15QzaTWsvZonJcXsNv-ilMRCYaQLhzR_i/view) and save the model to directory `checkpoints`.

To train a new model on VITON-HD, you should first modify the dataroot of VITON-HD dataset in `configs/viton512.yaml` and then use `main.py` for training. For example,

```shell
python -u main.py \
--logdir models/dci-vton \
--pretrained_model checkpoints/model.ckpt \
--base configs/viton512.yaml \
--scale_lr False
```

or simply run:

```shell
sh train.sh
```

## Acknowledgements

Our code is heavily borrowed from [Paint-by-Example](https://github.com/Fantasy-Studio/Paint-by-Example). We also thank [PF-AFN](https://github.com/geyuying/PF-AFN), our warping module depends on it.

## Citation

```
@inproceedings{gou2023taming,
  title={Taming the Power of Diffusion Models for High-Quality Virtual Try-On with Appearance Flow},
  author={Gou, Junhong and Sun, Siyu and Zhang, Jianfu and Si, Jianlou and Qian, Chen and Zhang, Liqing},
  booktitle={Proceedings of the 31st ACM International Conference on Multimedia},
  year={2023}
}



```

## 第一步：把图片放进对应的文件夹

首先，把要测试的图片放入 D:\projects\VITON-HD\test 目录下对应的文件夹中：

模特人物图片：放入 D:\projects\VITON-HD\test\image\ 文件夹中（例如 my_person.jpg）。
要试穿的衣服图片：放入 D:\projects\VITON-HD\test\cloth\ 文件夹中（例如 my_cloth.jpg）。
💡 注意：如果是您自己全新的图片，通常还需要生成对应的辅助文件（如衣服的 Mask 放入 cloth-mask 等）。如果您只是在数据集自带的 2000 多张图片里自由组合，则不需要这一步，可以直接看第二步。

## 第二步：在 test_pairs.txt 里配置配对关系

打开配对关系配置文件 D:\projects\VITON-HD\test_pairs.txt：

每一行就是一组试穿配置。格式为：[人物图片文件名] [衣服图片文件名]（中间用空格隔开）。
例如：如果您想让 05006_00.jpg 这个模特穿上 14096_00.jpg 这件衣服，就在 test_pairs.txt 里添加或修改一行：
text
05006_00.jpg 14096_00.jpg
运行推理命令时，程序会自动读取该文件中的每一行，并依次执行试穿。

## 第三步：配置推理命令（参数说明）

在运行命令时，我们可以通过修改命令行里的参数来做进一步的配置：

powershell
.\dci-vton\python.exe test.py `
--plms `
  --gpu_id 0 `
--ddim_steps 30 `
  --outdir results/viton `
--config configs/viton512.yaml `
  --dataroot D:/projects/VITON-HD `
--ckpt checkpoints/viton512_v2.ckpt `
  --n_samples 1 `
--H 512 --W 512 `
  --unpaired
--dataroot：数据集的根路径。如果您把图片移到了其他硬盘，可以修改此处的路径。
--ddim_steps：生成步数，默认是 30。数值越高图片细节越精细，但速度会变慢（您可以设为 30 ~ 100 之间的任意值）。
--unpaired：试穿模式。
加上该参数：程序会读取 test_pairs.txt 里您配对指定的不同衣服进行试穿。
不加该参数：程序会默认让模特穿她原本自己身上那件相同的衣服（一般用于做配对重建测试）。

## 一键试穿自定义配对（Windows 批处理 - 推荐）

为了简化流程，我们已将整个过程（包括第一阶段变形、第二阶段推理、以及自动对比图生成）打包为一个批处理脚本。

### 运行方式
在项目根目录下打开命令行，直接运行：
```shell
.\run_tryon.bat [模特人像文件名] [要试穿的衣服文件名]
```

### 运行示例
```shell
.\run_tryon.bat 01409_00.jpg 00008_00.jpg
```
脚本会自动处理：
1. 配置配对，写入 `test_pairs.txt`；
2. 运行第一阶段 Warping 变形对齐，并自动复制变形后的衣服和 Mask 到数据集；
3. 运行第二阶段 Diffusion 试穿渲染；
4. 自动调用 `make_comparison.py` 生成对比图。

### 查看结果
* **最终试穿图**：`results/viton/result/[人物名].png`
* **三宫格对比图**：`results/viton/comparisons/comparison_[人物ID].png`

---

## 拼接对比图生成器 (`make_comparison.py`)

可以通过该脚本一键把模特图、衣服图和试穿结果图拼成一张三宫格图。

### 怎么运行生成命令？
在命令行运行以下命令：

* **为特定单组生成对比图**：
  ```shell
  .\dci-vton\python.exe make_comparison.py --person 01409_00.jpg --cloth 00008_00.jpg
  ```

* **一键为所有配置好的默认对生成对比图**：
  ```shell
  .\dci-vton\python.exe make_comparison.py
  ```

生成好的图片会保存在 `results/viton/comparisons/` 目录下。
