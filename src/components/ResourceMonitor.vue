<template>
    <div class="dashboard">
        <a-collapse v-model="activeKey" accordion>
            <a-collapse-panel
                v-for="(section, index) in sections"
                :key="index"
                :header="section.title"
                :name="index.toString()"
            >
                <div
                    v-for="item in section.items"
                    :key="item.description"
                    class="stat-card"
                >
                    <a-card>
                        <template #title>
                            <div class="stat-value">{{ item.value }}</div>
                        </template>
                        <div class="stat-description">{{ item.description }}</div>
                    </a-card>
                </div>
            </a-collapse-panel>
        </a-collapse>
    </div>
</template>


<script>
// import MyChart from "./MyChart.vue";

export default {
    components: {
        // "my-chart": MyChart,
    },
    name: "Dashboard",
    data() {
        return {
            titles: [
                {
                    title: "Server Overview",
                    isCollapsed: false,
                },
                {
                    title: "Database Monitor",
                    isCollapsed: false,
                },
                {
                    title: "Command Center",
                    isCollapsed: false,
                },
                {
                    title: "Command Center",
                    isCollapsed: false,
                },
            ],
            // 新版获取后端的数据，存放至sections。
            //在Vue组件的 created 钩子中添加一个方法来从后端获取数据，并用这些数据更新你的 sections 数组
            sections: [],
            activeKey: ['0'], // 默认展开第一个section
        };
    },
    created() {
        this.fetchAndTransformData();
    },
    methods: {
        toggleSection(index) {
            this.sections[index].isCollapsed =
                !this.sections[index].isCollapsed;
        },
        // fetch 后发现前端不呈现了，其实也正常，数据格式完全不一样，你怎么呈现呢？
        // fetchData() {
        //     console.log("fetchData!!!!!");
        //     fetch("http://127.0.0.1:8000/monitor/resources/")
        //         .then((response) => response.json())
        //         .then((data) => {
        //             // 假设你的数据是一个数组，你可以将其直接分配给sections
        //             // 如果数据结构不同，你可能需要对其进行适当的转换
        //             this.sections = data.map((item) => {
        //                 return {
        //                     title: item.name,
        //                     isCollapsed: false,
        //                     items: [
        //                         {
        //                             value: item.value.toString(),
        //                             description: item.description,
        //                         },
        //                         {
        //                             value: item.value.toString(),
        //                             description: item.description,
        //                         },
        //                         {
        //                             value: item.value.toString(),
        //                             description: item.description,
        //                         },
        //                         {
        //                             value: item.value.toString(),
        //                             description: item.description,
        //                         },
        //                         {
        //                             value: item.value.toString(),
        //                             description: item.description,
        //                         },
        //                     ],
        //                 };
        //             });
        //         })
        //         .catch((error) => console.error("Error:", error));
        // },
        fetchAndTransformData() {
            const urls = [
                "http://127.0.0.1:8000/monitor/network/",
                // "http://127.0.0.1:8000/monitor/application/", // 假设这个端点是故障的
                // "http://127.0.0.1:8000/monitor/database/",
                "http://127.0.0.1:8000/monitor/system/",
            ];

            const transformData = (title, data) => {
                const items = [];
                for (const key in data) {
                    if (
                        data.hasOwnProperty(key) &&
                        typeof data[key] !== "object"
                    ) {
                        items.push({
                            value: data[key],
                            description: key.split("_").join(" ").toUpperCase(),
                        });
                    }
                }
                return {
                    title: title.title,
                    isCollapsed: false,
                    items,
                };
            };

            Promise.all(
                urls.map((url, index) =>
                    fetch(url)
                        .then((response) => {
                            if (!response.ok) {
                                throw new Error("Network response was not ok");
                            }
                            return response.json();
                        })
                        .then((data) => {
                            return transformData(this.titles[index], data);
                        })
                        .catch((error) => {
                            console.error("Error fetching data:", error);
                            return {
                                // 返回一个错误section，或者你可以选择不返回任何东西
                                title: this.titles[index].title,
                                isCollapsed: false,
                                items: [
                                    {
                                        value: "Error",
                                        description: "Could not fetch data",
                                    },
                                ],
                            };
                        })
                )
            )
                .then((sections) => {
                    this.sections = sections.filter(
                        (section) => section.items.length > 0
                    ); // 只保留包含项目的部分
                })
                .catch((error) => {
                    console.error("Error fetching data:", error);
                });
        },
        
    },
};
</script>

<style scoped>
.dashboard {
    background-color: #1a1a1a; /* New background color */
}

.dashboard-section + .dashboard-section {
    margin-top: 20px;
}

.section-header {
    background-color: #333;
    color: white;
    padding: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.toggle-button {
    background: none;
    border: none;
    color: white;
    cursor: pointer;
}

.section-content {
    padding: 10px;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.stat-card {
    flex: 1;
    min-width: calc(33% - 20px); /* Adjust card width here */
    background-color: #252525; /* Card background color */
    color: white; /* Text color */
    padding: 20px;
    border-radius: 4px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.stat-value {
    font-size: 20px;
    font-weight: 500;
}

.stat-description {
    font-size: 14px;
    opacity: 0.7;
}

@media (max-width: 768px) {
    .stat-card {
        min-width: 100%;
    }
}
</style>