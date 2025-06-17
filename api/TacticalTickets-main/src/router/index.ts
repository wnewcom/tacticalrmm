import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Dashboard from '../views/Dashboard.vue'
import Login from '../views/Login.vue'
import TicketList from '../views/TicketList.vue'
import TicketDetail from '../views/TicketDetail.vue'
import CreateTicket from '../views/CreateTicket.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: Dashboard,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { requiresAuth: false }
    },
    {
      path: '/tickets',
      name: 'tickets',
      component: TicketList,
      meta: { requiresAuth: true }
    },
    {
      path: '/tickets/create',
      name: 'create-ticket',
      component: CreateTicket,
      meta: { requiresAuth: true }
    },
    {
      path: '/tickets/:id',
      name: 'ticket-detail',
      component: TicketDetail,
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.name === 'login' && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router