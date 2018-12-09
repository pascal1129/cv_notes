## 0.0、参考资料

Docker中文文档：https://yeasy.gitbooks.io/docker_practice/

## 0.1、前期准备与测试程序

查看docker版本

    $ docker --version

新建 docker 用户组，并将自己的账号添加进docker组，以避免权限问题：

    $ sudo groupadd docker
    $ sudo usermod -aG docker pascal
退出当前终端并重新登录即可生效

尝试运行镜像，测试 Docker 是否安装正确，运行后自动删除容器：
​    $ docker run --rm hello-world

## 1、常见命令
列出镜像

    $ docker image ls
    $ docker image ls ubuntu 			# 根据仓库名列出镜像
    $ docker image ls ubuntu:18.04		# 指定仓库名和标签

删除镜像

    $ docker image rm
    $ docker image prune				# 删除虚悬镜像

镜像体积

    $ docker system df

列出容器

    $ docker container ls
    $ docker container ls -a			# 查看全部容器，包括终止状态

清除容器

    $ docker container rm  xxx			# 该容器处于终止状态
    $ docker container rm -f xxx		# 该容器处于运行状态，强制清除
    $ docker container prune			# 清除所有处于终止状态的容器

## 2、容器操作
除docker image/container ls/prune外，别的指令大多可以省略image/docker，多种写法是因为历史写法的一致性和可读性较差，后期指令的格式进行了升级

典型操作
实例化一个镜像，运行后终止，启动再进入，终止容器并删除容器

    $ docker pull ubuntu:18.04
    $ docker run -it  \
        ubuntu:18.04 \
        bash
    # exit or Ctrl+D
    $ docker start [容器]				
    
    $ docker container ls -a 可查阅容器ID
    
    $ docker exec -it [容器] bash
    $ docker stop [容器]
    $ docker rm  [容器]

获取镜像

    $ docker pull 仓库名[:标签]

实例化一个镜像

    $ docker run  [参数]  <镜像>
        -i 交互，让容器输入保持打开 
        -t 分配一个伪终端并绑定到容器的标准输入上
        -d 后台运行，结果不输出于宿主机，结果可用docker --rm 容器退出后删除，避免浪费空间
        logs [容器]查看


进入处于后台的容器
已终止的容器需要先启动：

    $ docker start	[容器]
    $ docker restart [容器]	# 终止并重启一个运行态的容器

后台运行的容器可直接进入：

    $ docker attach 243c				# exit后，容器会停止
    $ docker exec -it 69d1 bash	    	# exit后，容器不会停止，因此推荐使用；

终止容器

    （容器外）$ docker stop [容器]		
    （容器内）# exit or Ctrl+d



## 3、Docker数据管理
挂在主机目录：

    $ nvidia-docker run -it \
        --name ron \
        -v /home/pascal/data:/root:ro \
        detectron:c2-cuda9-cudnn7 \
        bash
    
    -v 宿主机目录：docker目录，如果目录不存在则创建
    --name 不可重名


## 4、管理维护
导出容器

    $ docker export [容器] > ubuntu.tar
导入容器

    $ cat ubuntu.tar | docker import - pascal1129/ubuntu:v1.0
    $ docker image ls
    REPOSITORY          TAG                 IMAGE ID            CREATED              VIRTUAL SIZE
    test/ubuntu         v1.0                9d37a6082e97        About a minute ago   171.3 MB

提交镜像
登陆docker账号

    $ docker login

新建一个容器，后台运行

    $ nvidia-docker run -dit \
        --name container_try \
        -v /home/pascal/data:/data \
        vistart/build_tensorflow:py36-cuda10.0-cudnn7-tensorrt5-devel-ubuntu18.04 \
        bash

进入容器，按需改动

    $ nvidia-docker exec -it container_try bash

提交容器为镜像

    $ docker commit \
        --author "pascal1129" \
        --message "test" \
        container_try \
        pascal1129/dl:conda_py36-cuda10.0-cudnn7-ubuntu18.04

查看历史记录

    $ docker history pascal1129/dl:conda_py36-cuda10.0-cudnn7-ubuntu18.04
推送镜像到云端

    $ docker push pascal1129/dl:conda_py36-cuda10.0-cudnn7-ubuntu18.04

保存别人的：

    $ docker tag someone/xxx:xxx pascal1129/xxx:xxx
    $ docker push pascal1129/xxx:xxx
    
    https://hub.docker.com/r/pascal1129/


## 其他
nvidia-docker安装:

[NVIDIA/nvidia-docker: Build and run Docker containers leveraging NVIDIA GPUs](https://github.com/nvidia/nvidia-docker#ubuntu-140416041804-debian-jessiestretch)