<script setup>
import { useRoute } from 'vue-router'
import IconUser from './components/icons/IconUser.vue';
import IconFavorite from './components/icons/IconFavorite.vue';

const route = useRoute()
</script>

<template>
  <header v-if="route.path !== '/login'">
    <h1 @click="$router.push('/')">MovieAs</h1>
    <button class="button-icon" @click="$router.push('/favorites')">
      <IconFavorite />
    </button>
    <button class="button-icon" @click="$router.push('/login')">
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
h1 {
  color: rgba(255, 255, 255, 0.753); /* Цвет текста */
  text-shadow: 0px 4px 8px rgba(68, 0, 135, 0.6), 0px 0px 25px rgba(68, 0, 135, 0.6); /* Тень */
}

.button-icon{
  background-color: inherit;
  border: none;
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.button-icon:hover {
  background-color:  var(--vt-c-black-mute-2);
}
.panel {
  background-color: #1a1a1a;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border-bottom: 1px solid var(--vt-c-blue-dark);
  box-shadow: 0 5px 5px -5px #440087;
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
