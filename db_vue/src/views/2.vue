<template>
    <div class="data-generator">
        <!-- 左边栏：逻辑操作区 -->
        <div class="left-panel">
            <!-- 上传文件按钮 -->
            <!-- 自定义文件上传按钮 -->
            <h2>文件选择</h2>
            <div @click="triggerFileUpload" class="file-upload-placeholder">
                {{ fileInputPlaceholder }}
                <input
                    type="file"
                    ref="fileInput"
                    multiple
                    @change="handleFileUpload"
                    accept=".csv"
                    style="display: none"
                />
            </div>

            <div @click="triggerFileUpload2" class="file-upload-placeholder">
                {{ fileInputPlaceholder2 }}
                <input
                    type="file"
                    ref="fileInput2"
                    @change="handleSchemaUpload"
                    accept=".txt"
                    style="display: none"
                />
            </div>

            <!-- <input
                type="file"
                multiple
                @change="handleFileUpload"
                accept=".csv"
                placeholder="aaaaaaaaaaaaa"
            /> -->

            <!-- 已上传文件列表 -->
            <div class="uploaded-files">
                <div
                    v-for="file in files"
                    :key="file.name"
                    @click="selectFile(file)"
                >
                    {{ file.name }}
                </div>
                <!-- 清除内容查看区按钮 -->
                <button @click="clearContent">清除选择文件</button>
            </div>

            <!-- 参数配置区 -->
            <div class="parameters-form">
                <h2>参数配置</h2>
                <span
                    v-if="!params.param1"
                    style="color: red; margin-right: 2px"
                >
                    *必填
                </span>
                <span>dataset_name:</span>
                <input v-model="params.dataset_name" type="text" required />

                <span>coeffi:</span>
                <input
                    v-model="params.coeffi"
                    type="number"
                    min="0"
                    max="1"
                    step="0.01"
                />

                <span>scale_factor:</span>
                <input v-model="params.scale_factor" type="number" />

                <span>cluster_per_col:</span>
                <input
                    v-model="params.cluster_per_col"
                    type="number"
                    min="2"
                    max="10"
                    step="1"
                />

                <span>privacy_budget:</span>
                <input
                    v-model="params.privacy_budget"
                    type="number"
                    min="0.1"
                    max="10"
                    step="0.1"
                />
                <!-- placeholder="aaaaaaa" -->
                <!-- 可以继续添加其他参数的输入框 -->
            </div>

            <!-- 生成数据按钮 -->
            <!-- 生成数据按钮 -->
            <button
                @click="generateData"
                :class="{ 'button-disabled': !params.param1 }"
                :disabled="!params.param1"
            >
                生成数据
            </button>

            <!-- SQL文件上传按钮 -->
            <h2>SQL文件上传</h2>
            <div @click="triggerSQLFileUpload3" class="file-upload-placeholder">
                {{ sqlFileInputPlaceholder }}
                <input
                    type="file"
                    ref="sqlFileInput"
                    @change="handleSQLFileUpload3"
                    accept=".sql"
                    style="display: none"
                />
            </div>

            <!-- 展示上传的SQL文件 -->
            <div class="uploaded-files">
                <div
                    v-for="sqlFile in sqlFiles"
                    :key="sqlFile.name"
                    @click="selectFile(sqlFile)"
                >
                    {{ sqlFile.name }}
                </div>
                <!-- 清除内容查看区按钮 -->
                <button @click="clearContent">清除选择文件</button>
            </div>

            <!-- 生成负载按钮 -->
            <button @click="generateLoad">生成负载</button>

            <!-- 历史生成文件区 -->
            <div class="generated-files">
                <h2>历史生成文件</h2>
                <ul>
                    <li v-for="file in generatedFiles" :key="file.name">
                        <a href="#" @click.prevent="downloadFile(file)">
                            {{ file.name }}
                        </a>
                    </li>
                </ul>
            </div>
        </div>

        <!-- 右边栏：内容呈现区和实时监控区 -->
        <div class="right-panel">
            <!-- 内容呈现区 -->
            <!-- 文件查看区 -->
            <div class="content-display">
                <h2>文件查看区</h2>
                <div v-if="fileType === 'csv'">
                    <table v-if="tableHeaders.length > 0">
                        <thead>
                            <tr>
                                <th
                                    v-for="(header, index) in tableHeaders"
                                    :key="index"
                                >
                                    {{ header }}
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="(row, rowIndex) in displayedRows"
                                :key="rowIndex"
                            >
                                <td
                                    v-for="(cell, cellIndex) in row"
                                    :key="cellIndex"
                                >
                                    {{ cell }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <div v-if="!fullFileContentArray.length">
                        请选择或上传文件以查看内容
                    </div>
                    <!-- 分页控制 -->
                    <div
                        class="pagination-controls"
                        v-if="fullFileContentArray.length > 0 && totalPages > 1"
                    >
                        <button
                            @click="changePage(currentPage - 1)"
                            :disabled="currentPage <= 1"
                        >
                            上一页
                        </button>
                        <span>Page {{ currentPage }} of {{ totalPages }}</span>
                        <button
                            @click="changePage(currentPage + 1)"
                            :disabled="currentPage >= totalPages"
                        >
                            下一页
                        </button>
                    </div>
                </div>
                <div v-else-if="fileType === 'sql' || fileType === 'txt'">
                    <pre>{{ selectedFileContent }}</pre>
                </div>
            </div>

            <!-- 实时监控区 -->
            <div class="realtime-monitor">
                <h2>数据生成监控区</h2>
                <p v-if="monitoringData > 2">正在生成数据...请耐心等待...</p>
                <p v-else-if="monitoringData == 1">
                    数据生成完毕！可在历史生成文件中下载！
                </p>
                <p v-else-if="monitoringData == 2">
                    您上传的文件内容或格式不正确，请重新上传文件，已为您清空已上传文件！
                </p>
                <p v-else>数据生成的反馈将显示在此处</p>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            files: [], // 存储上传的CSV文件
            fileType: "",
            selectedFileContent: "", // 存储选中文件的内容
            monitoringData: null, // 模拟监控数据
            generatedFiles: [], // 用来存储生成的文件信息和下载链接
            params: {
                // 存储用户设置的参数
                dataset_name: "",
                scale_factor: 1,
                coeffi: 0,
                privacy_budget: 0.1,
                cluster_per_col: 2,
                // 添加更多参数
            },
            fileInputPlaceholder: "请选择一或多个格式为csv的文件", // 默认的占位符文本
            fileInputPlaceholder2: "请选择格式为txt的schema文件", // 默认的占位符文本
            responseData: null, // 用来存储后端响应的数据

            // 分页属性
            fullFileContentArray: [], // 存储文件的完整内容
            currentPage: 1,
            perPage: 100, // 你可以设置每页想显示的行数
            totalPages: 0,
            tableHeaders: [], // 存储表头
            displayedRows: [], // 当前页面显示的行

            // sql文件属性
            sqlFiles: [], // 存储上传的SQL文件
            sqlFileInputPlaceholder: "请选择.sql文件", // SQL文件上传占位符
        };
    },
    computed: {},
    created() {
        this.fetchHistoryFiles();
    },
    methods: {
        triggerFileUpload() {
            // 触发原生的文件输入
            this.$refs.fileInput.click();
        },
        triggerFileUpload2() {
            // 触发原生的文件输入
            this.$refs.fileInput2.click();
        },
        triggerSQLFileUpload3() {
            // 触发SQL文件上传
            this.$refs.sqlFileInput.click();
        },
        handleFileUpload(event) {
            // 上传多个CSV文件
            // const files = event.target.files;
            // if (files) {
            //     for (let file of files) {
            //         this.files.push(file);
            //         console.log("File added:", file.name);
            //     }
            //     if (files.length > 0) {
            //         this.selectFile(files[0]); // 只处理第一个文件
            //     }
            // }
            const newFiles = [...event.target.files];
            this.files = [...this.files, ...newFiles];
            if (newFiles.length > 0) {
                this.selectFile(newFiles[0]);
            }
            // 创建 FormData 对象   你别急，后面再上传也是可以的
            // let formData = new FormData();
            // for (let file of this.files) {
            //     formData.append("myfile", file);

            //     // 发送 POST 请求到 Django 服务器
            //     axios
            //         .post(
            //             "http://172.31.178.221:8000/generator/upload/",
            //             formData,
            //             {
            //                 headers: {
            //                     "Content-Type": "multipart/form-data",
            //                 },
            //             }
            //         )
            //         .then((response) => {
            //             // 文件上传成功
            //             console.log("Uploaded:", response.data);
            //             // 你可能想把这个文件加到生成的文件列表中
            //             // this.generatedFiles.push({
            //             //     name: file.name,
            //             //     // 这里你需要处理响应数据以获得正确的下载 URL
            //             //     downloadUrl: response.data.uploaded_file_url,
            //             // });
            //         })
            //         .catch((error) => {
            //             // 文件上传失败
            //             console.error("Upload failed:", error);
            //         });
            // }
        },
        handleSchemaUpload(event) {
            const newFile = event.target.files[0];
            if (newFile) {
                this.files = [...this.files, newFile];
            }
            // const file = event.target.files[0];
            // console.log("File added:", file.name);
            // this.files.push(file);
            // if (file) {    //你也别急，后面再上传
            //     // 确保是txt文件
            //     // 创建 FormData 对象并添加文件
            //     let formData = new FormData();
            //     formData.append("myfile", file);

            //     // 发送 POST 请求到服务器
            //     axios
            //         .post(
            //             "http://172.31.178.221:8000/generator/upload/",
            //             formData,
            //             {
            //                 headers: {
            //                     "Content-Type": "multipart/form-data",
            //                 },
            //             }
            //         )
            //         .then((response) => {
            //             // 文件上传成功，可以在这里处理响应
            //             console.log("Schema uploaded:", response.data);
            //         })
            //         .catch((error) => {
            //             // 文件上传失败
            //             console.error("Schema upload failed:", error);
            //         });
            // } else {
            //     console.error("Please upload a valid .txt file");
            // }
        },
        handleSQLFileUpload3(event) {
            // 处理SQL文件上传
            const sqlFile = event.target.files[0];
            if (sqlFile) {
                this.sqlFiles.push(sqlFile);
                console.log("SQL File added:", sqlFile.name);
                // Implement the file upload logic here or save the file object for later processing
            } else {
                console.error("Please upload a valid .sql file");
            }
        },
        fetchHistoryFiles() {
            // 获取历史文件列表
            axios
                // .get("http://172.31.178.221:8000/generator/history-files/")
                .get("http://127.0.0.1:8000/generator/history-files/")
                .then((response) => {
                    console.log("Received files:", response.data);
                    // 更新generatedFiles以反映从后端接收到的文件
                    this.generatedFiles = response.data.map((file) => {
                        return {
                            name: file.name,
                            download_url: file.download_url, // 确保后端提供的是完整的下载URL
                        };
                    });
                })
                .catch((error) => {
                    console.error("Error fetching history files:", error);
                });
        },
        downloadFile(file) {
            // 下载文件
            // 确保download_url存在
            // download_url="http://localhost:8000"+download_url
            // if (!file.download_url) {
            //     console.error("Download URL is missing");
            //     return; // 直接返回，避免进一步执行
            // }

            // 如果download_url是一个有效的URL
            // const url = "http://127.0.0.1:80" + file.download_url;
            const url = "http://172.31.178.221:80" + file.download_url;
            console.log("Downloading file:", url);

            // file.download_url.startsWith("http")
            //     ? file.download_url
            //     : `${window.location.origin}${file.download_url}`;

            axios({
                url: url,
                method: "GET",
                responseType: "blob", // 重要：设置响应类型为blob处理文件
            })
                .then((response) => {
                    const blob = new Blob([response.data], {
                        type: "application/octet-stream",
                    });
                    const link = document.createElement("a");
                    link.href = window.URL.createObjectURL(blob);
                    link.setAttribute("download", file.name);
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                })
                .catch((error) => {
                    console.error("Download error:", error);
                });
        },
        generateLoad() {
            // 触发后端API逻辑
            if (this.sqlFiles.length > 0) {
                let formData = new FormData();
                formData.append("sql_file", this.sqlFiles[0]);

                axios
                    .post(
                        "http://127.0.0.1:8000/generator/generate-sql/",
                        formData,
                        {
                            headers: {
                                "Content-Type": "multipart/form-data",
                            },
                        }
                    )
                    .then((response) => {
                        console.log(
                            "Load generation triggered:",
                            response.data
                        );
                        // Handle successful response
                        // You may want to fetch the history files again to update the list
                        this.fetchHistoryFiles();
                    })
                    .catch((error) => {
                        console.error(
                            "Error triggering load generation:",
                            error
                        );
                    });
            } else {
                console.error("No SQL file available for upload.");
            }
        },
        generateData() {
            this.monitoringData = 3;
            // 这里构造包含参数的FormData
            let formData = new FormData();
            for (let key in this.params) {
                formData.append(key, this.params[key]);
            }

            //如果文件在上面已经发送了，怎么让多次寻文件位置正确呢？
            // 假设我们要把文件也一起发送
            this.files.forEach((file) => {
                formData.append("files", file);
            });

            this.params.param1 = "";
            // 发送 POST 请求到服务器以生成数据
            axios
                .post(
                    "http://127.0.0.1:8000/generator/generate-data/",
                    formData,
                    {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        },
                    }
                )
                .then((response) => {
                    // 处理生成数据的响应
                    console.log("Data generation initiated:", response.data);
                    this.responseData = response.data; // 将响应数据保存到数据属性中
                    this.monitoringData = response.data.message;
                    if (this.monitoringData == 2) {
                        this.clearContent();
                    } else if (this.monitoringData == 1) {
                        this.fetchHistoryFiles(); // 获取历史文件列表
                    }
                    // console.log("Data generation initiated:", response.data);
                })
                .catch((error) => {
                    // 数据生成请求clearContent
                    console.error("Data generation failed:", error);
                });

            // 生成数据

            // 模拟数据生成过程
            // this.monitoringData = 0; // 初始化监控数据
            // const interval = setInterval(() => {
            //     this.monitoringData += 100; // 假设每次增加100行
            //     if (this.monitoringData >= 1000) {
            //         // 当达到1000行时停止
            //         clearInterval(interval);
            //         this.monitoringData = "完成";
            //         // 假设生成的文件信息
            //         this.generatedFiles.push({
            //             name: "data-" + new Date().toISOString() + ".csv",
            //             downloadUrl: "path/to/generated/file.csv", // 这里应该是生成文件的下载链接
            //         });
            //     }
            // }, 1000); // 每1秒更新一次
        },
        // selectFile(file) {
        //     // 选择文件，读取内容
        //     // 使用 FileReader 读取选中文件的内容
        //     const reader = new FileReader();
        //     reader.onload = (e) => {
        //         this.selectedFileContent = e.target.result; // 将文件内容赋值到变量
        //     };
        //     reader.readAsText(file);
        // },
        selectFile(file) {
            const fileExtension = file.name.split(".").pop();
            console.log("File extension:", fileExtension);
            this.fileType = fileExtension;
            // 使用 FileReader 读取选中文件的内容

            const reader = new FileReader();
            reader.onload = (e) => {
                if (fileExtension === "csv") {
                    const fileContentArray = e.target.result.split("\n");
                    // 更新表头
                    this.tableHeaders = fileContentArray[0].split(",");
                    // 存储完整的文件内容以供分页使用
                    const dataRows = fileContentArray.slice(1);
                    this.fullFileContentArray = dataRows;
                    // 计算总页数
                    this.totalPages = Math.ceil(dataRows.length / this.perPage);
                    // 更新当前显示的行
                    this.updateDisplayedRows(
                        this.fullFileContentArray,
                        this.currentPage
                    );
                } else {
                    // Directly set the content for SQL and TXT files
                    this.selectedFileContent = e.target.result;
                }
            };
            reader.onerror = (e) => {
                console.error("FileReader error", e);
            };
            if (file instanceof Blob) {
                reader.readAsText(file);
            } else {
                console.error("The provided file is not a Blob");
            }
        },

        updateDisplayedRows(dataRows, page) {
            const startIndex = (page - 1) * this.perPage;
            const endIndex = startIndex + this.perPage;
            this.displayedRows = dataRows
                .slice(startIndex, endIndex)
                .map((row) => row.split(","));
        },

        changePage(newPage) {
            if (newPage >= 1 && newPage <= this.totalPages) {
                this.currentPage = newPage;
                this.updateDisplayedRows(this.fullFileContentArray, newPage);
            }
        },

        clearContent() {
            // 清除选择的文件和相关内容
            this.selectedFileContent = "";
            this.tableHeaders = [];
            this.displayedRows = [];
            this.currentPage = 1;
            this.totalPages = 0;
            // 清空上传文件列表
            this.files = [];

            // 重置文件输入
            if (this.$refs.fileInput) {
                this.$refs.fileInput.value = "";
            }
            if (this.$refs.fileInput2) {
                this.$refs.fileInput2.value = "";
            }
        },
        // ... 其他方法
    },
};
</script>

