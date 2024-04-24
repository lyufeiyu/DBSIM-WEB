<template>
    <div class="data-generator">
        <!-- 左边栏：逻辑操作区 -->
        <div class="left-panel">
            <!-- 上传文件按钮 -->
            <input type="file" @change="handleFileUpload" accept=".csv" />

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
                <button @click="clearContent">清除内容</button>
            </div>

            <!-- 生成数据按钮 -->
            <button @click="generateData">生成数据</button>

            <!-- 历史生成文件区 -->
            <div class="generated-files">
                <h2>历史生成文件</h2>
                <ul>
                    <li v-for="file in generatedFiles" :key="file.name">
                        <a :href="file.downloadUrl" download>{{ file.name }}</a>
                    </li>
                </ul>
            </div>
        </div>

        <!-- 右边栏：内容呈现区和实时监控区 -->
        <div class="right-panel">
            <!-- 内容呈现区 -->
            <div class="content-display">
                <h2>文件查看区</h2>
                <!-- 如果有选中的文件，显示其内容，否则提示 -->
                <div v-if="selectedFileContent">
                    {{ selectedFileContent }}
                </div>
                <div v-else>请选择或上传CSV文件以查看内容</div>
            </div>

            <!-- 实时监控区 -->
            <div class="realtime-monitor">
                <h2>数据生成监控区</h2>
                <!-- 监控数据生成的实时状态 -->
                <p v-if="monitoringData">
                    正在生成数据，已完成{{ monitoringData }}行...
                </p>
                <p v-else>数据生成的实时监控将显示在此处</p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            files: [],
            // generatedFiles: [], // 存储生成的文件信息
            selectedFileContent: "", // 存储选中文件的内容
            monitoringData: null, // 模拟监控数据
            generatedFiles: [], // 用来存储生成的文件信息和下载链接
            // 其他必要的状态
        };
    },
    methods: {
        handleFileUpload(event) {
            const file = event.target.files[0];
            if (file) {
                this.files.push(file);
                // 自动选中最新上传的文件
                this.selectFile(file);
            }
        },
        selectFile(file) {
            // 使用 FileReader 读取选中文件的内容
            const reader = new FileReader();
            reader.onload = (e) => {
                this.selectedFileContent = e.target.result; // 将文件内容赋值到变量
            };
            reader.readAsText(file);
        },
        generateData() {
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
        addToGeneratedFiles(fileName) {
            const downloadUrl = "/path/to/generated/" + fileName; // 替换为实际的文件下载路径
            this.generatedFiles.push({ name: fileName, downloadUrl });
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
    flex: 1;
    padding: 20px;
    background-color: #f5f5f5;
    border-right: 2px solid #ddd;
}

.right-panel {
    flex: 2;
    display: flex;
    flex-direction: column;
}

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
    padding: 10px;
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
