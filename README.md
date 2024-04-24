# 前后端设计思路
## 项目布局
我们一般是将前端和后端当作两个独立的项目来处理，这是因为它们各自有不同的依赖和构建过程。所以，它们通常会分别创建在不同的文件夹中，以保持结构的清晰和独立性。
总体的项目布局是这样的：
```
/DB_WEB
│
├── db_django/           # Django后端项目的根目录
│   ├── your_app/      # Django应用
│   ├── manage.py      # Django项目的管理脚本
│   └── ...            # 其他Django项目文件
│
├── db_vue/          # Vue前端项目的根目录
│   ├── node_modules/  # 前端项目依赖
│   ├── src/           # Vue源代码
│   ├── public/        # 静态资源和index.html
│   ├── package.json   # 前端项目的依赖列表
│   └── ...            # 其他Vue项目文件
│
└── shared/            # 可能的共享资源，如共用的模型定义、配置文件等
```

## 前后端优势
先写前端的优势：
- 直观反馈：前端开发能够让您直观地看到界面和用户交互的效果，对于初学者来说可能会更有成就感。
- 易于模拟：可以使用假数据或Mock服务来模拟后端API，这允许您在后端开发完成之前就能进行前端的开发。
- 用户体验关注：从用户的角度开始构建您的应用，有助于您在设计和开发中更好地理解用户需求和用户体验。

先写后端的优势：
- 核心逻辑：后端通常涉及应用的业务逻辑和数据处理，优先开发后端能够确保系统的核心稳定。
- API先行：一旦后端API定义好了，前端开发就可以基于这些API进行，这有助于前后端分工和并行开发。
- 技术挑战：后端涉及的技术可能更加多样化（数据库、服务器配置、API设计等），这可能对您来说是一个更具挑战性的起点。

注：我决定还是先写前端吧

# 前端
## 一些准备工作
创建一个虚拟环境db_web（在Windows和Linux系统上，都可以使用以下命令创建虚拟环境）
```sh
python -m venv db_web
```
安装Vue CLI（Vue的命令行工具）
```sh
npm install -g @vue/cli
```
创建一个vue项目
```sh
vue create db_vue
```
注：一开始我这里选择了版本3，即选择了Vue3。结果后面一堆bug，所以后面删了重新建了一个Vue2的项目。......后面因为作图的原因又换回了vue3（这波算是非常惨痛的教训了）


## 创建的Vue项目的文件结构说明：
- node_modules/: 存放项目依赖的库。当您运行npm install或yarn时，所有在package.json中列出的依赖都会被安装在这个目录下。
- public/: 包含静态资源，如index.html和favicon.ico。这里的文件在构建过程中通常会被复制到输出目录，而不会经过webpack处理。
	- favicon.ico: 网站的图标，显示在浏览器标签页上。
	- index.html: 应用的入口HTML文件。Vue CLI项目在构建时会将处理后的资源自动注入到这个文件中。
- src/: 包含源代码，是您主要工作的目录。
	- assets/: 存放静态资源，如图片、样式等，这些资源在构建过程中会被webpack处理。
		- logo.png: 示例图片，可以在组件中使用。
	- components/: 存放Vue组件的目录。
		- HelloWorld.vue: 一个示例Vue单文件组件，展示基本的Vue组件结构。
	- App.vue: 根Vue组件，应用的主要视图都在这里渲染。
	- main.js: Vue应用的入口文件。在这里创建Vue实例，并挂载到DOM中。
- .gitignore: Git版本控制的配置文件，指定不需要加入版本控制的文件和目录。
- babel.config.js: Babel的配置文件。Babel是一个JavaScript编译器，用于将ES6+代码转换为向后兼容的JavaScript版本。
- jsconfig.json: VS Code的JavaScript项目配置文件，用于改善开发体验。
- package.json: 包含项目的元数据和依赖列表。通过这个文件，npm/yarn知道如何安装和配置依赖。
- package-lock.json 或 yarn.lock: 确保其他开发者在安装依赖时能够得到与您相同版本的依赖，从而确保环境的一致性。
- README.md: 项目的说明文件，通常包含项目信息、构建步骤、使用方法等。
- vue.config.js: Vue CLI的配置文件。这里可以自定义Vue CLI的构建过程，比如修改webpack配置、指定环境变量等。
~~~
这个结构是基于Vue CLI 3或更高版本。当开始开发时，通常需要关注src目录中的内容，因为这是Vue组件和应用逻辑所在的地方。随着应用的扩展，你可能还会添加更多的目录和文件，如用于路由的router.js、状态管理的store.js（如果使用Vuex）等。
~~~
- 项目的开发通常从编辑App.vue和components目录下的组件开始。
- 如果您想使用router或Vuex等，可以通过Vue CLI的插件系统轻松添加它们。
- 对于大型项目，可能还需要组织和管理状态，对代码进行单元测试等。
- Vue CLI提供了很多内置的webpack优化，我们可以通过修改vue.config.js来进一步自定义这些设置。

## 安装View UI (只能vue2使用，vue3淘汰了，后面我用vue3重写的时候直接报废)
```sh
npm install view-design --save
或
yarn add view-design
（如果你使用Yarn）
```

