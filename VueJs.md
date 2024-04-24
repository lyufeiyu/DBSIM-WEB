
# 前言
Vue 是一个前端框架，它使得构建交互式应用程序变得更加容易，让前端开发者能够更好地处理复杂的数据，并使得用户界面更加美观、可应对各种设备。使用 Vue 可以在较短的时间内构建出具有雄心壮志的单页应用程序，它也很容易与其他工具协同工作。<br>
学习VUE之前，要学习 ES6 的语法，ES6 教程可以看 ES6.md

# 安装Vue
首先，需要从 Vue 的官方网站下载相关的脚本文件，或者通过类似 npm 或 Yarn 的工具安装。下载的文件包含了 Vue 的核心代码和几个常用的插件，可以通过 script 标签或操作性的方法引入到你的项目中。
下载脚本，可以在官网中下载。
```JS
//引包
<script src="./vue.js"></script>
//或者 不需要下载直接引用Vue 库
<script src="https://cdn.jsdelivr.net/npm/vue"></script>
```

# Vue.JS概念
Vue.js（通常称为Vue）是一个用于构建用户界面的渐进式JavaScript框架。它专注于视图层，采用了响应式数据绑定和组件化的开发方式，可以帮助开发者构建交互性的单页应用程序（Single-Page Applications，SPA）和可复用的组件。

Vue.js的核心思想是通过将视图（HTML模板）和数据（JavaScript对象）进行双向绑定，实现数据的自动更新和视图的响应性。这意味着当数据发生变化时，页面上对应的视图部分会自动更新，而不需要手动操作DOM。这使得开发者能够专注于业务逻辑和数据处理，而不必过多关注繁琐的DOM操作。

Vue.js也支持组件化开发，通过将页面拆分为多个独立可复用的组件，实现更好的代码组织和可维护性。每个组件都有自己的模板、逻辑和样式，可以独立进行开发和测试，并可以在不同的应用程序中共享和复用。

Vue.js还提供了许多其他功能和特性，如路由管理（Vue Router）、状态管理（Vuex）、动画效果（Vue Transitions）等，以满足不同项目的需求。

总的来说，Vue.js 是一个灵活、易学且功能强大的前端框架，帮助开发者构建高效、响应式的用户界面。

# Vue.JS特点
Vue.js 作为一个主流的前端框架，与其他框架相比具有以下特点和优势：

📒简单易学
Vue.js 的语法和概念相对简单，易于学习和上手。它采用了响应式的数据绑定和组件化的开发方式，使得开发者可以快速构建交互式的单页应用程序。

📒灵活性
Vue.js 可以与其他库或现有项目集成，也可以逐步应用到现有项目中。它不强制性地依赖特定的工具链，因此开发者可以根据自身需求选择合适的构建工具和库。

📒渐进式框架
Vue.js 是一个渐进式框架，可以根据项目规模和复杂度选择使用不同规模的功能。无论是小型的交互式组件还是大型的单页应用程序，Vue.js 都能提供适当的解决方案。

📒性能优化
Vue.js 在性能方面做了很多优化，包括虚拟 DOM、异步更新、组件级别的缓存策略等。这些优化措施使得应用程序可以高效地运行，响应速度更快。

📒生态系统丰富
Vue.js 生态系统非常丰富，有大量的第三方插件和库可供选择，以满足各种需求。同时，Vue.js 也有一个活跃的社区，提供了丰富的教程、文档和支持。

与其他框架相比，例如 React 和 Angular，Vue.js 的学习曲线相对较低，语法更加简洁直观。React 更加注重组件化和声明式编程，而 Angular 更注重模块化和强大的工具集。不同的框架适用于不同的项目和团队需求，开发者可以根据自身情况和偏好选择合适的框架。

# 插值表达式
## 文本
Vue 的插值表达式用双大括号{{}}表示，可以将数据动态地绑定到模板中。在双大括号中，你可以使用 Vue 实例中的数据属性，并将其显示在视图中。
```HTML
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>vue的插值表达式</title>
    </head>
    <body>

        <div id="app">
            <h2>{{ text }}</h2>
        </div>

        <script src="./vue.js"></script>
        <script>
            const v = new Vue({
                el:'#app',
                data:{
                    text:'vue study'
                }
            });
        </script>
    </body>
</html>
```
在上面的例子中，我们创建了一个 Vue 实例，并将其绑定到 id 为 app 的元素上。data 选项用来定义实例的数据属性，其中 text是一个字符串类型的数据属性。

在 HTML 文件中，我们通过使用双大括号 {{}} 的插值表达式来显示 text属性的值。当 Vue 实例中的 text属性发生变化。

vue是默认的双向绑定，若不想双向绑定，一次性数据的请用指令 v-once 指令，不过请小心影响到该节点上所有的数据绑定：

```html
<span v-once>这个将不会改变: {{ msg }}</span>
```


