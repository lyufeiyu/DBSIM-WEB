<!-- DataTest.vue -->
<template>
    <div class="data-test-container">
        <!-- X列：原始数据操作栏 -->
        <div class="data-operation original-data-operation">
            <h2>原始数据操作栏</h2>
            <!-- 数据集列表区 -->
            <div class="data-section dataset-list-section">
                <div class="section-title">后台数据集列表</div>
                <select
                    v-model="selectedDatasetOriginal"
                    class="dataset-select"
                >
                    <option disabled value="">请选择一个原始数据集</option>
                    <option
                        v-for="dataset in datasets"
                        :key="dataset"
                        :value="dataset"
                    >
                        {{ dataset }}
                    </option>
                </select>

                <div class="section-title">数据库类型</div>
                <select v-model="selectedDbTypeOriginal" class="dataset-select">
                    <option disabled value="">请选择数据库类型</option>
                    <option
                        v-for="dbType in dbTypes"
                        :key="dbType"
                        :value="dbType"
                    >
                        {{ dbType }}
                    </option>
                </select>

                <button
                    :disabled="!isOriginalDataButtonActive"
                    @click="importDataOriginal"
                >
                    将选定数据集导入选定数据库
                </button>
                <button
                    :disabled="!selectedDatasetOriginal"
                    @click="clearDatasetOriginal"
                >
                    清除选定数据集
                </button>
            </div>

            <div class="data-section sql-query-section">
                <div class="section-title">SQL查询输入栏</div>
                <textarea
                    v-model="sqlQueryOriginal"
                    placeholder="可在此处写入你的sql代码"
                    class="sql-textarea"
                ></textarea>
                <div class="section-title">或：选择.sql文件</div>
                <input
                    type="file"
                    @change="handleFileUploadOriginal"
                    accept=".sql"
                />
                <button
                    :disabled="!canRunQueryOriginal"
                    @click="runQueryOriginal"
                    class="sqlButton-1"
                >
                    查询
                </button>
            </div>
        </div>

        <!-- Y列：中间列 -->
        <div class="middle-column">
            <!-- Y列上部分：指标视图区 -->
            <div class="indicator-view-section">
                <h2>指标视图区</h2>
                <!-- 展示性能指标数据 -->
                <div
                    v-if="Object.keys(responses).length > 0"
                    class="response-table"
                >
                    <table>
                        <thead>
                            <tr>
                                <th>指标</th>
                                <th
                                    v-for="(value, key) in responses"
                                    :key="key"
                                >
                                    {{ key }}
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="(metrics, metric) in responses[
                                    Object.keys(responses)[0]
                                ]"
                                :key="metric"
                            >
                                <td>{{ metric }}</td>
                                <td
                                    v-for="(value, key) in responses"
                                    :key="key"
                                >
                                    {{ responses[key][metric] }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <data-test-chart
                    v-if="chartData && chartData.datasets.length > 0"
                    :chart-data="chartData"
                    :options="chartOptions"
                />
            </div>
            <!-- Y列下部分：操作监控区 -->
            <div class="operation-monitor-section">
                <!-- 操作监控内容 -->
            </div>
        </div>

        <!-- Z列：生成数据操作栏 -->
        <div class="data-operation generated-data-operation">
            <h2>生成数据操作栏</h2>
            <!-- 数据集列表区 -->
            <div class="data-section dataset-list-section">
                <div class="section-title">后台数据集列表</div>
                <select
                    v-model="selectedDatasetGenerated"
                    class="dataset-select"
                >
                    <option disabled value="">请选择一个生成数据集</option>
                    <option
                        v-for="dataset in datasets"
                        :key="dataset"
                        :value="dataset"
                    >
                        {{ dataset }}
                    </option>
                </select>

                <div class="section-title">数据库类型</div>
                <select
                    v-model="selectedDbTypeGenerated"
                    class="dataset-select"
                >
                    <option disabled value="">请选择数据库类型</option>
                    <option
                        v-for="dbType in dbTypes"
                        :key="dbType"
                        :value="dbType"
                    >
                        {{ dbType }}
                    </option>
                </select>

                <button
                    :disabled="!isGeneratedDataButtonActive"
                    @click="importDataGenerated"
                >
                    将选定数据集导入选定数据库
                </button>
                <button
                    :disabled="!selectedDatasetGenerated"
                    @click="clearDatasetGenerated"
                >
                    清除选定数据集
                </button>
            </div>

            <div class="data-section sql-query-section">
                <div class="section-title">SQL查询输入栏</div>
                <textarea
                    v-model="sqlQueryGenerated"
                    placeholder="可在此处写入你的sql代码"
                    class="sql-textarea"
                ></textarea>
                <div class="section-title">或：选择.sql文件</div>
                <input
                    type="file"
                    @change="handleFileUploadGenerated"
                    accept=".sql"
                />
                <button
                    :disabled="!canRunQueryGenerated"
                    @click="runQueryGenerated"
                >
                    查询
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import DataTestChart from "./DataTestChart.vue";

export default {
    components: {
        DataTestChart,
    },
    data() {
        return {
            datasets: [], // 来自后端API的数据集列表
            selectedDatasetOriginal: "", // 原始数据操作栏选中的数据集
            selectedDbTypeOriginal: "", // 原始数据操作栏选中的数据库类型
            sqlQueryOriginal: "", // 原始数据操作栏SQL查询
            selectedFileOriginal: null, // Added for the file upload
            responses: {},

            selectedDatasetGenerated: "", // 生成数据操作栏选中的数据集
            selectedDbTypeGenerated: "", // 生成数据操作栏选中的数据库类型
            sqlQueryGenerated: "", // 生成数据操作栏SQL查询
            selectedFileGenerated: null, // Added for the file upload

            // 图表属性
            chartData: {
                labels: [],
                datasets: [],
            },
            chartOptions: {
                responsive: true,
                maintainAspectRatio: false,
                // ... 更多的图表选项 ...
            },
        };
    },
    watch: {
        "responses.Response_Times_Percentiles": function (newVal) {
            this.chartData = {
                labels: Object.keys(newVal),
                datasets: [
                    {
                        label: "Response Times Percentiles",
                        backgroundColor: "#f87979",
                        data: Object.values(newVal),
                    },
                ],
            };
        },
    },
    computed: {
        // 计算属性来判断按钮是否激活
        // 如果你有生成数据操作栏的数据库类型选择也是如此
        isOriginalDataButtonActive() {
            return this.selectedDatasetOriginal && this.selectedDbTypeOriginal;
        },
        isGeneratedDataButtonActive() {
            return (
                this.selectedDatasetGenerated && this.selectedDbTypeGenerated
            );
        },

        canRunQueryOriginal() {
            return this.sqlQueryOriginal || this.selectedFileOriginal; // Check if text is entered or a file is selected
        },
        canRunQueryGenerated() {
            return this.sqlQueryGenerated || this.selectedFileGenerated; // Check if text is entered or a file is selected
        },
    },
    methods: {
        handleFileUploadOriginal(event) {
            const files = event.target.files;
            if (files.length > 0) {
                this.selectedFileOriginal = files[0]; // Set the first file as selected
            }
        },
        handleFileUploadGenerated(event) {
            const files = event.target.files;
            if (files.length > 0) {
                this.selectedFileGenerated = files[0]; // Set the first file as selected
            }
        },

        updateResponsesData(data) {
            this.responses.TPS = data.TPS;
            this.responses.QPS = data.QPS;
            this.responses.Response_Times_Percentiles =
                data.Response_Times_Percentiles;
        },

        // 原始数据操作栏的方法
        importDataOriginal() {
            // 调用API将数据集导入数据库
            const apiUrl = "http://172.31.178.221:8000/dataTest/import-database/";
            const formData = new FormData();
            console.log(this.selectedDatasetOriginal);
            console.log(this.selectedDbTypeOriginal);
            formData.append("dataset_name", this.selectedDatasetOriginal); // or this.selectedDatasetGenerated
            formData.append("database_type", this.selectedDbTypeOriginal); // currently hardcoded, could be dynamic

            axios
                .post(apiUrl, formData)
                .then((response) => {
                    // handle success
                    console.log(response.data.message);
                    // You might want to do something in your UI to show success
                })
                .catch((error) => {
                    // Check if the response object exists
                    if (error.response && error.response.data) {
                        // Handle error with a response data object
                        console.error(
                            "Error importing data:",
                            error.response.data.error || error.response.data
                        );
                    } else if (error.request) {
                        // The request was made but no response was received
                        console.error(
                            "Error importing data: No response received",
                            error.request
                        );
                    } else {
                        // Something happened in setting up the request that triggered an Error
                        console.error("Error importing data:", error.message);
                    }
                    // Log the full error if needed for debugging
                    console.error(error);
                });
        },
        clearDatasetOriginal() {
            // 调用API清除数据集
            this.exampleApiCall("clear", this.selectedDatasetOriginal);
        },
        runQueryOriginal() {
            // 创建FormData对象来发送文件数据
            const formData = new FormData();
            formData.append("sql_file", this.selectedFileOriginal);
            formData.append("db_type", this.selectedDbTypeOriginal);

            // 发送请求到您的Django后端
            axios
                .post("http://172.31.178.221:8000/dataTest/run-query/", formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                })
                .then((response) => {
                    // 处理成功的响应
                    console.log(response);
                    // 更新图表数据
                    this.chartData = {
                        labels: Object.keys(
                            response.data.Response_Times_Percentiles
                        ),
                        datasets: [
                            {
                                label: "Response Times Percentiles",
                                backgroundColor: "rgba(255, 99, 132, 0.2)",
                                borderColor: "rgba(255, 99, 132, 1)",
                                borderWidth: 1,
                                hoverBackgroundColor: "rgba(255, 99, 132, 0.4)",
                                hoverBorderColor: "rgba(255, 99, 132, 1)",
                                data: Object.values(
                                    response.data.Response_Times_Percentiles
                                ),
                            },
                        ],
                    };
                    // console.log(response.data.message);
                    const dbName = this.selectedDbTypeOriginal; // 当前选中的数据库名称
                    // 初始化或更新当前数据库的指标数据
                    if (!this.responses[dbName]) {
                        this.responses[dbName] = {
                            TPS: response.data.TPS,
                            QPS: response.data.QPS,
                            ...response.data.Response_Times_Percentiles,
                        };
                    } else {
                        this.responses[dbName].TPS = response.data.TPS;
                        this.responses[dbName].QPS = response.data.QPS;
                        Object.assign(
                            this.responses[dbName],
                            response.data.Response_Times_Percentiles
                        );
                    }

                    // this.responses.TPS = response.data.TPS;
                    // this.responses.QPS = response.data.QPS;
                    // this.responses.Response_Times_Percentiles =
                    //     response.data.Response_Times_Percentiles;
                    // console.log(this.responses.TPS);
                    // console.log(this.responses.QPS);
                    // console.log(this.responses.Response_Times_Percentiles);
                })
                .catch((error) => {
                    // 处理错误
                    console.error("Error running query:", error);
                });
        },
        // 生成数据操作栏的方法
        importDataGenerated() {
            // 调用API导入数据
            this.exampleApiCall("import", this.selectedDatasetGenerated);
        },
        clearDatasetGenerated() {
            // 调用API清除数据集
            this.exampleApiCall("clear", this.selectedDatasetGenerated);
        },
        runQueryGenerated() {
            // 执行SQL查询
            this.exampleApiCall("query", this.sqlQueryGenerated);
        },
        // 示例API调用方法
        exampleApiCall(action, data) {
            console.log(`API调用: ${action}, 数据: ${data}`);
            // 这里可以替换为实际的API调用代码
        },
    },
    mounted() {
        // 在这里可以调用API获取数据集列表
        this.datasets = ["IMDB","property"]; // 示例数据
        this.dbTypes = ["MySQL", "PostgreSQL"]; // 示例数据库类型
    },
};
</script>

