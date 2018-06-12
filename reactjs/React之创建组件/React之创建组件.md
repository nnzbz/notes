# React之创建组件

[TOC]

## 1. react创建组件的方式

- 函数式定义的无状态组件
- es5原生方式React.createClass定义的组件
- es6形式的extends React.Component定义的组件

### 1.1. 无状态函数式组件

无状态函数式组件形式上表现为一个只带有一个```render```方法的组件类，通过函数形式或者ES6 arrow function的形式在创建，并且该组件是无state状态的。具体的创建形式如下：

```jsx
function HelloComponent(props, /* context */) {
  return <div>Hello {props.name}</div>
}
ReactDOM.render(<HelloComponent name="Sebastian" />, mountNode)
```

特点：

- 组件不会被实例化，整体渲染性能得到提升
- 组件不能访问```this```对象
- 组件无法访问生命周期的方法
- 无状态组件只能访问输入的props，同样的props会得到同样的渲染结果，不会有副作用

> 只要有可能，尽量使用无状态组件

### 1.2. React.createClass

react刚开始推荐的创建组件的方式，这是ES5的原生的JavaScript来实现的React组件，其形式如下：

```jsx
var InputControlES5 = React.createClass({
    propTypes: {//定义传入props中的属性各种类型
        initialValue: React.PropTypes.string
    },
    defaultProps: { //组件默认的props对象
        initialValue: ''
    },
    // 设置 initial state
    getInitialState: function() {//组件相关的状态对象
        return {
            text: this.props.initialValue || 'placeholder'
        };
    },
    handleChange: function(event) {
        this.setState({ //this represents react component instance
            text: event.target.value
        });
    },
    render: function() {
        return (
            <div>
                Type something:
                <input onChange={this.handleChange} value={this.state.text} />
            </div>
        );
    }
});
InputControlES6.propTypes = {
    initialValue: React.PropTypes.string
};
InputControlES6.defaultProps = {
    initialValue: ''
};
```

问题：

- React.createClass会自绑定函数方法（不像React.Component只绑定需要关心的函数）导致不必要的性能开销，增加代码过时的可能性。
- React.createClass的mixins不够自然、直观；React.Component形式非常适合高阶组件（Higher Order Components--HOC）,它以更直观的形式展示了比mixins更强大的功能，并且HOC是纯净的JavaScript，不用担心他们会被废弃。HOC可以参考无状态组件(Stateless Component) 与高阶组件。

### 1.3. React.Component

```jsx
class InputControlES6 extends React.Component {
    constructor(props) {
        super(props);

        // 设置 initial state
        this.state = {
            text: props.initialValue || 'placeholder'
        };

        // ES6 类中函数必须手动绑定
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event) {
        this.setState({
            text: event.target.value
        });
    }

    render() {
        return (
            <div>
                Type something:
                <input onChange={this.handleChange}
               value={this.state.text} />
            </div>
        );
    }
}
InputControlES6.propTypes = {
    initialValue: React.PropTypes.string
};
InputControlES6.defaultProps = {
    initialValue: ''
};
```

## 2. React.createClass与React.Component区别

### 2.1. 函数this自绑定

React.createClass创建的组件，其每一个成员函数的this都有React自动绑定，任何时候使用，直接使用this.method即可，函数中的this会被正确设置。

```jsx
const Contacts = React.createClass({  
  handleClick() {
    console.log(this); // React Component instance
  },
  render() {
    return (
      <div onClick={this.handleClick}></div>
    );
  }
});
```

React.Component创建的组件，其成员函数不会自动绑定this，需要开发者手动绑定，否则this不能获取当前组件实例对象。

```jsx
class Contacts extends React.Component {  
  constructor(props) {
    super(props);
  }
  handleClick() {
    console.log(this); // null
  }
  render() {
    return (
      <div onClick={this.handleClick}></div>
    );
  }
```

