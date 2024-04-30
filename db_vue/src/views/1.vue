<template>
    <div class="resource-monitor">
        <!-- 这里使用v-for遍历sections，为每个section创建折叠面板 -->
        <div
            v-for="(section, index) in sections"
            :key="section.title"
            class="section"
        >
            <div class="section-header" @click="toggleSection(index)">
                {{ section.title }}
                <!-- 这里显示折叠/展开的图标 -->
                <span class="toggle-icon">
                    {{ section.isCollapsed ? "+" : "-" }}
                </span>
            </div>

            <div v-show="!section.isCollapsed" class="section-content">
                <!-- 这里遍历显示每个section的items -->
                <div
                    v-for="(item, idx) in section.items"
                    :key="idx"
                    class="stat-card"
                >
                    <div class="stat-description">{{ item.description }}</div>
                    <div class="stat-value">{{ item.value[0] }}</div>

                    <chart-card
                        :ref="`chart-${section.title}-${idx}`"
                        :chart-id="`chart-${section.title}-${idx}`"
                        :chart-data="item.value"
                    />

                    <!-- <chart-card
                        :chart-id="`chart-${section.title}-${idx}`"
                        :chart-data="item.value"
                    /> -->
                    <!-- :chart-labels="item.description" -->
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import ChartCard from "../views/ChartCard.vue";
export default {
    components: {
        ChartCard,
    },
    name: "ResourceMonitor",
    data() {
        return {
            titles: [
                { title: "Server Overview", isCollapsed: false },
                { title: "Database Monitor", isCollapsed: false },
                { title: "Command Center", isCollapsed: false },
                { title: "Service Summary", isCollapsed: false },
            ],
            sections: [],
            fetchIntervalId: null,
            intervalCount: 0, // 添加一个计数器
        };
    },
    methods: {
        toggleSection(index) {
            this.sections[index].isCollapsed =
                !this.sections[index].isCollapsed;
        },
        async fetchAndTransformData() {
            const urls = [
                "http://127.0.0.1:8000/monitor/system/",
                // "http://172.31.178.221:8000/monitor/system/",
                "http://127.0.0.1:8000/monitor/network/",
                // "http://172.31.178.221:8000/monitor/network/",
                // 添加其他URLs...
            ];
            try {
                const responses = await Promise.all(
                    urls.map((url) => fetch(url))
                );
                const dataArray = await Promise.all(
                    responses.map((response) => {
                        if (!response.ok) {
                            throw new Error("Network response was not ok");
                        }
                        return response.json();
                    })
                );
                this.sections = dataArray.map((data, index) => ({
                    title: this.titles[index].title,
                    isCollapsed: this.titles[index].isCollapsed,
                    items: Object.keys(data).map((key) => ({
                        value: data[key],
                        description: key.replace(/_/g, " ").toUpperCase(),
                    })),
                }));
            } catch (error) {
                console.error("Error fetching data:", error);
            }

        },
    },
    created() {
        this.fetchAndTransformData();
        // this.fetchIntervalId = setInterval(() => {
        //     if (this.intervalCount < 100) {
        //         this.fetchAndTransformData();
        //         this.intervalCount++; // 每次执行后计数器加1
        //     } else {
        //         clearInterval(this.fetchIntervalId); // 达到最大执行次数，清除定时器
        //     }
        // }, 2000);
    },
    beforeUnmount() {
        if (this.fetchIntervalId) {
            clearInterval(this.fetchIntervalId);
        }
    },
};
</script>


<style scoped>
.resource-monitor {
    background-color: #f8f9fa; /* 页面背景色 */
}

.section {
    margin-bottom: 1rem;
    border: 1px solid #ebedf0;
    border-radius: 0.5rem;
}

.section-header {
    background-color: #93b7c9; /* 大板块背景色 */
    color: #ffffff; /* 大板块字体颜色 */
    padding: 0.5rem 1rem;
    margin: 1%;
    margin-bottom: 0%;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.toggle-icon {
    font-weight: bold;
}

.section-content {
    padding: 1rem;
    background-color: #ffffff; /* 小板块背景色 */
    display: flex; /* 使用flex布局 */
    flex-wrap: wrap; /* 允许内容换行 */
    justify-content: space-between; /* 分散对齐 */
    margin: 1%;
    margin-top: 0%;
    margin-bottom: 0%;
}

.stat-card {
    flex: 1 1 calc(25% - 1rem);
    margin: 0.5rem;
    padding: 0.5rem;
    background: linear-gradient(to right, #bde6f2, #7dafee); /* Your gradient */
    color: #ffffff;
    border-radius: 0.25rem;
    transition: all 0.3s ease;
    cursor: pointer;
    max-width: calc(33.333% - 1rem);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    position: relative; /* Needed for absolute positioning of the pseudo element */
    overflow: hidden; /* Ensures the pseudo element is clipped */
}

.stat-card::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 20px; /* Height of the wave pattern */
    background: url("../assets/logo.png") repeat-x; /* Path to your wave pattern image */
    background-size: cover;
}

.stat-card:hover {
    /* 悬停时的背景色稍微调整为更亮的渐变 */
    background: linear-gradient(to right, #00d2ff, #3a7bd5);
}

.stat-value {
    font-size: 1.5rem; /* 值的字体大小 */
    font-weight: 600;
}

.stat-description {
    font-size: 1rem; /* 描述的字体大小 */
}

@media (max-width: 768px) {
    .stat-card {
        flex-basis: calc(50% - 1rem); /* 中等屏幕下一行显示两个 */
    }
}

@media (max-width: 480px) {
    .stat-card {
        flex-basis: 100%; /* 小屏幕下一行只显示一个 */
    }
}
</style>
