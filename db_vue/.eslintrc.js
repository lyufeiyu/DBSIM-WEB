module.exports = {
    root: true,
    env: {
      node: true,
    },
    extends: [
      'plugin:vue/vue3-essential',
      // 可能还有其他的extends配置
    ],
    parserOptions: {
      parser: '@babel/eslint-parser',
    },
    rules: {
      'vue/multi-word-component-names': 'off', // 添加这一行来禁用规则
      // 其他规则配置
    },
  };
  