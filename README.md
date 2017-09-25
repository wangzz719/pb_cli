# pb_cli

## 介绍
pb_cli 是一个用于生成python pb 文件进行打包发布的工具

目前不同项目之前对 proto 文件的使用通过文件复制的方式，这给 proto 文件的统一和版本管理带来不便

使用 pb_cli 可以将编译生成的 python 文件打包上传至 python 私服，其他需要使用的项目只需从私服上 pip install 对应的 python包 即可正常使用，而不必在重新编译 proto 文件

## 使用方法
### 配置本地 `~/.pypirc` 文件
```
[distutils]
index-servers =
    devpi

[devpi]
username = simple
password = 123
repository = http://10.46.182.130:3141/simple/pypi/

```
说明：
- index-servers 为源服务器配置，示例中源服务器命名为 devpi
- 配置源服务器的用户名，密码和仓库地址，注意仓库地址必须以 '/' 结尾

### 安装
#### 源码安装
1. 克隆代码到本地
2. 进入源码目录，执行 ```python setup.py install```

#### pip install 安装（pb_cli 已经上传到 10.46.182.130 私服）
直接 pip install 安装
```
pip install pb_cli --trusted-host 10.46.182.130 -i http://10.46.182.130:3141/simple/pypi/
```

### 使用
以 test_proto 为 proto 文件所在目录为例
进入 test_proto 目录创建 config.ini
#### 目录结构
```
- test_proto/
  - a.proto
  - b.proto
  - config.ini
```
#### 创建 config.ini

```
[config]
version = 0.1.1
package_name = test_proto
```
说明：
- version 为当前 proto 版本
- package_name 为要打包的 python 包名

#### 命令

```
pbcli -g -u
```
说明：
- -g: --generate，生成 proto python 文件和打包依赖文件
- -u: --upload，上传 python 包到 python 私服

### pip 安装源配置
可以通过配置 pip.conf 指定 pip 的安装源

pip.conf 位于`~/.pip/pip.conf`

配置示例：
```
[global]
timeout = 60
index-url = http://10.46.182.130:3141/simple/pypi/
extra-index-url = http://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host =
    10.46.182.130
    mirrors.aliyun.com
```
示例中配置了两个源，在安装时会首先从 10.46.182.130 查找，如果没有找到则从 mirrors.aliyun.com 查找