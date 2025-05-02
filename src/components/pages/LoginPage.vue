<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useToast } from "vue-toastification";

const router = useRouter();
const toast = useToast();

const username = ref("");
const password = ref("");

const login = () => {
  if (username.value && password.value) {
    localStorage.setItem("isAuthenticated", "true");
    localStorage.setItem("user", JSON.stringify({ username: username.value }));
    router.push("/");
  } else {
    toast.error("Пожалуйста, введите логин и пароль", {
      timeout: 3000,
      position: "bottom-center",
    });
  }
};

const goToRegister = () => {
  router.push("/register");
};
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <h2>Вход в <span class="highlight">FilmFinder</span></h2>

      <form @submit.prevent="login" class="login-form">
        <input
          v-model="username"
          type="text"
          placeholder="Логин"
          class="login-input"
          autofocus
        />
        <input
          v-model="password"
          type="password"
          placeholder="Пароль"
          class="login-input"
        />
        <div class="login-actions">
          <button type="submit" class="login-button">Войти</button>
          <button type="button" class="register-button" @click="goToRegister">
            Регистрация
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(to bottom right, #0f0f0f, #1a1a1a);
}

.login-card {
  background-color: #222;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(255, 255, 255, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

h2 {
  color: white;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.highlight {
  color: #8e2de2;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.login-input {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: 1px solid #444;
  background-color: #333;
  color: #fff;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s;
}

.login-input:focus {
  border-color: #8e2de2;
}

.login-actions {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.login-button,
.register-button {
  flex: 1;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-button {
  background-color: #8e2de2;
  color: white;
}

.login-button:hover {
  background-color: #732dd1;
}

.register-button {
  background-color: #444;
  color: #ccc;
}

.register-button:hover {
  background-color: #666;
}
</style>
