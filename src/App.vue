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
    <section class="panel">
      <input type="text" placeholder="Поиск фильма..." class="search-input" />

      <div class="cards">
        <div class="movie-card">
          <img src="https://via.placeholder.com/100x150?text=Poster+1" alt="Movie Poster 1" />
        </div>
        <div class="movie-card">
          <img src="https://via.placeholder.com/100x150?text=Poster+2" alt="Movie Poster 2" />
        </div>
      </div>
    </section>
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

.cards {
  display: flex;
  gap: 1rem;
}

.movie-card {
  width: 100px;
  height: 150px;
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.4);
}

.movie-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

</style>
