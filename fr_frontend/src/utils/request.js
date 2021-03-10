import axios from 'axios'
// import Qs from 'Qs'
import { ElMessage } from 'element-plus';
import store from '@/store'
import router from '@/router'
import { loadCsrfToken, loadToken } from '@/common/js/cache';


axios.defaults.timeout = 6000;
axios.defaults.baseURL = process.env.VUE_APP_API;
axios.defaults.headers.post['Content-Type'] = 'application/json'
axios.defaults.headers.put['Content-Type'] = 'application/json'


// http request 拦截器
axios.interceptors.request.use(
  request => {
    let csrftoken = loadCsrfToken();
    if (csrftoken) {
      request.headers['x-csrftoken'] = csrftoken;
    }
    let token = loadToken();
    if (token) {
      request.headers.Authorization = `Token ${token}`;
    }
    return request
  },
  error => {
    // 请求发生错误
    console.log('request interceptor error') // for debug
    Promise.reject(error)
  }
)

// http response 拦截器
axios.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    console.log('response interceptor error', error) // for debug 
    let msg = '未知错误'
    if (error.response) {
      switch (error.response.status) {
        case 400:
          msg = '错误请求'
          break;
        case 401:
          // 401 清除token信息并跳转到登录页面
          store.dispatch("removeUserInfo");
          msg = '认证失效'
          router.push({
            path: '/',
            query: { redirect: router.currentRoute.fullPath }
          });
          break
        case 403:
          // 403 清除token信息并跳转到登录页面
          store.dispatch("removeUserInfo");
          msg = '拒绝访问'
          router.push({
            path: '/',
            query: { redirect: router.currentRoute.fullPath }
          });
          break
        case 404:
          msg = '请求错误,未找到该资源'
          router.push({
            path: '/',
            query: { redirect: router.currentRoute.fullPath }
          });
          break;
        case 405:
          msg = '请求方法未允许'
          break;
        case 408:
          msg = '请求超时'
          break;
        case 500:
          msg = '服务器端出错'
          break;
        case 501:
          msg = '网络未实现'
          break;
        case 502:
          msg = '网络错误'
          break;
        case 503:
          msg = '服务不可用'
          break;
        case 504:
          msg = '网络超时'
          break;
        case 505:
          msg = 'http版本不支持该请求'
          break;
        default:
          msg = `连接错误 ${error.response.status}`
      }
    }
    ElMessage({
      message: msg,
      type: 'error',
      duration: 3 * 1000
    })
    return Promise.reject(error.response.data);
  });

export default axios;