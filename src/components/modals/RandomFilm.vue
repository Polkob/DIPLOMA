<template>
  <div v-if="showModal" class="modal">
    <div class="modal-content">
      <span class="close-btn" @click="closeModal">&times;</span>
      <div class="movie-card">
        <img
          :src="selectedMovie.poster_path"
          :alt="selectedMovie.title"
          class="movie-poster"
        />
        <div class="movie-info">
          <h2>{{ selectedMovie.title }}</h2>
          <p><strong>Жанры:</strong> {{ selectedMovie.genres }}</p>
          <p><strong>Актеры:</strong> {{ selectedMovie.actors }}</p>
          <p><strong>Описание:</strong> {{ selectedMovie.description }}</p>
          <button class="favorite-btn" @click="addToFavorites">
            <i class="fas fa-star"></i> Добавить в избранное
          </button>
        </div>
      </div>
    </div>
  </div>
  <v-snackbar v-model="snackbar" timeout="3000" color="green" location="top right">
  {{ snackbarText }}
</v-snackbar>

</template>

<script setup>
import { ref, defineProps, defineEmits, onMounted } from "vue";
import { useToast } from "vue-toastification";
const toast = useToast();

const props = defineProps({
  showModal: Boolean,
  selectedMovie: Object,
});

const emit = defineEmits(["update:showModal"]);

const closeModal = () => {
  emit("update:showModal", false);
};

const addToFavorites = () => {
  const isAuth = localStorage.getItem('isAuthenticated') === 'true';

  if (!isAuth) {
    toast.error('Чтобы добавить в избранное, войдите в аккаунт', {
      position: 'bottom-center'
    });
    return;
  }
  if (props.selectedMovie) {
  const currentFavorites = JSON.parse(localStorage.getItem("favorites")) || [];

  if (!currentFavorites.find(f => f.id === props.selectedMovie.id)) {
    currentFavorites.push(props.selectedMovie);
    localStorage.setItem("favorites", JSON.stringify(currentFavorites));
    toast.success("Фильм добавлен в избранное 🎉", {
      position: 'bottom-center'
    });
  } else {
    toast.info("Фильм уже в избранном 🤔", {
      position: 'bottom-center'
    });
  }
}
};


</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-in-out;
}

.modal-content {
  background-color: #1e1e1e;
  border-radius: 12px;
  padding: 20px;
  width: 80%;
  max-width: 900px;
  display: flex;
  gap: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  transform: translateY(-50px);
  animation: slideIn 0.5s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    transform: translateY(-50px);
  }
  to {
    transform: translateY(0);
  }
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 35px;
  cursor: pointer;
  color: white;
  transition: transform 0.2s;
}

.close-btn:hover {
  transform: rotate(90deg);
}

.movie-card {
  display: flex;
  gap: 20px;
}

.movie-poster {
  width: 220px;
  height: 330px;
  border-radius: 12px;
  object-fit: cover;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.movie-info {
  flex: 1;
  color: white;
}

h2 {
  font-size: 24px;
  margin-bottom: 10px;
  color: #fff;
}

p {
  margin: 5px 0;
  font-size: 14px;
  line-height: 1.6;
}

.favorite-btn {
  background-color: #440087;
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 10px;
  font-size: 1rem;
  cursor: pointer;
  transition: 0.3s;
}

.favorite-btn:hover {
  background-color: #5f0aad;
}
</style>
