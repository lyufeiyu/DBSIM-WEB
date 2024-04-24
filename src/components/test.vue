<template>
  <div class="data-generator">
    <!-- 数据和表结构上传区 -->
    <div class="upload-section">
      <h2>上传数据和表结构</h2>
      <input type="file" @change="handleFileUpload" multiple accept=".sql,.csv" />
    </div>

    <!-- 参数设置区 -->
    <div class="parameter-section">
      <h2>设置参数</h2>
      <div>
        <label for="rowCount">行数:</label>
        <input type="number" id="rowCount" v-model.number="parameters.rowCount" />
      </div>
      <div>
        <label for="batchSize">批处理大小:</label>
        <input type="number" id="batchSize" v-model.number="parameters.batchSize" />
      </div>
    </div>

    <!-- 查询上传区 -->
    <div class="query-upload-section">
      <h2>上传测试查询</h2>
      <input type="file" @change="handleQueryUpload" accept=".sql" />
    </div>

    <!-- 动作区 -->
    <div class="actions-section">
      <button @click="generateData">生成数据</button>
      <button @click="runTest">运行测试</button>
    </div>

    <!-- 监控区 -->
    <div class="monitoring-section">
      <h2>监控</h2>
      <pre v-if="monitoringData">{{ monitoringData }}</pre>
      <div v-else>暂无监控数据。</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DataGenerator',
  data() {
    return {
      parameters: {
        rowCount: 1000,
        batchSize: 100,
      },
      monitoringData: null, // 存储监控数据
    };
  },
  methods: {
    handleFileUpload(event) {
      // 用户上传数据和表结构的处理逻辑
      const files = event.target.files;
      console.log('上传的文件:', files);
      // 实际情况下应该是发送文件到服务器的逻辑
    },
    handleQueryUpload(event) {
      // 用户上传查询的处理逻辑
      const file = event.target.files[0];
      console.log('上传的查询文件:', file);
      // 实际情况下应该是发送文件到服务器的逻辑
    },
    generateData() {
      // 调用后端API生成数据
      console.log('生成数据参数:', this.parameters);
      // 实际情况下应该是向后端发送请求的逻辑
      // 这里我们只是模拟
      this.monitoringData = '数据生成中...';
      setTimeout(() => {
        this.monitoringData = '数据生成完毕';
      }, 3000);
    },
    runTest() {
      // 调用后端API运行测试
      console.log('运行测试');
      // 实际情况下应该是向后端发送请求的逻辑
      // 这里我们只是模拟
      this.monitoringData = '测试运行中...';
      setTimeout(() => {
        this.monitoringData = '测试完成';
      }, 3000);
    },
  },
};
</script>

<style scoped>
.data-generator {
  /* 主容器样式 */
  padding: 1rem;
  background: #f5f5f5;
}

.upload-section,
.parameter-section,
.query-upload-section,
.actions-section,
.monitoring-section {
  /* 区块样式 */
  margin-bottom: 1rem;
}

input[type="file"],
input[type="number"],
button {
  /* 输入框和按钮的样式 */
  display: block;
  margin-top: .5rem;
}

pre {
  /* 监控数据的预格式化样式 */
  background-color: #333;
  color: #fff;
  padding: .5rem;
}
</style>
