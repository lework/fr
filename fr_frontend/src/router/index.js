import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'

const page404 = {
  path: '/:pathMatch(.*)*',
  name: 'error-404',
  meta: {
      title: '404-页面不存在'
  },
  hidden: true,
  component: () => import(/* webpackChunkName: "about" */ '@/views/error-page/404.vue')
};

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/detail/:id',
    title: '事件详情',
    name: 'Detail',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '@views/Detail.vue')
  },
  page404
]

console.log(routes)

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
