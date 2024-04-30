<template>
    <div class="breadcrumb">
        <ul>
            <li v-for="(breadcrumb, index) in breadcrumbs" :key="index" :class="{ 'active-breadcrumb': breadcrumb.path === $route.path }">
                <router-link :to="breadcrumb.path">{{
                    breadcrumb.name
                }}</router-link>
                <button
                    class="delete-btn"
                    @click="removeBreadcrumb(breadcrumb)"
                >
                    ×
                </button>
                <span v-if="index < breadcrumbs.length - 1"> </span>
            </li>
        </ul>
    </div>
</template>


<script>
import { mapState, mapActions } from "vuex";

export default {
    computed: {
        ...mapState(["breadcrumbs"]), // 确保 'breadcrumbs' 与 Vuex store 中的状态名称匹配
    },
    methods: {
        ...mapActions(["deleteBreadcrumb"]), // 确保 'deleteBreadcrumb' 与 Vuex store 中的动作名称匹配
        removeBreadcrumb(breadcrumb) {
            this.deleteBreadcrumb(breadcrumb);
        },
    },
};
</script>

<style scoped>
.breadcrumb {
    display: flex;
    align-items: center;
    padding-left: 20px; /* 与左边内容对齐 */
    background-color: #dbf0f9; /* 背景颜色与app-header一致 */
    border-bottom: 0px solid #ffffff; /* 添加底部边框线 */
}

/* 覆盖 router-link 的默认样式 */
.breadcrumb a {
    text-decoration: none; /* 去掉下划线 */
    color: inherit; /* 使颜色与周围文本一致 */
}

.breadcrumb li.active-breadcrumb {
    background-color: #f8f8f8; /* 激活时的背景颜色 */
}


/* 当路由链接处于活动状态时的样式 */
.breadcrumb a.router-link-exact-active {
    /* font-weight: bold; 可以设置为加粗或其他样式 */
    background-color: #f8f8f8;
}

/* 移除点击效果样式 */
.breadcrumb a.router-link-exact-active,
.breadcrumb a.router-link-exact-active:hover {
    text-decoration: none; /* 防止悬停时出现下划线 */
}

.breadcrumb ul {
    display: flex;
    padding: 0;
    margin: 0;
    align-items: center; /* 垂直居中对齐列表项 */
}

.breadcrumb li {
    display: flex;
    align-items: center;
    margin-right: 5px; /* 调整列表项之间的距离 */
    background-color: #c6e6f3; /* 每个面包屑项的背景颜色 */
    padding: 5px 10px; /* 面包屑项内边距 */
    border-radius: 4px; /* 圆角边框 */
    border-bottom-left-radius: 0%;
    border-bottom-right-radius: 0%;
    margin-bottom: 0; /* 移除底部外边距 */
}

.breadcrumb li.router-link-exact-active {
    background-color: #ae0909; /* 选中项的背景颜色 */
}

.breadcrumb li button {
    margin-left: 5px; /* 删除按钮与文字的距离 */
    color: #366089; /* 删除按钮的颜色 */
    cursor: pointer;
    border: none;
    background: none;
}

/* 调整删除按钮的样式 */
.breadcrumb button {
    padding: 0;
    display: inline-block;
    background: none;
    border: none;
    cursor: pointer;
}
</style>