<style scoped>
.data-generator {
    display: flex;
    height: 100vh;
}

.left-panel {
    width: 30%; /* 或者你想要的任何固定宽度 */
    min-width: 30%; /* 使用min-width而不是width可以保证宽度至少为250px */
    padding: 20px;
    background-color: #f5f5f5;
    border-right: 2px solid #ddd;
    overflow-y: auto; /* 如果内容太多，允许滚动 */

    text-align: left;
}

.file-upload-placeholder {
    /* 样式可以根据需要进行调整 */
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 10px;
    margin-top: 10px;
    text-align: center;
    cursor: pointer;
    background-color: #f8f8f8;
}

.right-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow-y: auto; /* 如果内容太多，允许滚动 */
}

/* input{
    text-align: left !important;
} */

.uploaded-files {
    margin-top: 20px;
    padding: 10px;
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 5px;
}

.uploaded-files div {
    padding: 5px;
    border-bottom: 1px solid #eee;
    cursor: pointer;
}

.uploaded-files div:hover {
    background-color: #f0f0f0;
}

.content-display {
    flex: 7;
    margin-top: 10px;
    padding: 20px;
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 5px;
    overflow-y: auto;
    text-align: left;
    font-size: 14px; /* 调整字体大小 */
}

.realtime-monitor {
    flex: 3;
    margin-top: 10px;
    padding: 20px;
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 5px;
    overflow-y: auto;
    text-align: left;
    font-size: 14px; /* 调整字体大小 */
}

