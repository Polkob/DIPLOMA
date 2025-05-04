<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useToast } from 'vue-toastification'

const router = useRouter();
const toast = useToast()

const username = ref("");
const password = ref("");

const login = () => {
  if (username.value && password.value) {
    router.push('/')
  } else {
    toast.error('Пожалуйста, введите логин и пароль', {
      timeout: 3000,
      position: 'bottom-center'
    })
  }
}
</script>

<template>
  <div class="login-container">
    <h2>Вход в FilmFinder</h2>

    <form @submit.prevent="login" class="login-form">
      <input
        v-model="username"
        type="text"
        placeholder="Логин"
        class="login-input"
      />
      <input
        v-model="password"
        type="password"
        placeholder="Пароль"
        class="login-input"
      />
      <button type="submit" class="login-button">Войти</button>
    </form>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #1a1a1a;
  box-shadow: 0px 2px 2px 20px white;
}

h2 {
  color: white;
  margin-bottom: 2rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 300px;
}

.login-input {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: none;
  font-size: 1rem;
  outline: none;
}

.login-button {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: none;
  background-color: var(--vt-c-blue-dark, #440087);
  color: white;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-button:hover {
  background-color: #5c00b3;
}
</style>
