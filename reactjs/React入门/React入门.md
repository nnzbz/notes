# React入门

[TOC]

## 1. HelloWorld

```jsx
<!DOCTYPE html>
<html>

<head>
    <title>HelloWorld</title>
    <meta charset="utf-8">
    <script src="js/reactjs/react.js"></script>
    <script src="js/reactjs/react-dom.js"></script>
    <script src="js/reactjs/browser.js"></script>
</head>

<body>
    <div id="example"></div>
    <script type="text/babel">
        ReactDOM.render(
        <h1>Hello, world!</h1>, document.getElementById('example') );
    </script>
</body>

</html>
```

> jsx

上面代码在body里面的```<script>```标签的 ```type``` 属性为 ```text/babel```，这里jsx的独有语法，与js不兼容。

> 引入的js库

|     js库     |              说明               |
| :----------- | ------------------------------- |
| react.js     | React 的核心库                  |
| react-dom.js | react-dom.js                    |
| Browser.js   | 将 jsx 语法转为 js 语法 |

## 2. ReactDOM.render()

ReactDOM.render 是 React 的最基本方法，用于将模板转为 HTML 语言，并插入指定的 DOM 节点。

## 3. jsx语法

### 3.1. html 与 js 的混写

HTML 语言直接写在 JavaScript 语言之中，不加任何引号

JSX 的基本语法规则：

- 遇到 HTML 标签（以 ```<``` 开头），就用 HTML 规则解析；
- 遇到代码块（以 ```{``` 开头)，就用 JavaScript 规则解析

```jsx
var names = ['Alice', 'Emily', 'Kate'];

ReactDOM.render(
    <div>
        {names.map((name, index) => {
            return <div key={'mykey' + index}>Hello, {name}!</div>
        })}
    </div>, document.getElementById('example')
);
```

### 3.2. 展开数组变量

```jsx
var arr = [
    <h1>Hello world!</h1>,
    <h2>React is awesome</h2>,
];
ReactDOM.render(
    <div>{arr}</div>,
    document.getElementById('example')
);
```

## 4. 组件示例

### 4.1. 简单示例

React 允许将代码封装成组件（component），然后像插入普通 HTML 标签一样，在网页中插入这个组件。

```jsx
var HelloMessage = React.createClass({
    render: function () {
        return <h1>Hello {this.props.name}</h1>;
    }
});

ReactDOM.render(
    <HelloMessage name="John" />,
    document.getElementById('example')
);
```

**HelloMessage** 就是一个组件类。模板插入 **\<HelloMessage />** 时，会自动生成 **HelloMessage** 的一个实例（下文的"组件"都指组件类的实例）。所有组件类都必须有自己的 **render** 方法，用于输出组件。

### 4.2. 容易出错的地方

- **组件类的第一个字母必须大写**，否则会报错，比如HelloMessage不能写成helloMessage。
- 另外，**组件类只能包含一个顶层标签**，否则也会报错(可以用 ```Fragment``` 标签包围起来)。

例如:下面包含了两个顶层标签h1和p，是会报错

```jsx
var HelloMessage = React.createClass({
    render: function () {
        return <h1>
            Hello {this.props.name}
        </h1>
        <p>
            some text
        </p>;
    }
});
```

## 5. 组件的属性

### 5.1. 属性props

组件的用法与原生的 HTML 标签完全一致，可以任意加入属性，比如 ```<HelloMessage name="John">``` ，就是 ```HelloMessage``` 组件加入一个 ```name``` 属性，值为 ```John```。

组件的属性可以在组件类的 ```this.props``` 对象上获取，比如 name 属性就可以通过 ```this.props.name``` 读取。

**注意：**
添加组件属性，```class``` 属性需要写成 ```className``` ，```for``` 属性需要写成 ```htmlFor``` ，这是因为 ```class``` 和 ```for``` 是 js 的保留字。

```css
.testClass {
    color: red;
}
```

```jsx
var HelloMessage = React.createClass({
    render: function () {
        return <h1 className={this.props.class}>Hello, {this.props.name}</h1>;
    }
});

ReactDOM.render(
    <HelloMessage name="张三" class="testClass" />,
    document.getElementById('example')
);
```

### 5.2. 默认属性

getDefaultProps 方法可以用来设置组件属性的默认值。

```jsx
var HelloMessage = React.createClass({
    getDefaultProps: function () {
        return {
            name: '李四'
        };
    },
    render: function () {
        return <h1 className={this.props.class}>Hello, {this.props.name}</h1>;
    }
});

ReactDOM.render(
    <HelloMessage class="testClass" />,
    document.getElementById('example')
);
```

### 5.3. 验证属性是否符合要求(PropTypes)

