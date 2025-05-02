# Conoha 接続設定

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
