<template>
    <div class="layout">
        <Sidebar />
        <div class="main-content">
            <router-view></router-view>
            <!-- 路由视图，这里会显示ResourceMonitor -->
            <!-- <MyChart :data="data" :options="options" /> -->
        </div>
    </div>
</template>

<script>
import Sidebar from "./components/Sidebar.vue";
// import ResourceMonitor from "./components/ResourceMonitor.vue";
// import MyChart from "./components/MyChart.vue";

export default {
    name: "App",
    components: {
        Sidebar,
        // MyChart,
        // ResourceMonitor
    },
    data() {
        return {
            data: {
                labels: ["January", "February", "March"],
                datasets: [
                    {
                        label: "Data One",
                        backgroundColor: "#f87979",
                        data: [40, 20, 12],
                    },
                ],
            },
            options: null,
        };
    },
};
</script>

<style>
.layout {
    display: flex; /* 使用flex布局 */
    height: 100vh; /* 全屏高度 */
    width: 100vw; /* 全屏宽度 */
}

.main-content {
    flex-grow: 1; /* 主内容区域应占据剩余空间 */
    width: 85%; /* 保证主内容区域占据剩余的85% */
    overflow-y: auto; /* 如果内容过长，允许垂直滚动 */
    background-color: #66696d;
}
</style>