组件的属性可以接受任意值，字符串、对象、函数等等都可以。有时，我们需要一种机制，验证别人使用组件时，提供的参数是否符合要求。
组件类的```PropTypes```属性，就是用来验证组件实例的属性是否符合要求。

```jsx
var HelloMessage = React.createClass({
    propTypes: {
        name: React.PropTypes.string.isRequired,
    },
    render: function () {
        return <ol name={this.props.name}>
            {
                React.Children.map(this.props.children, function (child) {
                    return <li>{child}</li>
                })
            }
        </ol>;
    }
});

var name = 123;

ReactDOM.render(
    <HelloMessage name={name} class="testClass">
        <span>张三</span>
        <span>李四</span>
        <span>王五</span>
        <span>赵六</span>
        <span>钱七</span>
    </HelloMessage>,
    document.getElementById('example')
);
```

控制台会显示一行错误信息。

```js
Warning: Failed prop type: Invalid prop `name` of type `number` supplied to `HelloMessage`, expected `string`.
    in HelloMessage
```

## 6. 组件的子节点

### 6.1. this.props.children

**this.props** 对象的属性与组件的属性一一对应，但是有一个例外，就是 **this.props.children** 属性。

> this.props.children表示组件的所有子节点。

```jsx
var HelloMessage = React.createClass({
    render: function () {
        return <ol>
            {
                React.Children.map(this.props.children, function (child) {
                    return <li>{child}</li>
                })
            }
        </ol>;
    }
});
ReactDOM.render(
    <HelloMessage name="John" class="testClass">
        <span>张三</span>
        <span>李四</span>
        <span>王五</span>
        <span>赵六</span>
        <span>钱七</span>
    </HelloMessage>,
    document.getElementById('example')
);
```

### 6.2. React.Children.map

注意，**this.props.children** 的值有三种可能：

- 如果当前组件没有子节点，它就是**undefined**;
- 如果有一个子节点，数据类型是 **object** ；
- 如果有多个子节点，数据类型就是 **array** 。

所以，处理 this.props.children 的时候要小心。

React 提供一个工具方法 **React.Children** 来处理 **this.props.children** 。我们可以用 **React.Children.map** 来遍历子节点，而不用担心 **this.props.children** 的数据类型是 **undefined** 还是 **object**。

## 7. 获取真实的DOM节点

组件并不是真实的 DOM 节点，而是存在于内存之中的一种数据结构，叫做虚拟 DOM （virtual DOM）。只有当它插入文档以后，才会变成真实的 DOM 。根据 React 的设计，所有的 DOM 变动，都先在虚拟 DOM 上发生，然后再将实际发生变动的部分，反映在真实 DOM上，这种算法叫做 DOM diff ，它可以极大提高网页的性能表现。

但是，有时需要从组件获取真实 DOM 的节点，这时就要用到 ```ref``` 属性

```jsx
var MyComponent = React.createClass({
    handleClick: function () {
        this.refs.myTextInput.focus();
    },
    render: function () {
        return (
            <div>
                <input type="text" ref="myTextInput" />
                <input type="button" value="Focus the text input" onClick={this.handleClick} />
            </div>
        );
    }
});

ReactDOM.render(
    <MyComponent />,
    document.getElementById('example')
);
```

上面代码中，组件 MyComponent 的子节点有一个文本输入框，用于获取用户的输入。这时就必须获取真实的 DOM 节点，虚拟 DOM 是拿不到用户输入的。为了做到这一点，文本输入框必须有一个 ref 属性，然后 this.refs.[refName] 就会返回这个真实的 DOM 节点。

需要注意的是，由于 this.refs.[refName] 属性获取的是真实 DOM ，所以必须等到虚拟 DOM 插入文档以后，才能使用这个属性，否则会报错。上面代码中，通过为组件指定 Click 事件的回调函数，确保了只有等到真实 DOM 发生 Click 事件之后，才会读取 this.refs.[refName] 属性。

React 组件支持很多事件，除了 Click 事件以外，还有 KeyDown 、Copy、Scroll 等，完整的事件清单请查看官方文档。

## 8. 组件的状态

### 8.1. this.state

组件免不了要与用户互动，React 的一大创新，就是将组件看成是一个状态机，一开始有一个初始状态，然后用户互动，导致状态变化，从而触发重新渲染 UI 。

```jsx
var LikeButton = React.createClass({
    getInitialState: function () {
        return { liked: false };
    },
    handleClick: function (event) {
        this.setState({ liked: !this.state.liked });
    },
    render: function () {
        var text = this.state.liked ? '喜欢' : '不喜欢';
        return (
            <p onClick={this.handleClick}>
                我{text}你。 点击切换。
            </p>
        );
    }
});

ReactDOM.render(
    <LikeButton />,
    document.getElementById('example')
);
```

