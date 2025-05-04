import { createRouter, createWebHistory } from 'vue-router'

import HomePage from '../components/pages/HomePage.vue'
import FavoritesPage from '../components/pages/FavoritesPage.vue'
import LoginPage from '../components/pages/LoginPage.vue'

const routes = [
  { path: '/', component: HomePage },
  { path: '/favorites', component: FavoritesPage },
  { path: '/login', component: LoginPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