.realtime-monitor {
    background-color: #e9e9e9;
}

button {
    margin-top: 10px;
    padding: 10px 15px;
    border: none;
    background-color: #5b9bd5;
    color: white;
    border-radius: 5px;
    cursor: pointer;
    display: block;
}

button:hover {
    background-color: #4a8cc7;
}

input[type="file"] {
    margin-top: 20px;
}

.content-display h2,
.realtime-monitor h2 {
    margin-bottom: 15px;
}

.generated-files {
    margin-top: 40px;
    margin-bottom: 100px;
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 9px;
    text-align: left;
}

.generated-files h2 {
    margin-bottom: 10px;
}

.generated-files ul {
    list-style: none;
    padding: 0;
}

.generated-files li {
    padding: 5px 0;
    border-bottom: 1px solid #eee;
}

.generated-files li a {
    text-decoration: none;
    color: #337ab7;
}

.generated-files li a:hover {
    text-decoration: underline;
}

.parameters-form input {
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 5px 10px;
    margin-top: 5px;
    margin-bottom: 10px;
    font-size: 16px;
    width: calc(100% - 22px); /* 减去边框和内边距的总宽度 */
}

.parameters-form input:focus {
    outline: none;
    border-color: #80bdff;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.button-disabled {
    pointer-events: none; /* 禁止鼠标事件 */
    cursor: not-allowed; /* 显示禁止图标 */
    background-color: #aaa; /* 灰色背景表示禁用状态 */
}

