# Conoha

## Conoha 接続設定

```bash
ssh-keygen -t ed25519 -f ~/.ssh/oshiben

scp ~/.ssh/oshiben.pub root@163.44.127.243:~/.ssh/authorized_keys_hinaito
```

```bash
ssh root@163.44.127.243

chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys*
```

```bash
cp /etc/ssh/sshd_config /etc/ssh/sshd_config_BK20250502

vi /etc/ssh/sshd_config


# AuthorizedKeysFileに半角スース区切りで複数指定可能
"""
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys_hinaito
"""

diff /etc/ssh/sshd_config /etc/ssh/sshd_config_BK20250502
"""
45c45
< PubkeyAuthentication yes
---
> #PubkeyAuthentication yes
49c49
< AuthorizedKeysFile	.ssh/authorized_keys_hinaito
---
> AuthorizedKeysFile	.ssh/authorized_keys
"""

sudo systemctl restart sshd
```

```bash
vi ~/.ssh/config

# 以下を追記する
"""
Host 163.44.127.243
    HostName 163.44.127.243
    User root
    IdentityFile ~/.ssh/oshiben
"""

# `ssh $wm_airflow` で接続できるように .zprofile などに設定追加
echo "export oshiben=root@163.44.127.243" >> ~/.zprofile
source ~/.zprofile

ssh $oshiben
```

## Conoha docker 構築

```bash
yum update

sudo yum install -y yum-utils device-mapper-persistent-data lvm2
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce docker-ce-cli containerd.io

systemctl start docker
systemctl enable docker

docker -v
# Docker version 27.3.1, build ce12230
```

```bash
sudo yum update
sudo yum install -y git

```

```bash
# passwordは不要
ssh-keygen -t ed25519 -f ~/.ssh/github

vi  ~/.ssh/config
"""
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/github
"""
```

公開鍵を Deploy Keys に追加

```bash
cat ~/.ssh/github.pub
```

init clone

```bash
cd

git clone git@github.com:7110/oshiben-be.git
```

## ssh 化

```bash
sudo yum install -y epel-release
sudo yum install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```
