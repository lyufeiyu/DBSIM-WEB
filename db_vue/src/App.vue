<template>
    <div id="app">
        <header class="app-header">
            <li><i class="fa-solid fa-shekel-sign"></i>DBSIM-WEB</li>
        </header>
        <div class="app-body">
            <aside class="app-sidebar">
                <Sidebar />
            </aside>
            <main class="app-main">
                <Breadcrumbs />
                <!-- 使用 v-slot 语法和 <keep-alive> -->
                <router-view v-slot="{ Component }">
                    <keep-alive>
                        <component :is="Component" />
                    </keep-alive>
                </router-view>
            </main>
        </div>
    </div>
</template>

<script>
import Sidebar from "./components/Sidebar.vue";
import Breadcrumbs from "./components/Breadcrumbs.vue";

export default {
    name: "App",
    components: {
        Sidebar,
        Breadcrumbs,
    },
};
</script>

<style>
html,
body {
    height: 100%;
    margin: 0;
    overflow: hidden; /* 防止整个页面滚动 */
}

#app {
    text-align: center;
    font-family: Avenir, Helvetica, Arial, sans-serif;
    height: 100vh; /* 确保 #app 填满整个视口高度 */
}

.app-header {
    background-color: #dbf0f9; /* 淡黄色 */
    padding: 15px 39px;
    font-size: 24px;
    color: #191616;
    text-align: left;
    margin-bottom: 0; /* 移除底部外边距 */
}

.app-body {
    display: flex;
    height: calc(100vh - 50px); /* 减去 header 的高度 */
    flex: 1; /* 占据剩余的空间 */
    overflow: hidden; /* 如果需要，可以在这里防止内容区滚动 */
}

.app-sidebar {
    background-color: #dbf0f9; /* 淡黄色 */
    width: 12%;
    padding: 20px;
    height: 100%; /* 填满父容器的高度 */
}

.app-main {
    width: 88%;
    /* padding: 20px; */
    padding: 0;
    background-color: #f8f8f8; /* 主页面背景色 */
    overflow-y: auto; /* 如果主内容区超出高度，显示滚动条 */
    margin-top: 0;
}

li {
    list-style-type: none;
    padding: 0;
    margin: 0;
}

.fa-shekel-sign {
    margin-right: 20px;
}

/* 其他样式 */
</style>
