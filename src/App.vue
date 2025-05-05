<script setup>
import { useRoute, useRouter } from "vue-router";
import { useToast } from "vue-toastification";
import IconUser from "./components/icons/IconUser.vue";
import IconFavorite from "./components/icons/IconFavorite.vue";

const route = useRoute();
const router = useRouter();
const toast = useToast();

const isAuthenticated = localStorage.getItem("isAuthenticated") === "true";

const goToFavorites = () => {
  if (isAuthenticated) {
    router.push("/favorites");
  } else {
    toast.error("Пожалуйста, войдите в систему, чтобы посмотреть избранное", {
      timeout: 3000,
      position: "bottom-center",
    });
  }
};

const goToAccount = () => {
  if (isAuthenticated) {
    localStorage.setItem("isAuthenticated", "false");
    toast.success("Вы успешно вышли из системы", {
      timeout: 3000,
      position: "bottom-center",
    });
    router.push("/login");
  } else {
    toast.info("Пожалуйста, войдите в систему", {
      timeout: 3000,
      position: "bottom-center",
    });
    router.push("/login");
  }
};
</script>

<template>
  <header>
    <h1 @click="$router.push('/')">MovieAs</h1>
    <button class="button-icon" @click="goToFavorites">
      <IconFavorite />
    </button>
    <button class="button-icon" @click="goToAccount">
      <IconUser />
    </button>
  </header>
  <router-view />
</template>

<style scoped>
header {
  background-color: var(--vt-c-black);
  display: grid;
  grid-template-columns: 90% 5% 5%;
  padding: 1rem;
  width: 100vw;
}

.button-icon {
  background-color: inherit;
  border: none;
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.button-icon:hover {
  background-color: var(--vt-c-black-mute-2);
}

@media (max-width: 768px) {
  header {
    grid-template-columns: 80% 10% 10%;
    padding: 0.75rem;
  }

  .button-icon {
    width: 40px;
    height: 40px;
  }
}

@media (max-width: 480px) {
  header {
    grid-template-columns: 75% 12.5% 12.5%;
    padding: 0.5rem;
  }

  .button-icon {
    width: 35px;
    height: 35px;
  }
}

.panel {
  background-color: #1a1a1a;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border-bottom: 1px solid var(--vt-c-blue-dark);
  box-shadow: 0 5px 5px -5px #003687;
}

.search-input {
  flex: 1;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: none;
  font-size: 1rem;
  outline: none;
}
</style>