<style scoped>
.data-test-container {
    display: flex;
    height: 100vh;
    background-color: #ffffff;
    margin: 0;
    padding: 10px;
}

.data-operation,
.middle-column {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 20px;
    gap: 20px;
    border: 1px solid #eaeaea;
    border-radius: 4px;
    background-color: #edf4fa;
}

.middle-column {
    display: flex;
    flex-direction: column;
}

.indicator-view-section {
    flex: 8;
    /* 指标视图区的样式 */
    border: 2px solid #ccc; /* 临时样式，需按需修改 */
    margin-bottom: 20px; /* 临时样式，需按需修改 */
}

.operation-monitor-section {
    flex: 2;
    /* 操作监控区的样式 */
    border: 2px solid #ccc; /* 临时样式，需按需修改 */
}

/* 其余样式保持原样或按需修改 */
.data-section {
    margin-bottom: 10px; /* 为了和其他部分保持一致 */
}

.section-title {
    margin-bottom: 5px;
    text-align: left; /* 靠左对齐 */
    /* margin-left: 5%; */
}

.dataset-select,
.sql-textarea,
button {
    width: 95%;
    padding: 10px;
    margin-bottom: 10px;
    margin-top: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.sql-textarea {
    width: 90%;
}

button {
    background-color: #5b9bd5;
    color: white;
    cursor: pointer;
}

button:hover {
    background-color: #4a8cc7;
}

button:disabled {
    background-color: #aaa;
    cursor: default;
}

/* Add your file input styles here */
input[type="file"] {
    width: 95%;
    padding: 10px;
    margin-top: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.response-table {
    margin: 0 auto; /* 居中表格 */
    display: flex;
    justify-content: center;
    align-items: center;
}

table {
    width: 100%; /* 表格宽度为容器的100% */
    border-collapse: collapse; /* 移除表格之间的间距 */
    text-align: center; /* 文字居中 */
}

th,
td {
    text-align: center; /* 单元格文字居中 */
    border: 1px solid #ddd; /* 单元格边框 */
    padding: 5px; /* 单元格内边距 */
}

thead {
    background-color: #f4f4f4; /* 表头背景色 */
}

tr:nth-child(even) {
    background-color: #f9f9f9; /* 交替行背景色 */
}

th {
    text-align: center; /* 表头文字居中 */
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
    background-color: #a7d1fb;
    color: white;
}

/* 响应式布局调整 */
@media (max-width: 768px) {
    .data-test-container {
        flex-direction: column;
    }
    .data-operation,
    .middle-column {
        width: 100%;
        margin-bottom: 10px;
    }
}
</style>