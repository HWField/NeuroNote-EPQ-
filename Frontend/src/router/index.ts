import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/Home.vue'
import AuthenticationView from '@/views/Authentication.vue'
import Error from '@/views/Error.vue'
import { useUserStore } from "@/stores/useUserStore";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: HomeView,
      meta: { requiresAuth: true } // Protect this route
    },
    {
      path: '/login',
      name: 'login',
      component: AuthenticationView,
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      // component: () => import('../App.vue'),
    },
    {
      path : '/error',
      name : 'error',
      component : Error,
      props: route => ({ message: route.query.message })
    },
    {
      path: '/:catchAll(.*)',
      name: 'not-found',
      component: Error,
      props: { message: 'Page not found' }
    }
  ],
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore() // Access store inside navigation guard
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } }) // Redirect to login if not authenticated
  } else {
    next() // Allow navigation
  }
})
export default router