上面代码是一个 LikeButton 组件，它的 getInitialState 方法用于定义初始状态，也就是一个对象，这个对象可以通过 this.state 属性读取。当用户点击组件，导致状态变化，this.setState 方法就修改状态值，每次修改以后，自动调用 this.render 方法，再次渲染组件。

### 8.2. state与props的区别

由于 this.props 和 this.state 都用于描述组件的特性，可能会产生混淆。一个简单的区分方法是，this.props 表示那些一旦定义，就不再改变的特性，而 this.state 是会随着用户互动而产生变化的特性。

### 8.3. 表单form

用户在表单填入的内容，属于用户跟组件的互动，所以不能用 ```this.props``` 读取

```jsx
var Input = React.createClass({
    getInitialState: function () {
        return { value: 'Hello!' };
    },
    handleChange: function (event) {
        this.setState({ value: event.target.value });
    },
    render: function () {
        var value = this.state.value;
        return (
            <div>
                <input type="text" value={value} onChange={this.handleChange} />
                <p>{value}</p>
            </div>
        );
    }
});

ReactDOM.render(<Input />, document.getElementById('example'));
```

上面代码中，文本输入框的值，不能用 this.props.value 读取，而要定义一个 onChange 事件的回调函数，通过 event.target.value 读取用户输入的值。textarea 元素、select元素、radio元素也属于这种情况

## 9. 组件的生命周期

![Component的生命周期](Component的生命周期.png)

### 9.1. 组件的三个状态

组件的生命周期分成三个状态：

- Mounting：已插入真实 DOM
- Updating：正在被重新渲染
- Unmounting：已移出真实 DOM

### 9.2. 每个状态的处理函数

React 为每个状态都提供了两种处理函数，will 函数在进入状态之前调用，did 函数在进入状态之后调用，三种状态共计五种处理函数。

- componentWillMount()
- componentDidMount()
- componentWillUpdate(object nextProps, object nextState)
- componentDidUpdate(object prevProps, object prevState)
- componentWillUnmount()

### 9.3. 特殊状态的处理函数

此外，React 还提供两种特殊状态的处理函数。

- componentWillReceiveProps(object nextProps)
已加载组件收到新的参数时调用
- shouldComponentUpdate(object nextProps, object nextState)
组件判断是否重新渲染时调用

### 9.4. 示例：打印每个处理函数

```jsx
var Hello = React.createClass({
    componentWillMount: function () {
        console.log('componentWillMount');
    },
    componentDidMount: function () {
        console.log('componentDidMount');
    },
    componentWillUpdate: function (nextProps, nextState) {
        console.log('componentWillUpdate');
        console.log(nextProps);
        console.log(nextState);
    },
    componentDidUpdate: function (prevProps, prevState) {
        console.log('componentDidUpdate');
        console.log(prevProps);
        console.log(prevState);
    },
    componentWillUnmount: function () {
        console.log('componentWillUnmount');
    },
    componentWillReceiveProps(nextProps) {
        console.log('componentWillReceiveProps');
        console.log(nextProps);
    },
    shouldComponentUpdate(nextProps, nextState) {
        console.log('shouldComponentUpdate');
        console.log(nextProps);
        console.log(nextState);
        return true;
    },
    getInitialState: function () {
        return { class: 'testClass' };
    },
    handleClick: function () {
        this.setState({ class: this.state.class ? '' : 'testClass' });
    },
    render: function () {
        return <h1 className={this.state.class} onClick={this.handleClick}>
            Hello {this.props.name}
        </h1>;
    }
});

ReactDOM.render(
    <Hello name="world" />,
    document.getElementById('example')
);
```

### 9.5. 示例：组件渐隐

#### 9.5.1. 组件渐隐

上面代码在hello组件加载以后，通过 componentDidMount 方法设置一个定时器，每隔100毫秒，就重新设置组件的透明度，从而引发重新渲染。

```jsx
var Hello = React.createClass({
    getInitialState: function () {
        return {
            opacity: 1.0
        };
    },

    componentDidMount: function () {
        this.timer = setInterval(function () {
            var opacity = this.state.opacity;
            opacity -= .05;
            if (opacity < 0.1) {
                opacity = 1.0;
            }
            this.setState({
                opacity: opacity
            });
        }.bind(this), 100);
    },

    render: function () {
        return (
            <div style={{ opacity: this.state.opacity }}>
                Hello {this.props.name}
            </div>
        );
    }
});

ReactDOM.render(
    <Hello name="world" />,
    document.getElementById('example')
);
```

#### 9.5.2. 组件中的样式

另外，组件的style属性的设置方式也值得注意，不能写成

```jsx
style="opacity:{this.state.opacity};"
```

而要写成

```jsx
style={{opacity: this.state.opacity}}
```

这是因为 React 组件样式是一个对象，所以第一重大括号表示这是 JavaScript 语法，第二重大括号表示样式对象。

## 10. AJAX

