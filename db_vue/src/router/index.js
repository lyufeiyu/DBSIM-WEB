// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router';

// ...其他视图导入...
import Home from '../views/Home.vue';
import ResourceMonitor from '../views/ResourceMonitor.vue';
import DataGenerator from '../views/DataGenerator.vue';
import DataTest from '../views/DataTest.vue';

import store from '../store'; // 确保从正确的地方引入了store

const routes = [
    // ...路由定义...
    {
        path: '/',
        name: 'Home',
        component: Home,
        meta: { title: '首页' } // 为路由添加 meta 属性
    },
    {
        path: '/monitor',
        name: 'ResourceMonitor',
        component: ResourceMonitor,
        meta: { title: '资源监控' } // 为路由添加 meta 属性
    },
    {
        path: '/generate',
        name: 'DataGenerator',
        component: DataGenerator,
        meta: { title: '数据生成' } // 为路由添加 meta 属性
    },
    {
        path: '/test',
        name: 'DataTest',
        component: DataTest,
        meta: { title: '数据测试' } // 为路由添加 meta 属性
    }
    // 你可以继续添加更多的路由规则
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

router.beforeEach((to, from, next) => {
    // 确保每个路由都有meta属性，并且设置了title
    if (to.meta && to.meta.title) {
        store.dispatch('addBreadcrumb', { name: to.meta.title, path: to.path });
    }
    next();
});

export default router;
