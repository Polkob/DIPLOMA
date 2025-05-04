<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { Swiper, SwiperSlide } from "swiper/vue";
import "swiper/css";
import "swiper/css/effect-coverflow";
import defaultPoster from "@/assets/film-poster-default.webp";
import { Autoplay } from "swiper/modules";
import { EffectCoverflow, Pagination } from "swiper/modules";
import RandomFilm from "../modals/RandomFilm.vue";
import IconRaiting from "../../components/icons/IconRaiting.vue";
import IconLeft from "../../components/icons/IconLeft.vue";
import IconRight from "../../components/icons/IconRight.vue";

const API_KEY = "54a2541709252b5e3de68b7642666940";
const BASE_URL = "https://api.themoviedb.org/3";

const expanded = ref(false);
const recommendedMovies = ref([]);
const randomMovies = ref([]);
const showModal = ref(false);
const selectedMovie = ref({
  title: "",
  poster: "",
  genres: "",
  actors: "",
  description: "",
});
const similarMovies = ref([{ id: 1, title: "", poster: "" }]);

const currentSlide = ref(0);

const nextSlide = () => {
  if (currentSlide.value < recommendedMovies.value.length - 1) {
    currentSlide.value++;
  } else {
    currentSlide.value = 0; // Возвращаемся к первому слайду, если дошли до конца
  }
};

const prevSlide = () => {
  if (currentSlide.value > 0) {
    currentSlide.value--;
  } else {
    currentSlide.value = recommendedMovies.value.length - 1; // Возвращаемся к последнему слайду, если на первом
  }
};

const fetchRecommendedMovies = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/movie/popular`, {
      params: {
        api_key: API_KEY,
        language: "ru-RU",
        page: Math.floor(Math.random() * 50) + 1,
      },
    });

    const basicMovies = response.data.results
      .slice(0, 10)
      .filter((movie) => movie); // Только 10 фильмов

    // Получаем расширенные данные по каждому фильму
    const detailedMovies = await Promise.all(
      basicMovies
        .map(async (movie) => {
          try {
            const detailedResponse = await axios.get(
              `${BASE_URL}/movie/${movie.id}`,
              {
                params: {
                  api_key: API_KEY,
                  language: "ru-RU",
                  append_to_response: "credits",
                },
              }
            );
            return detailedResponse.data;
          } catch (err) {
            console.error(
              `Ошибка при получении деталей фильма ${movie.id}:`,
              err
            );
            return null; // Пропустить, если ошибка
          }
        })
        .filter((movie) => movie)
    );

    // Фильтруем только успешные запросы
    recommendedMovies.value = detailedMovies.filter((movie) => movie);
    console.log(recommendedMovies);
  } catch (error) {
    console.error("Ошибка при получении фильмов:", error);
  }
};

const getPosterUrl = (path) => {
  console.log(path);
  return path
    ? `https://image.tmdb.org/t/p/w500${path}`
    : "https://via.placeholder.com/500x750?text=Нет+постера";
};
const getDirector = (crew) => {
  const director = crew?.find((member) => member.job === "Director");
  return director ? director.name : "—";
};

