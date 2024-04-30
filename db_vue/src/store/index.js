// store/index.js 将包含 Vuex store 的定义。
import { createStore } from 'vuex';

export default createStore({
    state: {
        breadcrumbs: [],
    },
    mutations: {
        
        setBreadcrumb(state, breadcrumb) {
            // 如果面包屑已存在，则不重复添加
            if (!state.breadcrumbs.some(b => b.path === breadcrumb.path)) {
                state.breadcrumbs.push(breadcrumb);
            }
        },
        removeBreadcrumb(state, breadcrumb) {
            state.breadcrumbs = state.breadcrumbs.filter(b => b.path !== breadcrumb.path);
        }
    },
    actions: {
        addBreadcrumb({ commit }, breadcrumb) {
            commit('setBreadcrumb', breadcrumb);
        },
        deleteBreadcrumb({ commit }, breadcrumb) {
            commit('removeBreadcrumb', breadcrumb);
        }
    }
});