## HTML
在 Vue 的插值表达式中，默认情况下会对输出的文本内容进行转义，以防止XSS（跨站脚本攻击）的安全问题。这意味着如果你在插值表达式中包含 HTML 标签，它们将会以文本形式被展示而不会被解析为实际的 HTML。

如果你确实需要在插值表达式中显示原始 HTML，可以使用 v-html 指令。与 v-text 指令不同，v-html 指令会解析绑定的数据中包含的 HTML 标签，并将其作为实际的 HTML 内容进行渲染。

示例：
```html
<div v-html="htmlContent"></div>
```
在上面的示例中，htmlContent 是 Vue 实例中的一个数据属性，它的值是一个包含 HTML 标签的字符串。v-html 指令会将 htmlContent 的值解析为 HTML，并将其渲染到 div 元素中。

需要注意的是，对于使用 v-html 指令的内容，要确保它们来自于可信的来源，以避免潜在的安全风险。使用不受信任的内容时，一定要进行恰当的过滤和验证。

总结：插值表达式默认会将输出的文本进行转义，但如果你需要在 Vue 模板中显示原始 HTML 内容，可以使用 v-html 指令来实现。请谨慎使用，并确保内容来源可信。

## Attribute
在 Vue 的插值表达式中，你可以使用 v-bind 指令（或简写形式的冒号 :）来动态绑定 HTML 属性。

以下是一些例子：

- 使用变量绑定属性值：
```html
<a v-bind:href="url">{{ linkText }}</a>
```
在上面的例子中，属性 href 的值将被动态地绑定为 url 变量的值。linkText 表达式将作为链接的文本内容。

- 直接绑定表达式作为属性值：
```html
<img v-bind:src="imageSrc">
```
在上面的例子中，src 属性的值将被绑定为 imageSrc 表达式的值。这通常用于动态加载图像。

- v-bind缩写:
```html
<!-- 完整语法 -->
<a v-bind:href="url">...</a>

<!-- 缩写 -->
<a :href="url">...</a>
```

- 另一个例子是 v-on 指令，它用于监听 DOM 事件：
```html
<a v-on:click="doSomething">...</a>
```

- v-on缩写:
```html
<!-- 完整语法 -->
<a v-on:click="doSomething">...</a>

<!-- 缩写 -->
<a @click="doSomething">...</a>
```

它们看起来可能与普通的 HTML 略有不同，但 : 与 @ 对于特性名来说都是合法字符，在所有支持 Vue.js 的浏览器都能被正确地解析。而且，它们不会出现在最终渲染的标记中。缩写语法是完全可选的，但随着你更深入地了解它们的作用，你会庆幸拥有它们。


- 绑定动态的 CSS 类：
```html
<div v-bind:class="active ? 'active' : 'inactive'"></div>
```
在上面的例子中，class 属性的值将根据 active 变量的值动态绑定不同的 CSS 类。

请注意，对于布尔类型的属性，通过简单地省略属性值可以将其绑定为真值：
```html
<input type="checkbox" v-bind:checked="isActive">
```
在上面的例子中，如果 isActive 为 true，则 checked 属性会被添加到 元素上。

总结：通过使用 v-bind 指令，在 Vue 的插值表达式中可以动态地绑定 HTML 属性。你可以使用变量、表达式或布尔值来绑定属性的值。

## 使用 JavaScript 表达式
在 Vue 的插值表达式中，你可以使用 JavaScript 表达式执行简单的计算、逻辑判断和其他操作。以下是一些例子：

- 执行简单的计算：
```html
<p>{{ num1 + num2 }}</p>
```

上面的例子中，Vue 将会计算 num1 和 num2 的和，并将结果作为文本显示在标签中。

- 进行逻辑判断：
```html
<p v-if="showText">{{ message }}</p>
```
在上面的例子中，当 showText 的值为真时，Vue 将会渲染显示 message 变量的值。否则，该段落标签将不会显示。

- 调用函数或方法：
```html
<p>{{ getFullName(firstName, lastName) }}</p>
```
在上面的例子中，getFullName 是一个在 Vue 实例中定义的方法，它接收 firstName 和 lastName 作为参数，并返回一个完整的姓名。

请注意，插值表达式中的 JavaScript 表达式应该是简单和非副作用的。复杂的逻辑和大量的计算应该尽量放在 Vue 实例的计算属性或方法中，然后在插值表达式中使用这些属性或方法。

# 代码示例
```HTML
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>vue的插值表达式</title>
    </head>
    <body>

        <div id="app">
            <h2>{{ text }}</h2>
            <h2>{{ getContent() }}</h2>
            <h2>{{ 1<2 ? 'true':'false' }}</h2>
        </div>

        <script src="./vue.js"></script>
        <script>
            const v = new Vue({
                el:'#app',
                data:{
                    text:'vue study',
                    text2:'Hello!'
                },
                methods:{
                    getContent(){
                        return this.text2 + ' ' + this.text
                    }
                }
            });
        </script>
    </body>
</html>
```

