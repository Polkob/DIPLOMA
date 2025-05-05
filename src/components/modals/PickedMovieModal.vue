<template>
    <div v-if="show" class="modal-backdrop" @click.self="close">
      <div class="modal-content">
        <span class="close-x" @click="close">&times;</span>
        <h2>Результаты подбора</h2>
        <div v-if="movies.length > 0" class="movies-grid">
          <div
            v-for="movie in movies"
            :key="movie.id"
            class="movie-card"
            @click="openDetails(movie)"
            style="cursor:pointer"
          >
            <img :src="getImageUrl(movie.poster_path)" alt="poster" />
            <h3>{{ movie.title }}</h3>
            <div class="movie-country" v-if="getCountry(movie)">
              {{ getCountry(movie) }}
            </div>
            <div class="movie-year">
              {{ getYear(movie.release_date) }}
            </div>
          </div>
        </div>
        <div v-else>
          <p>Фильмы не найдены.</p>
        </div>
        <button v-if="canLoadMore" @click="loadMore" class="load-more-btn">Показать ещё</button>
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
  import { ref } from 'vue'
  import FilmDetailsModal from './FilmDetailsModal.vue'
  import defaultPoster from '@/assets/film-poster-default.webp'
  import axios from 'axios'
  
  const props = defineProps({
    movies: {
      type: Array,
      required: true,
    },
    show: {
      type: Boolean,
      required: true,
    },
    canLoadMore: Boolean
  })
  const emit = defineEmits(['close', 'loadMore'])
  
  const close = () => emit('close')
  const loadMore = () => emit('loadMore')
  
  const getImageUrl = (path) => {
    return path
      ? `https://image.tmdb.org/t/p/w500${path}`
      : defaultPoster
  }
  const getYear = (date) => {
    return date ? new Date(date).getFullYear() : '—'
  }
  const getCountry = (movie) => {
    return movie.production_countries?.[0]?.name || ''
  }
  
  // Для модалки деталей
  const showDetails = ref(false)
  const detailsMovie = ref(null)
  const API_KEY = "54a2541709252b5e3de68b7642666940"
  
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
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  .modal-content {
    background: rgb(26, 26, 26);
    padding: 32px 32px 24px 32px;
    max-height: 90vh;
    overflow-y: auto;
    width: 90vw;
    max-width: 1100px;
    border-radius: 16px;
    position: relative;
  }
  .modal-content::-webkit-scrollbar {
  display: none;
}

  .close-x {
    position: absolute;
    top: 18px;
    right: 24px;
    font-size: 2.2rem;
    color: #fff;
    cursor: pointer;
    z-index: 2;
    transition: color 0.2s;
  }
  .close-x:hover {
    color: #8e2de2;
  }

  .movies-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 24px;
    margin-top: 24px;
  }
  .movie-card {
    background: #181818;
    border-radius: 12px;
    padding: 18px 12px 14px 12px;
    text-align: center;
    min-width: 200px;
    max-width: 320px;
    margin: 0 auto;
    box-shadow: 0 2px 12px 0 #00000033;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .movie-card img {
    width: 100%;
    max-width: 180px;
    height: 260px;
    object-fit: cover;
    border-radius: 8px;
    margin-bottom: 10px;
    background: #222;
  }
  .movie-card h3 {
    font-size: 1.1rem;
    margin: 8px 0 4px 0;
    color: #fff;
    font-weight: 600;
  }
  .movie-country {
    color: #a259ec;
    font-size: 1rem;
    margin-bottom: 2px;
    font-weight: 500;
  }
  .movie-year {
    color: #42a5f5;
    font-size: 1rem;
    margin-bottom: 0;
    font-weight: 500;
  }
  .load-more-btn {
    display: block;
    margin: 32px auto 0 auto;
    padding: 12px 32px;
    background: #440087;
    color: #fff;
    border: none;
    border-radius: 10px;
    font-size: 1.1rem;
    cursor: pointer;
    transition: background 0.2s;
  }
  .load-more-btn:hover {
    background: #8e2de2;
  }
  </style>
  