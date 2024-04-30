<template>
    <div class="data-generator">
        <!-- 左边栏：逻辑操作区 -->
        <div class="left-panel">
            <!-- 上传文件按钮 -->
            <input
                type="file"
                multiple
                @change="handleFileUpload"
                accept=".csv"
            />
            <input
                type="file"
                @change="handleSchemaUpload"
                accept=".txt"
                placeholder="上传 Schema 文件"
            />

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
                <input
                    v-model="params.param1"
                    type="text"
                    placeholder="参数1"
                />
                <input
                    v-model="params.param2"
                    type="number"
                    placeholder="参数2"
                />
                <!-- 可以继续添加其他参数的输入框 -->
            </div>

            <!-- 生成数据按钮 -->
            <button @click="generateData">生成数据</button>

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
            <div class="content-display">
                <h2>文件查看区</h2>
                <div v-if="selectedFileContent">
                    {{ selectedFileContent }}
                </div>
                <div v-else>请选择或上传CSV文件以查看内容</div>
            </div>

            <!-- 实时监控区 -->
            <div class="realtime-monitor">
                <h2>数据生成监控区</h2>
                <p v-if="monitoringData">
                    正在生成数据，已完成{{ monitoringData }}行...
                </p>
                <p v-else>数据生成的实时监控将显示在此处</p>
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
            selectedFileContent: "", // 存储选中文件的内容
            monitoringData: null, // 模拟监控数据
            generatedFiles: [], // 用来存储生成的文件信息和下载链接
            params: {
                // 存储用户设置的参数
                param1: "",
                param2: 0,
                // 添加更多参数
            },
        };
    },
    created() {
        this.fetchHistoryFiles();
    },
    methods: {
        handleFileUpload(event) {
            // 上传多个CSV文件
            const files = event.target.files;
            if (files) {
                for (let file of files) {
                    this.files.push(file);
                }
                this.selectFile(files[0]); // 默认选中第一个文件
            }

            // 创建 FormData 对象
            let formData = new FormData();
            for (let file of this.files) {
                formData.append("myfile", file);

                // 发送 POST 请求到 Django 服务器
                axios
                    .post("http://localhost:8000/generator/upload/", formData, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        },
                    })
                    .then((response) => {
                        // 文件上传成功
                        console.log("Uploaded:", response.data);
                        // 你可能想把这个文件加到生成的文件列表中
                        // this.generatedFiles.push({
                        //     name: file.name,
                        //     // 这里你需要处理响应数据以获得正确的下载 URL
                        //     downloadUrl: response.data.uploaded_file_url,
                        // });
                    })
                    .catch((error) => {
                        // 文件上传失败
                        console.error("Upload failed:", error);
                    });
            }
        },
        handleSchemaUpload(event) {
            const file = event.target.files[0];
            if (file && file.name.endsWith(".txt")) {
                // 确保是txt文件
                // 创建 FormData 对象并添加文件
                let formData = new FormData();
                formData.append("schema", file);

                // 发送 POST 请求到服务器
                axios
                    .post("http://localhost:8000/generator/upload/", formData, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        },
                    })
                    .then((response) => {
                        // 文件上传成功，可以在这里处理响应
                        console.log("Schema uploaded:", response.data);
                    })
                    .catch((error) => {
                        // 文件上传失败
                        console.error("Schema upload failed:", error);
                    });
            } else {
                console.error("Please upload a valid .txt file");
            }
        },

        fetchHistoryFiles() {
            // 获取历史文件列表
            axios
                .get("http://localhost:8000/generator/history-files/")
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
            const url = "http://localhost:8000" + file.download_url;
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
        selectFile(file) {
            // 选择文件，读取内容
            // 使用 FileReader 读取选中文件的内容
            const reader = new FileReader();
            reader.onload = (e) => {
                this.selectedFileContent = e.target.result; // 将文件内容赋值到变量
            };
            reader.readAsText(file);
        },
        generateData() {
            // 这里构造包含参数的FormData
            let formData = new FormData();
            for (let key in this.params) {
                formData.append(key, this.params[key]);
            }
            // 假设我们要把文件也一起发送
            this.files.forEach((file) => {
                formData.append("files", file);
            });

            // 发送 POST 请求到服务器以生成数据
            axios
                .post(
                    "http://localhost:8000/generator/generate-data/",
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
                })
                .catch((error) => {
                    // 数据生成请求失败
                    console.error("Data generation failed:", error);
                });

            // 生成数据

            // 模拟数据生成过程
            this.monitoringData = 0; // 初始化监控数据
            const interval = setInterval(() => {
                this.monitoringData += 100; // 假设每次增加100行
                if (this.monitoringData >= 1000) {
                    // 当达到1000行时停止
                    clearInterval(interval);
                    this.monitoringData = "完成";
                    // 假设生成的文件信息
                    this.generatedFiles.push({
                        name: "data-" + new Date().toISOString() + ".csv",
                        downloadUrl: "path/to/generated/file.csv", // 这里应该是生成文件的下载链接
                    });
                }
            }, 1000); // 每1秒更新一次
        },
        clearContent() {
            // 清除文件查看区的内容
            this.selectedFileContent = "";
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

.content-display,
.realtime-monitor {
    flex: 1;
    margin-top: 20px;
    padding: 20px;
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 5px;
    overflow-y: auto;
    text-align: left;
}

.realtime-monitor {
    background-color: #e9e9e9;
}

button {
    margin-top: 20px;
    padding: 10px 15px;
    border: none;
    background-color: #5b9bd5;
    color: white;
    border-radius: 5px;
    cursor: pointer;
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

button {
    display: block;
    margin-top: 10px;
    /* 根据需要调整样式 */
}

.generated-files {
    margin-top: 40px;
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
</style>
