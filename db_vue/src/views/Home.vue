<template>
  <div class="home">
    <div class="welcome-section">
      <h1>Welcome to DBSIM-WEB！</h1>
      <p>This is a platform for resource monitoring, data management and data test.</p>
    </div>

    <div class="quick-links">
      <h2>Quick Links</h2>
      <ul>
        <li><router-link to="/monitor">Resource Monitoring</router-link></li>
        <li><router-link to="/generate">Data Generation</router-link></li>
        <li><router-link to="/test">Data Testing</router-link></li>
      </ul>
    </div>

    <div class="user-guide">
      <h2>User Guide</h2>
      <p>Below is a brief guide on how to get started with DBSIM-WEB.</p>
      <ul>
        <p>Monitor your server resources and database resources in real-time with our comprehensive dashboard.</p>
        <p>Generate data and query with custom parameters for testing and simulation.</p>
        <p>Test data integrity and performance of different databases with our built-in tools.</p>
      </ul>
    </div>

    <div class="realtime-data">
      <h2>Click on the sidebar to get started！</h2>
      <!-- 例如，这里可以插入一个图表或者数据快照组件 -->
    </div>
  </div>
</template>

<script>
export default {
    setup() {
        // 定义组件的逻辑...
    },
}
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.welcome-section, .quick-links, .user-guide, .realtime-data,ul p {
  margin-bottom: 20px;
  width: 100%; /* 宽度根据需要调整 */
  max-width: 800px; /* 最大宽度也根据需要调整 */
  text-align: center;
}

.quick-links ul {
  display: flex;
  justify-content: center;
  list-style-type: none;
  padding: 0;
  text-align: center;
}

.quick-links li {
  margin: 0 10px;
}

.user-guide ul {
  text-align: left;
  list-style-type: disc;
  margin-top: 10px;
  padding-left: 40px; /* 为列表项添加缩进 */
}


</style>
