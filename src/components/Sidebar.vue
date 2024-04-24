<template>
    <a-layout-sider width="200px" class="sidebar">
        <a-menu
            default-selected-keys="['1']"
            mode="inline"
            theme="dark"
            @click="handleMenuItemSelect"
        >
            <!-- Top menu item with larger icon and text -->
            <a-menu-item key="1" class="top-menu-item" >
                <a-icon type="home" />
                <span class="menu-text-large">DB WEB</span>
            </a-menu-item>

            <!-- Other menu items with centered icon and text -->
            <a-menu-item key="2" class="other-menu-item">
                <a-icon type="eye" />
                <span>资源监控</span>
            </a-menu-item>
            <a-menu-item key="3" class="other-menu-item">
                <a-icon type="plus-circle" />
                <span>数据生成</span>
            </a-menu-item>
            <a-menu-item key="4" class="other-menu-item">
                <a-icon type="appstore" />
                <span>数据测试</span>
            </a-menu-item>
            <!-- ...其他菜单项 -->
        </a-menu>
    </a-layout-sider>
</template>

<script>
export default {
    name: "Sidebar",
    methods: {
        handleMenuItemSelect(item) {
            const routeNameMapping = {
                '1': "Home",
                '2': "ResourceMonitor",
                '3': "DataGenerator",
                '4': "DataTest",
                // 添加更多菜单项映射
            };
            const routeName = routeNameMapping[item.key];
            if (routeName) {
                this.$router.push({ name: routeName }).catch((err) => {
                    if (err.name !== "NavigationDuplicated") {
                        throw err;
                    }
                    // 如果是重复导航，可能只需要记录或者忽略
                });
            }
        },
    },
};
</script>

<style scoped>


.layout {
    display: flex; /* 使用flex布局 */
    height: 100vh; /* 全屏高度 */
    overflow: hidden; /* 防止滚动条出现 */
}

.sidebar {
    width: 15%; /* 侧边栏宽度占15% */
    height: 100vh; /* 侧边栏高度 */
    background-color: #515a6e; /* 侧边栏背景颜色 */
    flex-shrink: 0; /* 防止侧边栏被压缩 */
    display: flex; /* 使用flex布局以便内部元素居中 */
    flex-direction: column; /* 子元素垂直排列 */
}

.menu-item-content {
    display: flex;
    align-items: center;
    width: 100%;
    height: 100%; /* Set the height to 100% for the content to fill the MenuItem */
    padding: 10px;
    box-sizing: border-box;
}

.top-menu-item .menu-item-content {
    justify-content: center; /* Center align content for the top menu item */
    font-size: 1.5em; /* Enlarge text for the top menu item */
}

.menu-text-large {
    margin-left: 15px; /* Add some space between the icon and text */
    font-size: 20px; /* Larger font size for the top menu item text */
}

/* Adjust the size of the icons */
.top-menu-item .ivu-icon {
    font-size: 35px; /* Larger icon for the top menu item */
}

.other-menu-item .menu-item-content {
    justify-content: flex-start; /* Left align content for other menu items */
}

/* Keep the icon sizes for other menu items unchanged */
.other-menu-item .ivu-icon {
    font-size: 20px;
}

.ivu-menu-item .ivu-icon {
    margin-right: 15px; /* 图标与文字之间的间距 */
}

/* Add other styles here as needed */
</style>
