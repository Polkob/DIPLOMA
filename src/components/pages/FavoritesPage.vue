<template>
  <div class="favorites-page">
    <h1>Избранные фильмы</h1>
    <div v-if="favorites.length === 0" class="no-favorites">
      <p>Нет избранных фильмов</p>
    </div>
    <div v-else class="favorites-list">
      <div
        v-for="movie in favorites"
        :key="movie.id"
        class="favorite-item"
        @click="openDetails(movie)"
        style="cursor:pointer"
      >
        <div class="favorite-poster-wrapper">
          <img
            :src="getPosterUrl(movie.poster_path)"
            :alt="movie.title"
            class="favorite-poster"
          />
          <button
            class="remove-btn"
            @click="removeFromFavorites(movie.id)"
            title="Удалить из избранного"
          ></button>
        </div>
      </div>
    </div>

    <FilmDetailsModal
      v-if="showDetails"
      :show="showDetails"
      :movie="detailsMovie"
      @close="closeDetails"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import FilmDetailsModal from '@/components/modals/FilmDetailsModal.vue'
import axios from 'axios'

const favorites = ref([]);
const showDetails = ref(false)
const detailsMovie = ref(null)
const API_KEY = "54a2541709252b5e3de68b7642666940" // твой ключ

onMounted(() => {
  const storedFavorites = JSON.parse(localStorage.getItem("favorites")) || [];
  favorites.value = storedFavorites;
});

const removeFromFavorites = (movieId) => {
  const updatedFavorites = favorites.value.filter(
    (movie) => movie.id !== movieId
  );
  favorites.value = updatedFavorites;
  localStorage.setItem("favorites", JSON.stringify(updatedFavorites));
};

const getPosterUrl = (path) => {
  console.log(path);
  return path
    ? `https://image.tmdb.org/t/p/w500${path}`
    : "https://via.placeholder.com/500x750?text=Нет+постера";
};

const openDetails = async (movie) => {
  // Загружаем детали фильма с credits
  const { data } = await axios.get(`https://api.themoviedb.org/3/movie/${movie.id}`, {
    params: {
      api_key: API_KEY,
      language: 'ru-RU',
      append_to_response: 'credits'
    }
  })
  detailsMovie.value = data
  showDetails.value = true
}

const closeDetails = () => showDetails.value = false
</script>

<style scoped>
.favorites-page {
  padding: 2rem;
  max-width: 100vw;
}

h1 {
  text-align: center;
  font-size: 1.7rem;
  margin-bottom: 40px;
}

.no-favorites p {
  font-size: 1.2rem;
  color: #aaa;
}

.favorites-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 24px;
  justify-items: center;
  justify-content: center;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.favorite-item {
  position: relative;
}

.favorite-poster-wrapper {
  position: relative;
  width: 100%;
  height: 300px;
}

.favorite-poster {
  width: 100%;
  height: 100%;
  border-radius: 8px;
  object-fit: cover;
}

.remove-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: rgba(10, 207, 0, 0.5);
  color: white;
  border: none;
  padding: 8px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 20px;
  transition: background-color 0.3s;
}

.remove-btn:hover {
  background-color: rgba(255, 0, 0, 0.7);
}

.remove-btn i {
  margin: 0;
}
</style>