# vue生命周期表
学好vue生命周期表是绝对要看懂的

将官网生命周期图示进行注解，以加深印象和理解
![alt text](assets\lifeCirclePattern.png)

# Vue实例
每个 Vue 应用都是通过用 Vue 函数创建一个新的 Vue 实例开始的：
```JS
var vm = new Vue({
  // 选项
})
```

# 实例生命周期钩子

每个 Vue 实例在被创建时都要经过一系列的初始化过程——比如在设置数据绑定、方法传参将实例挂载到 DOM 并在数据变化时更新 DOM 等。同时在过程中也就运行了一些叫做生命周期钩子的函数，可以在不同的阶段添加自己的代码的机会。

比如 mounted 钩子可以用来在一个实例被创建之后执行代码：
```JS
new Vue({
  data: {
    a: 1
  },
  mounted: function () {
    // `this` 指向 vm 实例
    console.log('a is: ' + this.a)
  }
})
// => "a is: 1"
```
也有一些其它的钩子，在实例生命周期的不同阶段被调用，如updated 和 destroyed。生命周期钩子的 this 上下文指向调用它的 Vue 实例。

~~~
在Vue.js中，组件的生命周期是指组件从创建到销毁的整个过程，而生命周期钩子函数则是在不同阶段执行的函数，允许您在特定时间点添加自定义逻辑。本文将详细介绍组件的生命周期以及常用的生命周期钩子函数。
~~~

### 组件的生命周期
组件的生命周期可以分为以下几个阶段：

- 创建阶段： 在这个阶段，组件被实例化，初始化数据，并准备渲染。

- 挂载阶段： 组件在这个阶段被添加到DOM中，进行渲染，此时组件的模板被编译成真实的DOM元素。

- 更新阶段： 当组件的状态或数据发生变化时，它会进行重新渲染，进入更新阶段。

- 卸载阶段： 当组件从DOM中移除时，它进入卸载阶段，此时可以进行一些清理工作。

创建阶段
- beforeCreate： 在实例被创建之前被调用，此时实例的属性和方法还未初始化。
- created： 在实例被创建之后被调用，此时可以访问实例的属性和方法，但是还未挂载到DOM。

挂载阶段
- beforeMount： 在组件挂载到DOM之前被调用，此时模板已经编译完成，但尚未渲染。
- mounted： 在组件挂载到DOM之后被调用，此时组件已经渲染完成，可以访问DOM元素。

更新阶段
- beforeUpdate： 在组件数据更新之前被调用，可以在此阶段进行一些数据处理。
- updated： 在组件数据更新之后被调用，此时DOM已经更新完成。

卸载阶段
- beforeDestroy： 在组件销毁之前被调用，此时组件实例仍然可用。
- destroyed： 在组件销毁之后被调用，此时组件实例已经被销毁，无法再访问其属性和方法。

示例：使用生命周期钩子函数
```JS
<template>
  <div>
    <p>{{ message }}</p>
    <button @click="changeMessage">改变消息</button>
  </div>
</template>
 
<script>
export default {
  data() {
    return {
      message: 'Hello, Vue!'
    };
  },
  beforeCreate() {
    console.log('beforeCreate hook');
  },
  created() {
    console.log('created hook');
  },
  beforeMount() {
    console.log('beforeMount hook');
  },
  mounted() {
    console.log('mounted hook');
  },
  beforeUpdate() {
    console.log('beforeUpdate hook');
  },
  updated() {
    console.log('updated hook');
  },
  beforeDestroy() {
    console.log('beforeDestroy hook');
  },
  destroyed() {
    console.log('destroyed hook');
  },
  methods: {
    changeMessage() {
      this.message = 'Hello, Lifecycle!';
    }
  }
};
</script>
```
在上面的例子中，您可以在控制台中查看不同阶段的生命周期钩子函数的调用情况。通过在这些钩子函数中添加自定义逻辑，您可以在不同阶段实现特定的操作。

组件的生命周期和生命周期钩子函数是Vue.js中非常重要的概念。它们使得您可以在不同阶段执行自定义的操作，从而实现更精细的控制和逻辑。了解生命周期的不同阶段和常用的生命周期钩子函数，将有助于您更好地理解和利用Vue.js框架，构建出更高效、可维护的应用程序。


# 模板语法
Vue.js 使用了基于 HTML 的模板语法，允许开发者声明式地将 DOM 绑定至底层 Vue 实例的数据。所有 Vue.js 的模板都是合法的 HTML ，所以能被遵循规范的浏览器和 HTML 解析器解析。

在底层的实现上，Vue 将模板编译成虚拟 DOM 渲染函数。结合响应系统，Vue 能够智能地计算出最少需要重新渲染多少组件，并把 DOM 操作次数减到最少。

如果你熟悉虚拟 DOM 并且偏爱 JavaScript 的原始力量，你也可以不用模板，直接写渲染 (render) 函数，使用可选的 JSX 语法。(官网原话)



