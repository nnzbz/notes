# Git使用代理

## 设置代理

```sh
# http
git config --global http.proxy http://127.0.0.1:1080
git config --global https.proxy https://127.0.0.1:1080
# socket
git config --global http.proxy 'socks5://127.0.0.1:1080'
git config --global https.proxy 'socks5://127.0.0.1:1080'
```

## 取消代理

```sh
git config --global --unset http.proxy
git config --global --unset https.proxy
```
