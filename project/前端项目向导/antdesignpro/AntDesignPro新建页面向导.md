# AntDesignPro新建页面向导

[TOC]

## 1. 目录说明

- dist
 编译后的文件，每次将此目录部署至线上需要先将原来的dist目录删除；
- doc
 说明文档；
- mock
 模拟后台服务提供数据的代码；
- src
 前端源代码文件。
- src/routes
 放置页面文件
- src/components
 公用组件
- src/models
 与service层过渡层
- src/services
 向服务器发出各种请求的封装

## 2. 新建页面

以新建快递单管理页面为例说明如何构件一个页面:

1. 如果需要增加目录节点，首先在src/common/menu.js增加目录节点;

```js
const menuData = [
  ...
 {
    name: '快递管理',
    icon: 'profile',
    path: 'kdi',
    children: [
         {
        name: '快递单管理',
        path: 'kdi-mng',
      },
    ],
},
...
```

2. 在src/common/router.js增加路由配置，需要注意组件命名需要与数据库表名相一致，如快递物流单管理的组件名为kdilogistic；

```js
const routerConfig = {
  ...
'/kdi/kdi-mng': {
      component: dynamicWrapper(app, ['kdilogistic'], () => import('../routes/Kdi/KdiLogistic')),
    },
  ...
```

3. 在src/routes文件夹下新建一个 ```Kdi``` 的文件夹存放快递管理的页面，并在该文件夹下新建页面组件文件 ```KdiLogistic.js``` 以及其它需要导入的组件文件；

    3.1 页面文件中，render()是渲染页面的方法，return()方法则是将渲染出来的页面返回

4. 在```src/models```文件夹下新建一个快递的模型文件kdilogistic.js;

5. 在```src/serivces```文件夹下新建一个快递的服务层文件```kdilogistic.js```;

6. 在```.roadhogrc.mock.js```文件中增加快递请求的映射;

```js
import {
  kdilogisticList,
  kdilogisticGetById,
  kdilogisticAdd,
  kdilogisticModify,
  kdilogisticDel,
} from './mock/kdilogistic';
```

```js
const proxy = {
  ...
//kdilogitic
  'GET /kdi-svr/kdi/logistic': kdilogisticList,
  'GET /kdi-svr/kdi/logistic/getbyid': kdilogisticGetById,
  'POST /kdi-svr/kdi/logistic': kdilogisticAdd,
  'PUT /kdi-svr/kdi/logistic': kdilogisticModify,
  'DELETE /kdi-svr/kdi/logistic': kdilogisticDel,
  ...
```

7. 在mock文件夹下新建模拟服务器数据文件kdilogistic.js;

8. 最后在控制台进入项目文件夹用yarn start 命令启动项目后，就可以在浏览器看到我们新建的页面了。

## 3. 常见问题：

1. 项目启动时报no space left on the device错误

由于linux打开文件数量的限制，运行下面命令修改系统的打开文件数量限制：
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
