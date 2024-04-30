<template>
  <div class="sidebar">
    <nav>
      <ul>
        <li>
          <router-link to="/"><i class="fas fa-home"></i> 首页</router-link>
        </li>
        <li>
          <router-link to="/monitor"><i class="fas fa-chart-bar"></i>资源监控</router-link>
        </li>
        <li>
          <router-link to="/generate"><i class="fas fa-database"></i>数据生成</router-link>
        </li>
        <li>
          <router-link to="/test"><i class="fas fa-cogs"></i>数据测试</router-link>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'Sidebar'
};
</script>

<style scoped>


.sidebar {
  width: 100%;
  height: 100%;
  background: #dbf0f9; /* 淡蓝色背景 */
  /*background: #5f5f5f; /* 淡黄色背景 */
  padding: 0;
  margin: 0;
}

ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

li {
  margin-bottom: 2em;
}

li a {
  text-decoration: none;
  color: #080808; /* 深色字体 */
  display: flex;
  align-items: center;
}

.fa-home {
  margin-right: 13%; 
}
.fa-chart-bar,
.fa-database{
  /* 使用一些图标库，例如 Font Awesome */
  /* 在这里添加适当的类来显示图标 */
  margin-right: 16%; /* 图标和文字之间的距离 */
}
.fa-cogs {
  margin-right: 13%; 
}

.sidebar nav ul li a {
  padding: 10px;
  border-radius: 4px;
  transition: background-color 0.3s;
  display: block; /* 确保链接占据整个列表项的空间 */
}

/* 链接处于活动状态或鼠标悬停时的样式 */
.sidebar nav ul li a.router-link-exact-active,
.sidebar nav ul li a:hover {
  color: #017cff; /* 更改为所需的高亮颜色 */
}

/* 文字对齐 */
.sidebar nav ul li {
  text-align: left; /* 确保文本左对齐 */
}

</style>
