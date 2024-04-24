<template>
    
</template>

  <!-- <div class="breadcrumb-container">  
    <Breadcrumb>
      <BreadcrumbItem to="/">主页</BreadcrumbItem>
      <BreadcrumbItem to="/database">数据库监控</BreadcrumbItem>
      <BreadcrumbItem>资源监控</BreadcrumbItem>
    </Breadcrumb>
  </div> -->

<script>

</script>


<!--
import { Breadcrumb, BreadcrumbItem } from 'view-design';

export default {
  components: {
    Breadcrumb,
    BreadcrumbItem
  }
};
</script>

<style scoped>
.breadcrumb-container {
  background-color: #515a6e; /* 与侧边栏相同的背景颜色 */
  padding: 8px 15px; /* 按需调整内边距 */
  margin: 0; /* 移除外边距 */
}

.breadcrumb-container /deep/ .ivu-breadcrumb {
  padding: 0; /* 移除默认内边距 */
  margin: 0; /* 确保没有默认外边距 */
}

.breadcrumb-container >>> .ivu-breadcrumb-item-link {
  color: #fff; /* 文字颜色设置为白色或其他与侧边栏匹配的颜色 */
}

.breadcrumb-container /deep/ .ivu-breadcrumb-item + .ivu-breadcrumb-item:before {
  color: #fff; /* 面包屑分隔符颜色 */
}

/* 如果你的构建系统不支持 /deep/，可以尝试使用 >>> 来穿透scoped样式 */