const getTopActors = (cast) => {
  return (
    cast
      ?.slice(0, 3)
      .map((actor) => actor.name)
      .join(", ") || "—"
  );
};
const getGenres = (genres) => {
  if (!Array.isArray(genres)) return "—";
  return genres.map((genre) => genre.name).join(", ");
};
const getYear = (date) => {
  return date ? new Date(date).getFullYear() : "Неизвестно";
};
const loadRandomMovies = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/movie/popular`, {
      params: {
        api_key: API_KEY,
        language: "ru-RU",
        page: Math.floor(Math.random() * 50) + 1,
      },
    });

    randomMovies.value = response.data.results.slice(0, 20).map((movie) => ({
      id: movie.id,
      title: movie.title,
      poster: movie.poster_path
        ? `https://image.tmdb.org/t/p/w300${movie.poster_path}`
        : "https://via.placeholder.com/120x180?text=No+Image",
    }));
  } catch (error) {
    console.error("Ошибка загрузки фильмов:", error);
  }
};
const openMovieModal = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/movie/popular`, {
      params: {
        api_key: API_KEY,
        language: "ru-RU",
        page: Math.floor(Math.random() * 50) + 1,
      },
    });

    const movie =
      response.data.results[
        Math.floor(Math.random() * response.data.results.length)
      ];

    const movieDetails = await axios.get(`${BASE_URL}/movie/${movie.id}`, {
      params: {
        api_key: API_KEY,
        language: "ru-RU",
      },
    });

    const actorsResponse = await axios.get(
      `${BASE_URL}/movie/${movie.id}/credits`,
      {
        params: {
          api_key: API_KEY,
          language: "ru-RU",
        },
      }
    );

    selectedMovie.value = {
      title: movie.title,
      poster: movie.poster_path
        ? `https://image.tmdb.org/t/p/w300${movie.poster_path}`
        : "https://via.placeholder.com/120x180?text=No+Image",
      genres: movieDetails.data.genres.map((genre) => genre.name).join(", "),
      actors: actorsResponse.data.cast
        .slice(0, 5)
        .map((actor) => actor.name)
        .join(", "),
      description: movie.overview,
    };

    showModal.value = true;
  } catch (error) {
    console.error("Ошибка при загрузке данных о фильме:", error);
  }
};
const addMovieCard = () => {
  if (similarMovies.value.length < 3) {
    similarMovies.value.push({
      id: Date.now(),
      title: "",
      poster: "",
      query: "",
      suggestions: [],
    });
  }
};

const searchMovies = async (movie, index) => {
  if (!movie.query.trim()) {
    similarMovies.value[index].suggestions = [];
    return;
  }
  try {
    const response = await axios.get(`${BASE_URL}/search/movie`, {
      params: {
        api_key: API_KEY,
        language: "ru-RU",
        query: movie.query,
      },
    });

    similarMovies.value[index].suggestions = response.data.results
      .slice(0, 5)
      .map((result) => ({
        id: result.id,
        title: result.title,
        poster: result.poster_path
          ? `https://image.tmdb.org/t/p/w300${result.poster_path}`
          : "https://via.placeholder.com/100x150?text=No+Image",
      }));
  } catch (error) {
    console.error("Ошибка поиска фильмов:", error);
  }
};

const selectSuggestion = (index, suggestion) => {
  similarMovies.value[index].title = suggestion.title;
  similarMovies.value[index].poster = suggestion.poster;
  similarMovies.value[index].query = "";
  similarMovies.value[index].suggestions = [];
};

const pickMovies = () => {
  console.log("Подбираем похожие фильмы...");
};

onMounted(() => {
  loadRandomMovies();
});
</script>

