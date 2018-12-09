## 参考资料
安装教程：
https://github.com/facebookresearch/Detectron/blob/master/INSTALL.md

快速开始：
https://github.com/facebookresearch/Detectron/blob/master/GETTING_STARTED.md

## Docker安装Detectron
1、下载Detectron源代码

    $ git clone https://github.com/facebookresearch/Detectron.git

2、编译镜像

    $ cd DETECTRON/docker
    $ docker build -t detectron:c2-cuda9-cudnn7 .

查看镜像是否成功生成

    pascal@490-pc-2:~$ docker image ls
    REPOSITORY                 TAG                                                       IMAGE ID            CREATED             SIZE
    detectron                  c2-cuda9-cudnn7                                           0131f1c609d3        30 hours ago        4.14GB


3、试运行镜像，运行测试代码后自动删除

    $ nvidia-docker run --rm -it detectron:c2-cuda9-cudnn7 python detectron/tests/test_batch_permutation_op.py

4、进入容器，并挂载宿主机数据

    $ nvidia-docker run -dit \
        --name pascal_ron \
        -v /home/pascal/data:/data \
        detectron:c2-cuda9-cudnn7 \
        bash

5、以后进入容器

    $ nvidia-docker exec -it pascal_ron bash

Caffe2安装测试（Caffe2是否安装成功、打印GPU可用个数、运行测试代码）：

    python -c 'from caffe2.python import core' 2>/dev/null && echo "Success" || echo "Failure"
    python -c 'from caffe2.python import workspace; print(workspace.NumCudaDevices())'
    python /detectron/detectron/tests/test_batch_permutation_op.py


## 必要组件的安装
1、安装vim

    sudo apt-get update
    sudo apt-get install vim

2、更换Ubuntu软件源

备份原有的源列表

    cd /etc/apt
    cp sources.list sources.list.backup
更换源列表

    vim /etc/apt/sources.list

在文件开头添加阿里源，具体参见 [Ubuntu 18.04换国内源](https://blog.csdn.net/xiangxianghehe/article/details/80112149)，亲测清华源不可用

    deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
    deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
    deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
    deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
    deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
    deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
    deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
    deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
    deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
    deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse

更改后更新

    sudo apt-get update

3、安装COCO API

    sudo apt-get install python-tk
    
    cd /cocoapi/PythonAPI
    make
    python setup.py install


>安装测试：

    python -c 'from pycocotools.coco import COCO' 2>/dev/null && echo "Success" || echo "Failure"

## 提交做好的镜像到Docker Hub
1、提交镜像到Docker Hub

    $ docker commit \
        --author "pascal1129" \
        --message "detectron with vim, pycocotools, aliyun" \
        pascal_ron \
        pascal1129/detectron:caffe2_cuda9_aliyun
        
    $ docker push pascal1129/detectron:caffe2_cuda9_aliyun

2、以后在其他环境使用

    $ docker pull pascal1129/detectron:caffe2_cuda9_aliyun
    $ nvidia-docker run -dit \
        --name pascal_ron \
        -v /home/pascal/data:/data \
        pascal1129/detectron:caffe2_cuda9_aliyun \
        bash
    $ nvidia-docker exec -it pascal_ron bash

3、可以在~/.bashrc指定快捷命令

    alias ron='nvidia-docker exec -it pascal_ron bash'

4、将detectron代码下载到到宿主data文件夹，便于借助WinSCP查看代码

    ~/data$ git clone https://github.com/facebookresearch/Detectron.git
    ~/data$ mv Detectron/ detectron
    cd detectron
    make
    make ops

## 使用预训练模型测试
测试命令： [Inference with Pretrained Models](https://github.com/facebookresearch/Detectron/blob/master/GETTING_STARTED.md#inference-with-pretrained-models)

该部分解说：[使用Detectron进行目标检测 - 知乎](https://zhuanlan.zhihu.com/p/34036460)

使用tools目录下内置的infer_simple.py 来使用预训练的模型来预测实际的照片，infer_simple.py里面调用的是detectron封装的vis_utils.vis_one_image API

    python tools/infer_simple.py \
        --cfg configs/12_2017_baselines/e2e_mask_rcnn_R-101-FPN_2x.yaml \
        --output-dir /tmp/detectron-visualizations \
        --image-ext jpg \
        --wts https://s3-us-west-2.amazonaws.com/detectron/35861858/12_2017_baselines/e2e_mask_rcnn_R-101-FPN_2x.yaml.02_32_51.SgT4y1cO/output/train/coco_2014_train:coco_2014_valminusminival/generalized_rcnn/model_final.pkl \
        demo

1. --cfg 用来指定配置文件
2. --output-dir 指定生成结果存储的路径
3. --image-ext jpg 规定寻找jpg后缀的文件；
4. --wts 默认根据地址下载预训练模型存储在本地的/tmp目录下，也可以给定已经下载好的预训练模型的地址直接调用；
5. demo 检测当前demo目录里jpg后缀的图片；


    python tools/infer_simple.py \
        --cfg configs/12_2017_baselines/e2e_mask_rcnn_R-101-FPN_2x.yaml \
        --output-dir ../tmp/detectron-visualizations \
        --image-ext jpg \
        --wts ../tmp/model_final.pkl \
        demo

这里的程序主要是检测demo/*.jpg，我修改了输出路径，便于查看，由于预训练模型也下载很艰难，我提前下载了。