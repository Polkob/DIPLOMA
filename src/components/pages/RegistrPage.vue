<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useToast } from "vue-toastification";

const router = useRouter();
const toast = useToast();

const username = ref("");
const password = ref("");
const confirmPassword = ref("");

const register = () => {
  if (!username.value || !password.value || !confirmPassword.value) {
    toast.error("Пожалуйста, заполните все поля", {
      position: "bottom-center",
    });
    return;
  }

  if (password.value !== confirmPassword.value) {
    toast.error("Пароли не совпадают", {
      position: "bottom-center",
    });
    return;
  }

  toast.success("Регистрация прошла успешно!", {
    position: "bottom-center",
  });

  router.push("/login");
};
</script>

<template>
  <div class="register-container">
    <div class="register-card">
      <h2>Регистрация в <span class="highlight">FilmFinder</span></h2>

      <form @submit.prevent="register" class="register-form">
        <input
          v-model="username"
          type="text"
          placeholder="Логин"
          class="register-input"
          autofocus
        />
        <input
          v-model="password"
          type="password"
          placeholder="Пароль"
          class="register-input"
        />
        <input
          v-model="confirmPassword"
          type="password"
          placeholder="Подтверждение пароля"
          class="register-input"
        />
        <button type="submit" class="register-button">
          Зарегистрироваться
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(to bottom right, #0f0f0f, #1a1a1a);
}

.register-card {
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

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.register-input {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: 1px solid #444;
  background-color: #333;
  color: #fff;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s;
}

.register-input:focus {
  border-color: #8e2de2;
}

.register-button {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: none;
  background-color: #8e2de2;
  color: white;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.register-button:hover {
  background-color: #732dd1;
}
</style>
