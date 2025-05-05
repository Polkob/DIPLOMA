<template>
  <div v-if="show" class="modal-backdrop" @click.self="close">
    <div class="modal-content">
      <span class="close-x" @click="close">&times;</span>
      <div class="film-details">
        <img :src="getImageUrl(movie.poster_path)" class="film-poster" />
        <div class="film-info">
          <div class="film-header">
            <button class="favorite-btn" @click="toggleFavorite">
              <IconFavorite :filled="isFavorite" />
            </button>
            <h2>{{ movie.title }}</h2>
          </div>
          <div class="film-meta">
            <span class="meta blue">{{ getYear(movie.release_date) }}</span>
            <span class="meta blue">• {{ movie.runtime }} мин •{{ getCountry(movie) }}</span>
          </div>
          <div class="film-genres">
            <span v-for="genre in movie.genres" :key="genre.id" class="genre">
              {{ genre.name }}
            </span>
          </div>
          <div class="film-crew">
            <div><b>Режиссёр:</b> {{ getDirectors(movie.credits?.crew) }}</div>
            <div><b>Актёры:</b> {{ getActors(movie.credits?.cast) }}</div>
          </div>
          <div class="film-rating mb-2 pa-0 d-flex align-center">
            <IconRaiting />
            <div class="d-flex align-center ml-2" style="gap: 20px">
              <span style="font-size: 14px">{{ movie.vote_average }}</span>
            </div>
          </div>
          <div class="film-description">
            <b>Описание:</b>
            <p>{{ movie.overview || "Нет описания" }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import IconFavorite from '@/components/icons/IconFavorite.vue'
import IconRaiting from '@/components/icons/IconRaiting.vue'
import defaultPoster from '@/assets/film-poster-default.webp'
import { ref, computed, watch } from 'vue'
import { useToast } from "vue-toastification";

const props = defineProps({
  show: Boolean,
  movie: Object
})
const emit = defineEmits(['close'])

const close = () => emit('close')

const toast = useToast();

const getImageUrl = (path) => {
  return path
    ? `https://image.tmdb.org/t/p/w500${path}`
    : defaultPoster
}
const getYear = (date) => date ? new Date(date).getFullYear() : '—'
const getCountry = (movie) => movie.production_countries?.[0]?.name || '—'
const getDirectors = (crew) => {
  if (!crew) return '—'
  return crew.filter(p => p.job === 'Director').map(p => p.name).join(', ') || '—'
}
const getActors = (cast) => {
  if (!cast) return '—'
  return cast.slice(0, 5).map(a => a.name).join(', ') || '—'
}

// Проверка, в избранном ли фильм
const isFavorite = ref(false)
watch(
  () => props.movie,
  (movie) => {
    if (!movie) return
    const favs = JSON.parse(localStorage.getItem('favorites') || '[]')
    isFavorite.value = favs.some(f => f.id === movie.id)
  },
  { immediate: true }
)

const toggleFavorite = () => {
  if (!props.movie || !props.movie.id) return;

  // Проверка на авторизацию
  const isAuth = localStorage.getItem('isAuthenticated') === 'true';
  if (!isAuth) {
    toast.error('Чтобы добавить в избранное, войдите в аккаунт', {
      position: 'bottom-center'
    });
    return;
  }

  let favs = JSON.parse(localStorage.getItem('favorites') || '[]')
  const idx = favs.findIndex(f => f.id === props.movie.id)
  if (idx === -1) {
    favs.push(props.movie)
    isFavorite.value = true
    toast.success('Фильм добавлен в избранное 🎉', { position: "bottom-center" })
  } else {
    favs.splice(idx, 1)
    isFavorite.value = false
    toast.info('Фильм удалён из избранного ❌', { position: "bottom-center" })
  }
  localStorage.setItem('favorites', JSON.stringify(favs))
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0,0,0,0.7);
  display: flex; justify-content: center; align-items: center;
  z-index: 2000;
}
.modal-content {
  background: #1e1e1e;
  border-radius: 16px;
  padding: 32px;
  width: 70vw;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
}
.modal-content::-webkit-scrollbar{
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
.close-x:hover { color: #8e2de2; }
.film-details {
  display: flex;
  gap: 32px;
  align-items: stretch;
  min-height: 330px;
  height: 100%;
}
.film-poster {
  width: auto;
  min-width: 220px;
  height: 80%;
  min-height: 330px;
  max-height: 100%;
  object-fit: cover;
  border-radius: 12px;
  background: #222;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
  align-self: stretch;
  display: block;
}
.film-info {
  flex: 1 1 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  gap: 12px;
}
.film-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 8px;
}
.favorite-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  margin: 0;
  display: flex;
  align-items: center;
}
.film-header h2 {
  font-size: 2rem;
  margin: 0;
  color: #fff;
  font-weight: 700;
  line-height: 1.2;
}
.film-meta {
  display: flex;
  gap: 12px;
  font-size: 1.1rem;
  margin-bottom: 8px;
}
.meta.blue { color: #42a5f5; }
.meta.purple { color: #a259ec; }
.film-genres {
  margin-bottom: 8px;
}
.genre {
  display: inline-block;
  background: #222;
  color: #fff;
  border-radius: 8px;
  padding: 2px 10px;
  margin-right: 6px;
  font-size: 0.95rem;
}
.film-crew {
  font-size: 1rem;
  margin-bottom: 8px;
}
.film-rating {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
.film-description {
  font-size: 1rem;
  margin-top: 8px;
}

@media (max-width: 1200px) {
  .modal-content {
    width: 80vw;
    padding: 24px;
  }

  .film-details {
    flex-direction: column;
    gap: 24px;
    min-height: auto;
  }

  .film-poster {
    width: 100%;
    max-width: 300px;
    min-height: 250px;
    margin: 0 auto;
  }

  .film-header h2 {
    font-size: 1.8rem;
  }

  .film-meta {
    font-size: 1rem;
    flex-wrap: wrap;
  }

  .film-genres {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }

  .genre {
    font-size: 0.9rem;
    padding: 2px 8px;
  }

  .film-crew, .film-description {
    font-size: 0.95rem;
  }
}

@media (max-width: 768px) {
  .modal-content {
    width: 90vw;
    padding: 20px;
  }

  .film-details {
    flex-direction: column;
    gap: 20px;
    min-height: auto;
  }

  .film-poster {
    width: 100%;
    max-width: 300px;
    min-height: 250px;
    margin: 0 auto;
  }

  .film-header h2 {
    font-size: 1.5rem;
  }

  .film-meta {
    font-size: 0.9rem;
    flex-wrap: wrap;
  }

  .film-genres {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }

  .genre {
    font-size: 0.85rem;
    padding: 2px 8px;
  }

  .film-crew {
    font-size: 0.9rem;
  }

  .film-description {
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .modal-content {
    width: 95vw;
    padding: 16px;
  }

  .close-x {
    top: 12px;
    right: 16px;
    font-size: 1.8rem;
  }

  .film-poster {
    max-width: 250px;
    min-height: 200px;
  }

  .film-header h2 {
    font-size: 1.3rem;
  }

  .film-meta {
    font-size: 0.8rem;
  }

  .genre {
    font-size: 0.75rem;
    padding: 2px 6px;
  }

  .film-crew {
    font-size: 0.8rem;
  }

  .film-description {
    font-size: 0.8rem;
  }
}
</style>
