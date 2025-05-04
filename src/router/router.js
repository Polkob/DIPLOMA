import { createRouter, createWebHistory } from "vue-router";
import { useToast } from "vue-toastification";
import HomePage from "../components/pages/HomePage.vue";
import FavoritesPage from "../components/pages/FavoritesPage.vue";
import LoginPage from "../components/pages/LoginPage.vue";
import RegisterPage from "@/components/pages/RegistrPage.vue";

const routes = [
  { path: "/", component: HomePage },
  {
    path: "/favorites",
    component: FavoritesPage,
    meta: { requiresAuth: true },
  },
  { path: "/login", component: LoginPage },
  { path: "/register", component: RegisterPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuth = localStorage.getItem("isAuthenticated") === "true";
  const toast = useToast();
  if (to.meta.requiresAuth && !isAuth) {
    toast.error("Пожалуйста, войдите в систему, чтобы продолжить.", {
      timeout: 3000,
      position: "bottom-center",
    });
    next("/login");
  } else {
    next();
  }
});

export default router;
