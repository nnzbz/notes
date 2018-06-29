# React之高阶组件

[TOC]

## 1. 简介

### 1.1. 什么是高阶组件？

HOC(Higher-Order Components)

> 高阶组件就是返回组件的组件

### 1.2. 为什么要通过一个组件去返回另一个组件？

> 使用高阶组件可以在不修改原组件代码的情况下，修改原组件的行为或增强功能。

## 2. 实现方式

实现高阶组件分为两种方式

1. 属性代理(Props Proxy)
2. 反向继承(Inheritance Inversion)

### 2.1. 属性代理

#### 2.1.1. 简单实现

通过包裹原来的组件来操作props

```jsx
import React, { Component } from 'React';
//高阶组件定义
const HOC = (WrappedComponent) =>
  class WrapperComponent extends Component {
    render() {
      return <WrappedComponent {...this.props} />;
    }
}
//普通的组件
class WrappedComponent extends Component{
    render(){
        //....
    }
}

//高阶组件使用
export default HOC(WrappedComponent)
```

#### 2.1.2. 操作props

我们可以按照需要对传入的props进行增加、删除、修改

```jsx
const HOC = (WrappedComponent) =>
    class WrapperComponent extends Component {
        render() {
            const newProps = {
                name: 'HOC'
            }
            return <WrappedComponent
                {...this.props}
                {...newProps}
            />;
        }
    }
```

#### 2.1.3. 获得refs的引用

我们在属性代理中，可以轻松的拿到被包裹的组件的实例引用(ref)

```jsx
import React, { Component } from 'React';

const HOC = (WrappedComponent) =>
    class wrapperComponent extends Component {
        storeRef(ref) {
            this.ref = ref;
        }
        render() {
            return <WrappedComponent
                {...this.props}
                ref = {::this.storeRef}
            />;
        }
    }
```

#### 2.1.4. 抽象state

属性代理的情况下，我们可以将被包裹组件中的状态提到包裹组件中

```jsx
class WrappedComponent extends Component {
    render() {
        return <input name="name" {...this.props.name} />;
    }
}

const HOC = (WrappedComponent) =>
    class extends Component {
        constructor(props) {
            super(props);
            this.state = {
                name: '',
            };

            this.onNameChange = this.onNameChange.bind(this);
        }

        onNameChange(event) {
            this.setState({
                name: event.target.value,
            })
        }

        render() {
            const newProps = {
                name: {
                    value: this.state.name,
                    onChange: this.onNameChange,
                },
            }
            return <WrappedComponent {...this.props} {...newProps} />;
        }
    }
```

#### 2.1.5. 用其他元素包裹组件

直接看代码

```jsx
render(){
        <div>
            <WrappedComponent {...this.props} />
        </div>
    }
```

### 2.2. 反向继承

反向继承是指返回的组件去继承之前的组件

```jsx
const HOC = (WrappedComponent) =>
  class extends WrappedComponent {
    render() {
      return super.render();
    }
  }
```