<template>
  <div class="card-main">
    <main class="home">
      <span class="span-citata">
        Каждый фильм — это новый мир. Найди свой.
      </span>

      <div class="carousel-wrapper">
        <Swiper
          :effect="'coverflow'"
          :grabCursor="true"
          :centeredSlides="true"
          :slidesPerView="3"
          :coverflowEffect="{
            rotate: 0,
            stretch: 30,
            depth: 200,
            modifier: 1,
            scale: 1,
            slideShadows: false,
          }"
          :pagination="{
            el: '.swiper-pagination',
            clickable: true,
          }"
          :navigation="{
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
          }"
          :modules="[Autoplay, EffectCoverflow, Pagination]"
          :autoplay="{ delay: 3000, disableOnInteraction: false }"
          space-between="20"
          loop
        >
          <SwiperSlide v-for="movie in randomMovies" :key="movie.id">
            <img :src="movie.poster" :alt="movie.title" class="carousel-img" />
          </SwiperSlide>
        </Swiper>
      </div>

      <section class="buttons">
        <button @click="pickMovies">Подобрать фильм</button>
        <button @click="openMovieModal">Случайный фильм</button>
      </section>

      <RandomFilm
        :showModal="showModal"
        :selectedMovie="selectedMovie"
        @update:showModal="showModal = $event"
      />
      <section class="similar">
        <h2>Похожие фильмы</h2>
        <div class="similar-cards">
          <div
            v-for="(movie, index) in similarMovies"
            :key="movie.id"
            class="similar-card"
          >
            <!-- Карточка фильма -->
            <img :src="movie.poster || defaultPoster" alt="Poster" />
            <div class="input-wrapper">
              <input
                type="text"
                v-model="movie.query"
                @input="searchMovies(movie, index)"
                placeholder="Введите название фильма"
              />
              <ul v-if="movie?.suggestions?.length" class="suggestions">
                <li
                  v-for="suggestion in movie.suggestions"
                  :key="suggestion.id"
                  @click="selectSuggestion(index, suggestion)"
                >
                  <img :src="suggestion.poster || defaultPoster" alt="Poster" />
                  {{ suggestion.title }}
                </li>
              </ul>
            </div>
          </div>

          <!-- Кнопка добавления -->
          <div
            v-if="similarMovies.length < 3"
            class="similar-card add-card"
            @click="addMovieCard"
          >
            +
          </div>
        </div>

        <!-- Кнопка внизу для подбора фильма -->
        <button class="select-movie" @click="fetchRecommendedMovies">
          Подобрать фильм
        </button>
      </section>

      <div v-if="recommendedMovies.length > 0" class="recommended-movies">
        <div class="slider-wrapper">
          <div class="nav-btn left">
            <button class="mb-4" @click="prevSlide" icon>
              <IconLeft />
            </button>
          </div>
          <!-- Контейнер для слайдов -->
          <div class="movie-slider">
            <!-- Слайды фильмов -->
            <div
              class="movie-slide"
              v-for="(movie, index) in recommendedMovies"
              :key="movie.id"
              :style="{ transform: `translateX(-${currentSlide * 100}%)` }"
            >
              <v-card
                class="d-flex pa-4 mb-4 movie-card"
                color="black"
                dark
                max-width="1200"
              >
                <!-- Постер -->
                <v-img
                  :src="getPosterUrl(movie.poster_path)"
                  width="20vw"
                  max-width="400px"
                  class="mr-4 rounded"
                  cover
                ></v-img>

                <!-- Информация -->
                <div class="d-flex flex-column flex-grow-1">
                  <!-- Название -->
                  <h2 class="text-uppercase mb-1">{{ movie.title }}</h2>

                  <!-- Год / Страна / Длительность -->
                  <div class="text-blue mb-2">
                    {{ getYear(movie.release_date) }} •
                    {{ movie.production_countries?.[0]?.name || "—" }} •
                    {{ movie.runtime }} мин
                  </div>

                  <!-- Жанры -->
                  <div class="mb-1">
                    <span class="text-grey">Жанры: </span>
                    {{ getGenres(movie.genres) }}
                  </div>

                  <!-- Режиссёр -->
                  <div class="mb-1">
                    <span class="text-grey">Режиссёр: </span>
                    {{ getDirector(movie.credits?.crew) }}
                  </div>

                  <!-- Актёры -->
                  <div class="mb-2">
                    <span class="text-grey">Актёры: </span>
                    {{ getTopActors(movie.credits?.cast) }}
                  </div>

                  <!-- Рейтинг -->
                  <div class="mb-2 pa-0 d-flex align-center">
                    <IconRaiting />
                    <div class="d-flex align-center ml-2" style="gap: 20px">
                      <span style="font-size: 14px">{{
                        movie.vote_average
                      }}</span>
                    </div>
                  </div>

                  <!-- Описание -->
                  <div>
                    <div>
                      {{ movie.overview || "Увы, описания нет" }}
                    </div>
                  </div>
                </div>
              </v-card>
            </div>
          </div>

          <!-- Навигационные кнопки -->
          <div class="nav-btn right">
            <button @click="nextSlide" icon>
              <IconRight />
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.card-main {
  background-color: #1c1c1e; /* Темная подложка */
  border-radius: 20px; /* Закругленные углы */
  box-shadow: 0 1px 30px 5px rgba(77, 92, 255, 0.445); /* Светлая тень */
  padding: 2rem;
  width: 90vw;
  margin: 2rem auto; /* Центрируем */
}

.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  padding: 2rem;
}

.carousel-wrapper {
  border-radius: 20px;
  padding: 20px;
  width: 80%;
  max-width: 1400px;
  overflow: hidden;
}

.carousel-img {
  margin: 20px;
  width: 100%;
  height: 90%;
  object-fit: cover;
  border-radius: 16px;
  box-shadow: 0px 10px 20px -5px rgba(77, 92, 255, 0.445); /* Подсветка снизу */
}

