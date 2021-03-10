import * as types from '@/store/mutation-types'
import { loadUser, loadToken, removeLoginInfo, saveLoginInfo } from '@/common/js/cache'

// 用户模块
const user = {

  // 存储全局变量的数据
  state: {
    user: { username: loadUser(), token: loadToken() },
  },

  // 提供存储设置state数据的方法
  mutations: {
    // state指的是state的数据
    // name传递过来的数据
    [types.SET_USER]: (state, data) => {
      state.user = data //将传参设置给state的user
    },
  },

  // 提供用来获取state数据的方法
  getters: {
    getUsername: state => state.user.username,
    getToken: state => state.user.token,
  },

  // 提供跟后台接口打交道的方法，并调用mutations提供的方法
  actions: {
    // 设置用户信息
    // 参数列表：{commit, state}
    // state指的是state数据
    // commit调用mutations的方法 
    // data就是调用此方法时要传的参数
    saveUserInfo ({ commit }, data) {
      commit(types.SET_USER, data)
      saveLoginInfo(data)
    },

    // 删除用户信息
    removeUserInfo ({ commit }) {
      commit(types.SET_USER, {})
      removeLoginInfo()
    }
  }
}

export default user
