<template>
  <div v-if="showModal" class="modal">
    <div class="modal-content">
      <span class="close-btn" @click="closeModal">&times;</span>
      <div class="film-details">
        <img :src="getImageUrl(selectedMovie.poster_path)" class="film-poster" />
        <div class="film-info">
          <div class="film-header">
            <button class="favorite-btn" @click="addToFavorites">
              <IconFavorite :filled="isFavorite" />
            </button>
            <h2>{{ selectedMovie.title }}</h2>
          </div>
          <div class="film-meta">
            <span class="meta blue">{{ getYear(selectedMovie.release_date) }}</span>
            <span class="meta blue"> {{ getCountry(selectedMovie) }}</span>
          </div>
          <div class="film-genres">
            <span v-if="selectedMovie.genres"><b>Жанры:</b> {{ selectedMovie.genres }}</span>
          </div>
          <div class="film-crew">
            <div v-if="selectedMovie.actors"><b>Актёры:</b> {{ selectedMovie.actors }}</div>
          </div>
          <div class="film-description">
            <b>Описание:</b>
            <p>{{ selectedMovie.description || "Нет описания" }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
  <v-snackbar v-model="snackbar" timeout="3000" color="green" location="top right">
  {{ snackbarText }}
</v-snackbar>
</template>

<script setup>
import { ref, defineProps, defineEmits, onMounted, computed, watch } from "vue";
import { useToast } from "vue-toastification";
import IconFavorite from '@/components/icons/IconFavorite.vue'
import defaultPoster from '@/assets/film-poster-default.webp'

const toast = useToast();

const props = defineProps({
  showModal: Boolean,
  selectedMovie: Object,
});

const emit = defineEmits(["update:showModal"]);

const closeModal = () => {
  emit("update:showModal", false);
};

const getImageUrl = (path) => {
  return path
    ? `https://image.tmdb.org/t/p/w500${path}`
    : defaultPoster
}
const getYear = (date) => date ? new Date(date).getFullYear() : '—'
const getCountry = (movie) => movie.production_countries?.[0]?.name || '—'

// Избранное
const isFavorite = ref(false)

watch(
  () => props.selectedMovie,
  (movie) => {
    if (!movie || !movie.id) {
      isFavorite.value = false
      return
    }
    const favs = JSON.parse(localStorage.getItem('favorites') || '[]')
    isFavorite.value = favs.some(f => f.id === movie.id)
  },
  { immediate: true }
)

const addToFavorites = () => {
  if (!props.selectedMovie || !props.selectedMovie.id) return;

  // Проверка на авторизацию
  const isAuth = localStorage.getItem('isAuthenticated') === 'true';
  if (!isAuth) {
    toast.error('Чтобы добавить в избранное, войдите в аккаунт', {
      position: 'bottom-center'
    });
    return;
  }

  let favs = JSON.parse(localStorage.getItem('favorites') || '[]')
  const idx = favs.findIndex(f => f.id === props.selectedMovie.id)
  if (idx === -1) {
    favs.push(props.selectedMovie)
    localStorage.setItem('favorites', JSON.stringify(favs))
    isFavorite.value = true
    toast.success("Фильм добавлен в избранное 🎉", { position: "bottom-center" })
  } else {
    toast.info("Фильм уже в избранном 🤔", { position: "bottom-center" })
  }
}
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh;
  background-color: rgba(0, 0, 0, 0.7);
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
.close-btn {
  position: absolute;
  top: 18px; right: 24px;
  font-size: 2.2rem;
  color: #fff;
  cursor: pointer;
  z-index: 2;
  transition: color 0.2s;
}
.close-btn:hover { color: #8e2de2; }
.film-details {
  display: flex;
  gap: 32px;
  align-items: stretch;
  min-height: 330px;
}
.film-poster {
  width: auto;
  min-width: 220px;
  height: 100%;
  min-height: 330px;
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
.film-genres, .film-crew, .film-description {
  font-size: 1rem;
  margin-bottom: 8px;
}

@media (max-width: 1200px) {
  .modal-content {
    width: 80vw;
    padding: 24px;
  }

  .film-details {
    gap: 24px;
  }

  .film-poster {
    min-width: 200px;
    min-height: 300px;
  }

  .film-header h2 {
    font-size: 1.8rem;
  }

  .film-meta {
    font-size: 1rem;
  }

  .film-genres, .film-crew, .film-description {
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

  .film-genres, .film-crew, .film-description {
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .modal-content {
    width: 95vw;
    padding: 16px;
  }

  .close-btn {
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

  .film-genres, .film-crew, .film-description {
    font-size: 0.8rem;
  }
}
</style>
