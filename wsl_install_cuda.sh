#!/bin/bash
# wsl_install_cuda.sh
# DISTRO变量是NVIDIA CUDA资源库名称的一部分，被设置为你所使用的发行版名称；
# 我们将使用 "wsl-ubuntu "来表示WSL上的CUDA。 APT_INSTALL变量指定了要安装的软件包的名称；
# 你可以从wsl-ubuntu资源库中安装cuda软件包来获得最新版本的CUDA工具包。
export DISTRO=wsl-ubuntu
export APT_INSTALL=cuda
# export DISTRO=ubuntu2004
# export APT_INSTALL=cuda-toolkit-11-4

# 在apt-key中添加CUDA
sudo apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/${DISTRO}/x86_64/7fa2af80.pub
echo "deb http://developer.download.nvidia.com/compute/cuda/repos/${DISTRO}/x86_64 /" | sudo tee /etc/apt/sources.list.d/cuda.list
wget https://developer.download.nvidia.com/compute/cuda/repos/${DISTRO}/x86_64/cuda-${DISTRO}.pin
sudo mv cuda-${DISTRO}.pin /etc/apt/preferences.d/cuda-repository-pin-600

# 安装CUDA Toolkit
sudo apt update && sudo apt -y upgrade
sudo apt install -y ${APT_INSTALL}
# sudo proxychains4 apt update && sudo apt -y upgrade
# sudo proxychains4 apt install -y ${APT_INSTALL}

# 设置环境变量
cat << 'EOS' >> ~/.profile

#Added by install-cuda-on-wsl.sh
#Ref: https://astherier.com/blog/2021/07/windows11-cuda-on-wsl2-setup/
export PATH=/usr/local/cuda-11.4/bin${PATH:+:${PATH}}
#Added: end

EOS

# 安装第三方库（可选）
sudo apt install -y g++ freeglut3-dev build-essential libx11-dev libxmu-dev libxi-dev libglu1-mesa libglu1-mesa-dev

# build建立一些样本程序来检查CUDA工具包的运行情况
# 存放在/usr/local/cuda/samples/下
cd /usr/local/cuda/samples/1_Utilities/deviceQuery/
sudo make
cd /usr/local/cuda/samples/1_Utilities/bandwidthTest/
sudo make
cd /usr/local/cuda/samples/7_CUDALibraries/simpleCUBLAS/
sudo make
cd /usr/local/cuda/samples/7_CUDALibraries/simpleCUFFT/
sudo make

cd /usr/local/cuda/samples/bin/x86_64/linux/release/

echo "

你已经完成了在WSL上配置CUDA的工作。
请检查它们是否正常工作，例如：
$ cd /usr/local/cuda/samples/bin/x86_64/linux/release/
$ ./deviceQuery

"