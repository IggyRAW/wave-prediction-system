import { createRouter, createWebHistory } from 'vue-router'
import Top from '@/views/Top.vue'
import Learning from '@/views/Learning.vue'
import SeaInfomation from '@/views/SeaInfomation.vue'

const routes = [
  {
    path: '/',
    component: Top
  },
  {
    path: '/Learning',
    component: Learning
  },
  {
    path: '/SeaInfomation',
    component: SeaInfomation
  }
]
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
