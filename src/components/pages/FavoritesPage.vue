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
        >
          <div class="favorite-poster-wrapper">
            <img
              :src="movie.poster"
              :alt="movie.title"
              class="favorite-poster"
            />
            <button
              class="remove-btn"
              @click="removeFromFavorites(movie.id)"
              title="Удалить из избранного"
            >
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  
  const favorites = ref([]);
  
  // Загружаем избранные фильмы из localStorage при монтировании компонента
  onMounted(() => {
    const storedFavorites = JSON.parse(localStorage.getItem('favorites')) || [];
    favorites.value = storedFavorites;
  });
  
  // Удалить фильм из избранных
  const removeFromFavorites = (movieId) => {
    const updatedFavorites = favorites.value.filter(movie => movie.id !== movieId);
    favorites.value = updatedFavorites;
    localStorage.setItem('favorites', JSON.stringify(updatedFavorites)); // Обновляем localStorage
  };
  </script>
  
  <style scoped>
  .favorites-page {
    background-color: #1c1c1e; /* Темная подложка */
  border-radius: 20px; /* Закругленные углы */
  box-shadow: 0 1px 30px 5px rgba(77, 92, 255, 0.445); /* Светлая тень */
  padding: 2rem;
  max-width: 1400px;
  margin: 2rem auto; /* Центрируем */
  }
  
  h1 {
    text-align: center;
    font-size: 2rem;
    margin-bottom: 20px;
  }
  
  .no-favorites p {
    font-size: 1.2rem;
    color: #aaa;
  }
  
  .favorites-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
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
  