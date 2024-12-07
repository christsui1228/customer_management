// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/DefaultLayout.vue'),
    children: [
      {
        path: '',
        redirect: '/customers'
      },
      {
        path: 'customers',
        name: 'Customers',
        component: () => import('../views/customers/index.vue'),
        meta: {
          title: '客户管理'
        }
      }
      // 其他路由...
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router