button:disabled {
    background-color: #aaa; /* 灰色背景表示禁用状态 */
    /* 如果需要，可以在这里添加其他表示禁用状态的样式 */
}

.pagination-controls {
    display: flex;
    justify-content: centern;
    align-items: center;
    padding: 10px;
    margin-top: 10px;
    background-color: #f9f9f9;
    border-radius: 5px;
}

.pagination-controls button {
    margin: 0 10px; /* 按钮之间的间距 */
    padding: 5px 15px; /*
    /*按钮内部的间距 */
    background-color: #007bff;
    border: none;
    color: white;
    border-radius: 3px;
    cursor: pointer;
}

.pagination-controls button:disabled {
    background-color: #ccc;
    cursor: default;
}

.pagination-controls span {
    font-weight: normal;
    color: #333;
}

table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px; /* 减小字体大小 */
}

th,
td {
    padding: 8px;
    text-align: left;
    border-bottom: 1px solid #ddd;
    font-weight: normal; /* 去除加粗 */
}

th {
    background-color: #f2f2f2;
}

pre {
    white-space: pre-wrap; /* Since CSS 2.1 */
    white-space: -moz-pre-wrap; /* Mozilla, since 1999 */
    white-space: -pre-wrap; /* Opera 4-6 */
    white-space: -o-pre-wrap; /* Opera 7 */
    word-wrap: break-word; /* Internet Explorer 5.5+ */
    overflow-x: auto; /* for horizontal scroll */
    border: 1px solid #ccc;
    background-color: #f8f8f8;
    padding: 10px;
    border-radius: 4px;
}
</style>
