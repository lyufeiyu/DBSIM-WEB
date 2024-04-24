// import Vue from 'vue'
// import App from './App.vue'
// import Antd from 'ant-design-vue';
// // import 'ant-design-vue/dist/antd.css'; // 引入Ant Design Vue样式
// import router from './router'; // 引入路由配置

// Vue.config.productionTip = false

// // 导入并使用Ant Design Vue
// Vue.use(Antd); 

// // 注册全局组件可以在这里添加
// // 例如：Vue.component('AIcon', Icon);

// new Vue({
//   router, // 使用路由
//   render: h => h(App)
// }).$mount('#app');
import  {createApp}  from 'vue';
import App from './App.vue';
import router from './router';
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';


// Create a new Vue application
const app = createApp(App);

// Use the router instance
app.use(router);

// Use Ant Design Vue
app.use(Antd);

// Mount the app to the DOM
app.mount('#app');