.swiper-slide:hover .carousel-img {
  transform: scale(0.95);
  box-shadow: 0px 15px 30px -5px rgba(77, 92, 255, 0.6);
}

.buttons {
  display: flex;
  gap: 1.5rem;
}

.buttons button {
  background-color: #440087;
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 10px;
  font-size: 1rem;
  cursor: pointer;
  transition: 0.3s;
}

.buttons button:hover {
  background-color: #5f0aad;
}

.similar {
  padding: 40px 20px;
  background-color: #1c1c1e;
  border-radius: 16px;
  margin: 20px 0;
}

.similar h2 {
  text-align: center;
  margin-bottom: 30px;
  font-size: 28px;
}

.similar-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.similar-card {
  width: 20vw;
  height: 50vh;
  background-color: #252525;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 12px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.similar-card:hover {
  transform: translateY(-5px);
}

.similar-card img {
  width: 13vw;
  height: 38vh;
  object-fit: cover;
  border-radius: 12px;
  margin-bottom: 15px;
}

.similar-card input {
  width: 15vw;
  padding: 10px;
  margin-bottom: 10px;
  font-size: 16px;

  box-shadow: 0px 0px 20px rgba(77, 92, 255, 0.445);
  border-radius: 8px;
}
.similar-card input:focus {
  box-shadow: 0px 0px 20px rgba(65, 144, 255, 0.445);
}
.suggestions {
  position: absolute;
  top: 100%;
  left: 25px;
  width: 15vw;
  background-color: #252525;
  border: 1px solid #ddd;
  border-radius: 12px;
  box-shadow: 0px 0px 20px rgba(65, 144, 255, 0.445);
  margin-top: 8px;
  list-style: none;
  padding: 8px 0;
  z-index: 1000;
  max-height: 300px;
  overflow-y: auto;
}
.suggestions::-webkit-scrollbar {
  display: none;
}
/* Элементы внутри списка */
.suggestions li {
  display: flex;
  font-size: 12px;
  align-items: center;
  gap: 10px;
  padding: 5px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.suggestions li:hover {
  background-color: #464646;
}

.suggestions img {
  width: 40px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
}

.input-wrapper {
  position: relative;
  width: 100%;
}

.add-card {
  justify-content: center;
  align-items: center;
  font-size: 48px;
  color: #ffffff;
  cursor: pointer;
  border: 2px dashed #aaa;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.add-card:hover {
  background-color: #484848;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.select-movie {
  margin-top: 30px;
  display: block;
  margin-left: auto;
  margin-right: auto;
  background-color: #007bff;
  color: white;
  font-size: 18px;
  padding: 12px 30px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.select-movie:hover {
  background-color: #0056b3;
}

.movie-results {
  margin-top: 3rem;
  width: 100%;
}
.movie-slider {
  display: flex;
  transition: transform 0.5s ease-in-out;
  overflow: hidden; /* Прячет лишний контент, выходящий за пределы */
}

.movie-slide {
  flex: 0 0 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 30px;
}

.movie-card {
  width: 100%;
  max-width: 1200px; /* Ограничиваем максимальную ширину карточки */
  min-height: 70vh; /* Ограничиваем высоту карточки */
  display: flex;
  box-shadow: 0 1px 30px 5px rgba(77, 92, 255, 0.445);
}

.navigation-buttons {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.navigation-buttons .v-btn {
  background-color: #000;
  color: #fff;
  margin: 0 10px;
  border-radius: 50%;
}
.text-blue {
  color: #42a5f5;
}
.text-grey {
  color: #6d6d6d;
}
.text-uppercase {
  text-transform: uppercase;
}
.line-clamp {
  display: -webkit-box;
  -webkit-line-clamp: 5;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.slider-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.movie-slider {
  width: 80vw;
  max-width: 1200px;
}

.nav-btn button {
  background-color: rgba(77, 92, 255, 0.8);
  border: none;
  border-radius: 50%;
  padding: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.nav-btn button:hover {
  background-color: rgba(77, 92, 255, 1);
  transform: scale(1.1);
}

.nav-btn button:focus {
  outline: none;
}
.recommended-movies {
  width: 90vw;
}
.span-citata {
  font-size: 1.2rem;
  font-weight: 400;
  color: #424242;
  text-align: center;
  display: block;
  margin: 10px 0;
  font-style: italic;
}
</style>
