import Vue from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import ResourceMonitor from '../components/ResourceMonitor.vue'; 
import DataGenerator from '../components/DataGenerator.vue';
import DataTest from '../components/DataTest.vue'; 
import Home from '../components/Home.vue';

// Vue.use(VueRouter);
// const router = createRouter({
//     history: createWebHistory(process.env.BASE_URL),
//     routes,
// });
  
// export default router;

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
  {
    path: '/data-test',
    name: 'DataTest',
    component: DataTest
  },
  {
    path: '/',
    name: 'Home',
    component: Home
  }
  // 添加更多路由
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});
  
export default router;
// const router = new VueRouter({
//   mode: 'history',
//   base: process.env.BASE_URL,
//   routes
// });

// export default router;
