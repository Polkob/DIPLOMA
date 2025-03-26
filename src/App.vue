<script setup>
import IconUser from './components/icons/IconUser.vue';
import IconFavorite from './components/icons/IconFavorite.vue';


</script>

<template>
  <header>
    <h1>FilmFinder</h1>
    <button class="button-icon"><IconFavorite /></button>
    <button class="button-icon"><IconUser /></button>
  </header>

  <main>
    
  </main>
</template>

<style scoped>
header {
  background-color: var(--vt-c-black-mute);
  display: grid;
  grid-template-columns: 90% 5% 5%;
  padding: 1rem;
  width: 100vw;
  border-bottom: 2px solid var(--vt-c-blue-dark);
  box-shadow: 0 10px 10px -10px #440087;
}
h1 {
  color: white;
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
</style>
