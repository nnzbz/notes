# vue 路由跳转方式

[TOC]

## 1. 标签跳转 router-link

- 不传参

```html
<li >
  <router-link to="user">点击验证动画效果 </router-link>
</li>
```

- 跳转时传参

```js
// 先要配置路由
path: '/user/:id'

<router-link :to="'/user/' + this.id"> <router-link/>

// 接收参数
this.$route.params.id
```

## 2. 事件跳转 this.$router.push()

描述：跳转到不同的url，但这个方法会向history栈添加一个记录，点击后退会返回到上一个页面。
用法：

- 字符串

```js
this.$router.push('/home')
```

- 对象

```js
this.$router.push({path:'/home'})
```

- query 传参，相当于get请求，页面跳转时参数会在地址栏中显示，通过this.$route.query.id获取

```js
// 变成 /user?id=2
this.$router.push({
    path:'/user',
    query:{
        id:this.id
    }
})
```

- params 传参，相当于post请求，页面跳转时参数不会在地址栏中显示,通过this.$route.params.id获取

```js
this.$router.push({
    path:'/user',
    params:{
        id:this.id
    }
})
```

注：传参是 router，接收参数是 route

## 3. this.$router.replace{path:'/user'}

描述：同样是跳转到指定的url，但是这个方法不会向history里面添加新的记录，点击返回，会跳转到上上一个页面。上一个记录是不存在的。

## 4. this.$router.go(n)

描述：相对于当前页面向前或向后跳转多少个页面,类似 window.history.go(n)。n可为正数可为负数。正数返回上一个页面。

```js
// 在浏览器记录中前进1步，相当于history.forward()
this.$router.go(1)

// 后退一步记录，等同于history.back()
this.$router.go(-1)

// 前进三步记录
this.$router.go(3)

// 如果history记录不够用，就会失败
this.$router.go(100)
this.$router.go(-100)
```

## 5. this.router.forward() 前进一步

## 6. this.router.back() 回退一步