当然，React.Component有三种手动绑定方法：可以在构造函数中完成绑定，也可以在调用时使用method.bind(this)来完成绑定，还可以使用arrow function来绑定。拿上例的handleClick函数来说，其绑定可以有：

```jsx
    constructor(props) {
       super(props);
       this.handleClick = this.handleClick.bind(this); //构造函数中绑定
  }
```

```jsx
    <div onClick={this.handleClick.bind(this)}></div> //使用bind来绑定
```

```jsx
    <div onClick={()=>this.handleClick()}></div> //使用arrow function来绑定
```

### 2.2. 组件属性类型propTypes及其默认props属性defaultProps配置不同

React.createClass在创建组件时，有关组件props的属性类型及组件默认的属性会作为组件实例的属性来配置，其中defaultProps是使用getDefaultProps的方法来获取默认组件属性的

```jsx
const TodoItem = React.createClass({
    propTypes: { // as an object
        name: React.PropTypes.string
    },
    getDefaultProps(){   // return a object
        return {
            name: ''    
        }
    }
    render(){
        return <div></div>
    }
})
```

React.Component在创建组件时配置这两个对应信息时，他们是作为组件类的属性，不是组件实例的属性，也就是所谓的类的静态属性来配置的。对应上面配置如下：

```jsx
class TodoItem extends React.Component {
    static propTypes = {//类的静态属性
        name: React.PropTypes.string
    };

    static defaultProps = {//类的静态属性
        name: ''
    };

    ...
}
```

### 2.3. 组件初始状态state的配置不同

React.createClass创建的组件，其状态state是通过getInitialState方法来配置组件相关的状态；
React.Component创建的组件，其状态state是在constructor中像初始化组件属性一样声明的。

```jsx
const TodoItem = React.createClass({
    // return an object
    getInitialState(){ 
        return {
            isEditing: false
        }
    }
    render(){
        return <div></div>
    }
})
class TodoItem extends React.Component{
    constructor(props){
        super(props);
        this.state = { // define this.state in constructor
            isEditing: false
        } 
    }
    render(){
        return <div></div>
    }
}
```

### 2.4. Mixins的支持不同

Mixins(混入)是面向对象编程OOP的一种实现，其作用是为了复用共有的代码，将共有的代码通过抽取为一个对象，然后通过Mixins进该对象来达到代码复用。具体可以参考React Mixin的前世今生。

React.createClass在创建组件时可以使用mixins属性，以数组的形式来混合类的集合。

```jsx
var SomeMixin = {  
  doSomething() {

  }
};
const Contacts = React.createClass({  
  mixins: [SomeMixin],
  handleClick() {
    this.doSomething(); // use mixin
  },
  render() {
    return (
      <div onClick={this.handleClick}></div>
    );
  }
});
```

但是遗憾的是React.Component这种形式并不支持Mixins，至今React团队还没有给出一个该形式下的官方解决方案；但是React开发者社区提供一个全新的方式来取代Mixins,那就是Higher-Order Components，具体细节可以参考这篇文章

## 3. 如何选择哪种方式创建组件

由于React团队已经声明React.createClass最终会被React.Component的类形式所取代。但是在找到Mixins替代方案之前是不会废弃掉React.createClass形式。所以：

- 能用React.Component创建的组件的就尽量不用React.createClass形式创建组件。
- 只要有可能，尽量使用无状态组件创建形式。
- 否则（如需要state、生命周期方法等），使用`React.Component`这种es6形式创建组件

补充一点

无状态组件内部其实是可以使用ref功能的，虽然不能通过this.refs访问到，但是可以通过将ref内容保存到无状态组件内部的一个本地变量中获取到。
例如下面这段代码可以使用ref来获取组件挂载到dom中后所指向的dom元素：

```jsx
function TestComp(props){
    let ref;
    return (<div>
        <div ref={(node) => ref = node}>
            ...
        </div>
    </div>)
}
```