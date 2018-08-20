# 调用 dll

[TOC]

## 1. hello项目

### 1.1. 安装 ```node-gyp```

```sh
sudo npm install -g node-gyp
```

### 1.2. 创建C语言文件

```c
// hello.cc
#include <node.h>

namespace demo {

using v8::FunctionCallbackInfo;
using v8::Isolate;
using v8::Local;
using v8::Object;
using v8::String;
using v8::Value;

void Method(const FunctionCallbackInfo<Value>& args) {
  Isolate* isolate = args.GetIsolate();
  args.GetReturnValue().Set(String::NewFromUtf8(isolate, "world"));
}

void init(Local<Object> exports) {
  NODE_SET_METHOD(exports, "hello", Method);
}

NODE_MODULE(addon, init)

}  // namespace demo
```

### 1.3. 创建 ```binding.gyp``` 文件

```json
{
  "targets": [
    {
      "target_name": "addon",
      "sources": [ "hello.cc" ]
    }
  ]
}
```

### 1.4. 生成构建文件

```sh
node-gyp configure
```

### 1.5. 编译

```sh
node-gyp build
```

编译生成 ```addon.node``` 文件。

### 1.6. 在 nodejs 中调用

```js
// hello.js
const addon = require('./build/Release/addon');

console.log(addon.hello()); // 'world'
```