在项目中引入View UI。你可以在main.js或main.ts文件中全局引入View UI和它的CSS文件，这样就可以在整个项目中使用View UI提供的组件了。


## 安装view-design（vue3不能用了啊啊啊啊）
在项目文件夹中，运行
```SH
npm install view-design --save
```
或
```SH
yarn add view-design
```
（如果你使用Yarn）来安装View UI。
在main.js中，确保您导入了View UI并且使用了它：
```JS
import Vue from 'vue';
import ViewUI from 'view-design';
import 'view-design/dist/styles/iview.css';

Vue.use(ViewUI);
```
同时对组件进行注册，如下：
```JS
import Vue from 'vue';
import { Card, Row, Col } from 'view-design';

Vue.component('Card', Card);  //这是全局注册，如果用export default就是局部注册
Vue.component('Row', Row);
Vue.component('Col', Col);
```


## 在App.vue中导入其他组件
步骤 1：创建组件文件

在 src/components/ 文件夹内创建一个新的 .vue 文件。例如，创建一个名为 MyComponent.vue 的文件。

步骤 2：编写组件

在 MyComponent.vue 文件中编写我的组件代码。一个基本的组件结构包括`<template>, <script>, 和 <style> 部分：`
```html
<template>
  <div>
    <!-- 组件的 HTML 结构 -->
    <h1>这是我的组件</h1>
  </div>
</template>

<script>
export default {
  name: 'MyComponent',
  // 组件的数据和方法
};
</script>

<style scoped>
/* 组件的局部样式 */
</style>
```

步骤 3：导入组件

在 App.vue 中，您需要使用 import 语句导入 MyComponent 组件：
```html
<script>
import MyComponent from './components/MyComponent.vue';

export default {
  name: 'App',
  components: {
    MyComponent // 将 MyComponent 注册为子组件
  },
  // 其他选项...
};
</script>
```

步骤 4：使用组件

在 App.vue 的 `<template>` 部分中使用 MyComponent：

```html
<template>
  <div id="app">
    <MyComponent/> <!-- 使用组件 -->
    <!-- 其他 HTML 结构... -->
  </div>
</template>
```
注意 `<MyComponent/>` 标签的命名与 import 时指定的名称相对应。


## 设置vue-router路由
首先在终端安装与 Vue 2 兼容的 vue-router 版本
命令如下：
```sh
npm install vue-router@3.5.3 --save
```
（1）App.vue模板代码

在 App.vue 中，我们将使用 `<router-view>` 来显示当前路由匹配的组件：
```html
<template>
  <Layout class="layout">
    <Sidebar />
    <Layout class="main-content">
      <router-view></router-view> <!-- 路由视图 -->
    </Layout>
  </Layout>
</template>

<style>
.main-content {
  flex: 1; /* 主内容区域应占据剩余空间 */
  padding: 20px; /* 根据需要添加内边距 */
}
</style>
```

（2）设置路由

先在 src/router/index.js 中设置路由（如果还没有，请先创建该文件）：

```js
import Vue from 'vue';
import VueRouter from 'vue-router';
import ResourceMonitor from '../components/ResourceMonitor.vue';  // 替换成自己的组件
import DataGenerator from '../components/DataGenerator.vue'; 

Vue.use(VueRouter);

const routes = [
  {
    path: '/resource-monitor',
    name: 'ResourceMonitor',
    component: ResourceMonitor
  },
  {
    path: '/data-generator',
    name: 'DataGenerator',
    component: DataGenerator
  },
  // 添加更多路由
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

export default router;
```

（3）创建对应的主内容区组件

创建相应的组件文件，比如 ResourceMonitor.vue 和 DataGenerator.vue，并在这些文件中编写各自的模板和脚本。

（4）整合路由

在 main.js 文件中，引入路由并告诉 Vue 实例使用这些路由：
```js
import Vue from 'vue';
import App from './App.vue';
import router from './router'; // 引入路由配置

new Vue({   // 我们应该只调用一次 new Vue(...) 来创建您的根 Vue 实例
  router, // 使用路由
  render: h => h(App)
}).$mount('#app');
```

（5）在侧边栏组件 Sidebar.vue 中进行路由链接的配置

在 Sidebar.vue 组件中，我们需要为 Menu 组件添加 @on-select 事件来处理菜单项的点击事件，并使用 this.$router.push({ name: 'RouteName' }) 来改变路由。如：

```html
<template>
  <!-- 侧边栏菜单 -->
</template>

<script>
export default {
  // ...组件代码
  methods: {
    handleMenuItemSelect(name) {
      if(name === '1') {
        this.$router.push({ name: 'ResourceMonitor' });
      } else if(name === '2') {
        this.$router.push({ name: 'DataGenerator' });
      }
      // 处理其他菜单项
    }
  }
};
</script>
```
同时确保在 Menu 组件上绑定了该方法：
```html
<Menu @on-select="handleMenuItemSelect">
  <!-- 菜单项 -->
</Menu>
```
现在，就可以通过点击侧边栏中的不同菜单项来切换主内容区。

