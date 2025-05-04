<template>
    <div v-if="show" class="modal-backdrop" @click.self="close">
      <div class="modal-content">
        <h2>Результаты подбора</h2>
        <div v-if="movies.length > 0" class="movies-grid">
          <div v-for="movie in movies" :key="movie.id" class="movie-card">
            <img :src="getImageUrl(movie.poster_path)" alt="poster" />
            <h3>{{ movie.title }}</h3>
            <p>{{ movie.release_date }}</p>
          </div>
        </div>
        <div v-else>
          <p>Фильмы не найдены.</p>
        </div>
        <button @click="close" class="close-btn">Закрыть</button>
      </div>
    </div>
  </template>
  
  <script setup>
  const props = defineProps({
    movies: {
      type: Array,
      required: true,
    },
    show: {
      type: Boolean,
      required: true,
    }
  })
  const emit = defineEmits(['close'])
  
  const close = () => emit('close')
  
  const getImageUrl = (path) => {
    return path
      ? `https://image.tmdb.org/t/p/w500${path}`
      : 'https://via.placeholder.com/200x300?text=Нет+постера'
  }
  </script>
  
  <style scoped>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  .modal-content {
    background: rgb(26, 26, 26);
    padding: 20px;
    max-height: 90vh;
    overflow-y: auto;
    width: 80%;
    max-width: 800px;
    border-radius: 8px;
  }
  .modal-content::-webkit-scrollbar {
  display: none;
}

  .movies-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 16px;
    margin-top: 16px;
  }
  .movie-card {
    background: #000000;
    border-radius: 8px;
    padding: 10px;
    text-align: center;
  }
  .movie-card img {
    width: 100%;
    height: auto;
    border-radius: 4px;
  }
  .close-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
  }
  </style>
  