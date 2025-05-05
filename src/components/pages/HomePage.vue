<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useToast } from "vue-toastification";
const toast = useToast();
import { Swiper, SwiperSlide } from "swiper/vue";
import "swiper/css";
import "swiper/css/effect-coverflow";
import defaultPoster from "@/assets/film-poster-default.webp";
import { Autoplay } from "swiper/modules";
import { EffectCoverflow, Pagination } from "swiper/modules";
import RandomFilm from "../modals/RandomFilm.vue";
import MoviePickerModal from "../modals/MoviePickerModal.vue";
import PickedMovieModal from "../modals/PickedMovieModal.vue";
import IconRaiting from "../../components/icons/IconRaiting.vue";
import IconLeft from "../../components/icons/IconLeft.vue";
import IconRight from "../../components/icons/IconRight.vue";
import IconFavorite from "@/components/icons/IconFavorite.vue";
import FilmDetailsModal from '@/components/modals/FilmDetailsModal.vue'

const API_KEY = "54a2541709252b5e3de68b7642666940";
const BASE_URL = "https://api.themoviedb.org/3";

const showPicker = ref(false)
const showResults = ref(false)
const pickedMovies = ref([])
const pickedMoviesPage = ref(1)
const pickedMoviesTotalPages = ref(1)
const pickedMoviesQuery = ref(null)
const expanded = ref(false);
const recommendedMovies = ref([]);
const randomMovies = ref([]);
const showModal = ref(false);
const selectedMovie = ref({
  id: "",
  title: "",
  poster_path: "",
  genres: "",
  actors: "",
  description: "",
});
const similarMovies = ref([{ id: 1, title: "", poster: "" }]);
const favorites = ref(
  Array.isArray(JSON.parse(localStorage.getItem("favorites")))
    ? JSON.parse(localStorage.getItem("favorites"))
    : []
);
const currentSlide = ref(0);
const showDetails = ref(false)
const detailsMovie = ref(null)
const searchQuery = ref('')
const searchResults = ref([])

const isFavorite = (id) => {
  return favorites.value.some((f) => f.id === id);
};
const nextSlide = () => {
  if (currentSlide.value < recommendedMovies.value.length - 1) {
    currentSlide.value++;
  } else {
    currentSlide.value = 0;
  }
};

const prevSlide = () => {
  if (currentSlide.value > 0) {
    currentSlide.value--;
  } else {
    currentSlide.value = recommendedMovies.value.length - 1;
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
      .filter((movie) => movie);
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
            return null;
          }
        })
        .filter((movie) => movie)
    );

    recommendedMovies.value = detailedMovies.filter((movie) => movie);

    console.log(recommendedMovies);
  } catch (error) {
    console.error("Ошибка при получении фильмов:", error);
  }
};

const getPosterUrl = (path) => {
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
      id: movie.id,
      title: movie.title,
      poster_path: movie.poster_path
        ? `https://image.tmdb.org/t/p/w300${movie.poster_path}`
        : "https://via.placeholder.com/120x180?text=No+Image",
      genres: movieDetails.data.genres.map((genre) => genre.name).join(", "),
      actors: actorsResponse.data.cast
        .slice(0, 5)
        .map((actor) => actor.name)
        .join(", "),
      description: movie.overview,
      release_date: movieDetails.data.release_date,
      production_countries: movieDetails.data.production_countries,
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

const handlePick = async ({ genre, yearStart, yearEnd, country }) => {
  if (!genre || !yearStart || !yearEnd || !country) {
    console.error("Не все параметры выбраны");
    return;
  }
  pickedMovies.value = []
  pickedMoviesPage.value = 1
  pickedMoviesQuery.value = { genre, yearStart, yearEnd, country }
  await fetchPickedMovies()
  showPicker.value = false
  showResults.value = true
};

const fetchPickedMovies = async () => {
  const { genre, yearStart, yearEnd, country } = pickedMoviesQuery.value
  try {
    const response = await axios.get('https://api.themoviedb.org/3/discover/movie', {
      params: {
        api_key: API_KEY,
        language: 'ru-RU',
        with_genres: genre,
        'primary_release_date.gte': `${yearStart}-01-01`,
        'primary_release_date.lte': `${yearEnd}-12-31`,
        with_origin_country: country,
        sort_by: 'popularity.desc',
        page: pickedMoviesPage.value
      }
    })
    // Добавляем новые фильмы к уже найденным
    pickedMovies.value = [...pickedMovies.value, ...response.data.results]
    pickedMoviesTotalPages.value = response.data.total_pages
  } catch (error) {
    console.error('Ошибка при подборе фильмов:', error)
  }
}

const loadMorePickedMovies = async () => {
  pickedMoviesPage.value++
  await fetchPickedMovies()
}

const addToFavorites = (movie) => {
  const isAuth = localStorage.getItem("isAuthenticated") === "true";

  if (!isAuth) {
    toast.error("Чтобы добавить в избранное, войдите в аккаунт", {
      position: "bottom-center",
    });
    return;
  }

  const movieIndex = favorites.value.findIndex((f) => f.id === movie.id);

  if (movieIndex === -1) {
    favorites.value.push(movie);
    toast.success("Фильм добавлен в избранное 🎉", {
      position: "bottom-center",
    });
  } else {
    favorites.value.splice(movieIndex, 1);
    toast.success("Фильм удалён из избранного ❌", {
      position: "bottom-center",
    });
  }

  localStorage.setItem("favorites", JSON.stringify(favorites.value));
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

const onSearchInput = async () => {
  if (!searchQuery.value.trim()) {
    searchResults.value = []
    return
  }
  const { data } = await axios.get('https://api.themoviedb.org/3/search/movie', {
    params: {
      api_key: API_KEY,
      language: 'ru-RU',
      query: searchQuery.value,
      page: 1
    }
  })
  searchResults.value = data.results
}

const selectSearchedMovie = async (movie) => {
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
  searchResults.value = []
  searchQuery.value = ''
}

onMounted(() => {
  loadRandomMovies();
});
</script>

<template>
  <div class="card-main">
    <main class="home">
      <div class="search-bar-wrapper">
        <span class="search-icon">
          <svg width="22" height="22" fill="none" viewBox="0 0 24 24">
            <circle cx="11" cy="11" r="7" stroke="#42a5f5" stroke-width="2"/>
            <line x1="16.5" y1="16.5" x2="22" y2="22" stroke="#42a5f5" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </span>
        <input
          v-model="searchQuery"
          @input="onSearchInput"
          type="text"
          placeholder="Фильм как новый мир — открой его с MovieAs..."
          class="search-bar"
          autocomplete="off"
        />
        <ul v-if="searchResults.length && searchQuery" class="search-suggestions">
          <li
            v-for="movie in searchResults"
            :key="movie.id"
            @click="selectSearchedMovie(movie)"
          >
            <img :src="getPosterUrl(movie.poster_path)" alt="" class="search-thumb" />
            <span>{{ movie.title }} <span class="search-year">({{ getYear(movie.release_date) }})</span></span>
          </li>
        </ul>
      </div>

      <div class="carousel-wrapper">
        <Swiper
          :loop="true"
          :slides-per-view="3"
          :centered-slides="true"
          :space-between="20"
          :autoplay="{ delay: 3000, disableOnInteraction: false }"
          :modules="[Autoplay, EffectCoverflow, Pagination]"
          effect="coverflow"
          :coverflowEffect="{
            rotate: 0,
            stretch: 30,
            depth: 200,
            modifier: 1,
            scale: 1,
            slideShadows: false,
          }"
        >
          <SwiperSlide
            v-for="movie in randomMovies"
            :key="movie.id"
            @click="openDetails(movie)"
            style="cursor:pointer"
          >
            <img :src="movie.poster" :alt="movie.title" class="carousel-img" />
          </SwiperSlide>
        </Swiper>
      </div>

      <section class="buttons">
        <button @click="showPicker = true">Подобрать фильм</button>

       
        <button @click="openMovieModal">Случайный фильм</button>
      </section>
      <MoviePickerModal
          v-if="showPicker"
          :show="showPicker"
          @close="showPicker = false"
          @submit="handlePick"
        />

        <PickedMovieModal
        v-if="showResults"
        :show="showResults"
          :movies="pickedMovies"
          :canLoadMore="pickedMoviesPage < pickedMoviesTotalPages"
          @close="showResults = false"
          @loadMore="loadMorePickedMovies"
        />
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
          <div
            v-if="similarMovies.length < 3"
            class="similar-card add-card"
            @click="addMovieCard"
          >
            +
          </div>
        </div>
        <button class="select-movie" @click="fetchRecommendedMovies">
          Похожие фильмы
        </button>
      </section>

      <div v-if="recommendedMovies.length > 0" class="recommended-movies">
        <div class="slider-wrapper">
          <div class="nav-btn left">
            <button class="mb-4" @click="prevSlide" icon>
              <IconLeft />
            </button>
          </div>
          <div class="movie-slider">
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
                <v-img
                  :src="getPosterUrl(movie.poster_path)"
                  width="20vw"
                  max-width="400px"
                  class="mr-4 rounded"
                  cover
                ></v-img>
                <div class="d-flex flex-column flex-grow-1">
                  <div
                    class="d-flex flex-row justify-space-between align-center"
                  >
                    <h2 class="text-uppercase mb-1">{{ movie.title }}</h2>
                    <button
                      class="add-favorite-btn"
                      :class="{ save: isFavorite(movie.id) }"
                      @click="addToFavorites(movie)"
                    >
                      <IconFavorite :filled="isFavorite(movie.id)" />
                    </button>
                  </div>
                  <div class="text-blue mb-2">
                    {{ getYear(movie.release_date) }} •
                    {{ movie.production_countries?.[0]?.name || "—" }} •
                    {{ movie.runtime }} мин
                  </div>
                  <div class="mb-1">
                    <span class="text-grey">Жанры: </span>
                    {{ getGenres(movie.genres) }}
                  </div>
                  <div class="mb-1">
                    <span class="text-grey">Режиссёр: </span>
                    {{ getDirector(movie.credits?.crew) }}
                  </div>
                  <div class="mb-2">
                    <span class="text-grey">Актёры: </span>
                    {{ getTopActors(movie.credits?.cast) }}
                  </div>
                  <div class="mb-2 pa-0 d-flex align-center">
                    <IconRaiting />
                    <div class="d-flex align-center ml-2" style="gap: 20px">
                      <span style="font-size: 14px">{{
                        movie.vote_average
                      }}</span>
                    </div>
                  </div>
                  <div>
                    <div>
                      {{ movie.overview || "Увы, описания нет" }}
                    </div>
                  </div>
                </div>
              </v-card>
            </div>
          </div>
          <div class="nav-btn right">
            <button @click="nextSlide" icon>
              <IconRight />
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
  <FilmDetailsModal
    v-if="showDetails"
    :show="showDetails"
    :movie="detailsMovie"
    @close="closeDetails"
  />
</template>

<style scoped>
.card-main {
  background-color: #1c1c1e;
  border-radius: 20px;
  box-shadow: 0 1px 30px 5px rgba(77, 92, 255, 0.445);
  padding: 2rem;
  width: 90vw;
  margin: 2rem auto;
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
  margin: 10px;
  width: 100%;
  height: 90%;
  object-fit: cover;
  border-radius: 16px;
  box-shadow: 0px 10px 20px -5px rgba(77, 92, 255, 0.445);
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
  overflow: hidden;
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
  max-width: 1200px;
  min-height: 70vh;
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
  text-shadow: none;
}
.add-favorite-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 3px;
  transition: transform 0.2s;
  display: flex;
  align-items: center;
}

.add-favorite-btn .icon {
  /* убери fill отсюда, если используешь через проп filled */
}

.add-favorite-btn:hover {
  transform: scale(1.3);
}

.add-favorite-btn:active {
  transform: scale(0.95);
}

.save {
  fill: #003d80;
}

.search-bar-wrapper {
  position: relative;
  width: 100%;
  max-width: 820px;
  margin: 0 auto 0 auto;
  display: flex;
  align-items: center;
  background: rgba(34, 34, 34, 0.85);
  border-radius: 16px;
  box-shadow: 0 4px 24px 0 #44008722;
  transition: box-shadow 0.2s;
}
.search-bar-wrapper:focus-within {
  box-shadow: 0 0 0 3px #2d39e2aa;
}
.search-icon {
  position: absolute;
  left: 18px;
  z-index: 2;
  display: flex;
  align-items: center;
  pointer-events: none;
}
.search-bar {
  width: 100%;
  padding: 14px 18px 14px 48px;
  border-radius: 16px;
  border: none;
  background: transparent;
  color: #fff;
  font-size: 1.15rem;
  outline: none;
  transition: background 0.2s;
}
.search-bar::placeholder {
  color: #aac5ff;
  font-size: 1.08rem;
  opacity: 1;
}
.search-suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background: #181818;
  border-radius: 0 0 16px 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
  z-index: 10;
  list-style: none;
  margin: 0;
  padding: 0;
  max-height: 320px;
  overflow-y: auto;
}
.search-suggestions li {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 18px;
  cursor: pointer;
  transition: background 0.2s;
}
.search-suggestions li:hover {
  background: #001487;
}
.search-thumb {
  width: 40px;
  height: 60px;
  object-fit: cover;
  border-radius: 6px;
  background: #222;
}
.search-year {
  color: #42a5f5;
  font-size: 0.95em;
}

/* Медиа-запросы для адаптивности */
@media screen and (max-width: 1200px) {
  .card-main {
    width: 95vw;
    padding: 1rem;
    box-shadow: none;
  }
  
  .carousel-wrapper {
    width: 90%;
  }

  .similar-card {
    width: calc(33.33% - 20px);
    min-height: auto;
    max-height: 300px;
    display: flex;
    flex-direction: column;
    padding: 8px;
    background-color: #252525;
    border-radius: 12px;
  }

  .similar-card img {
    width: 100%;
    height: 240px;
    object-fit: cover;
    border-radius: 8px;
    margin-bottom: 8px;
  }

  .similar-card input {
    width: 100%;
    font-size: 13px;
    padding: 8px;
    margin-bottom: 0;
    background: #1c1c1e;
    color: #fff;
    border: 1px solid #333;
    border-radius: 6px;
  }

  .suggestions {
    width: 100%;
    left: 0;
    max-height: 200px;
    margin-top: 4px;
    background: #1c1c1e;
    border: 1px solid #333;
    border-radius: 6px;
  }

  .suggestions li {
    padding: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid #333;
  }

  .suggestions li:last-child {
    border-bottom: none;
  }

  .suggestions img {
    width: 30px;
    height: 45px;
    object-fit: cover;
    border-radius: 4px;
  }

  .movie-card {
    flex-direction: column;
    align-items: center;
    text-align: left;
    box-shadow: none !important;
  }

  .movie-card .v-img {
    width: 100% !important;
    max-width: 250px !important;
    margin-bottom: 15px;
  }

  .movie-card h2 {
    font-size: 1.1rem;
    margin-bottom: 8px;
  }

  .movie-card .text-blue {
    font-size: 0.85rem;
  }

  .movie-card .text-grey {
    font-size: 0.8rem;
  }

  .movie-card div {
    font-size: 0.85rem;
    line-height: 1.4;
  }

  .movie-card .mb-1 {
    margin-bottom: 4px;
  }

  .movie-card .mb-2 {
    margin-bottom: 8px;
  }

  .movie-card .d-flex {
    gap: 10px !important;
  }

  .nav-btn button {
    width: 34px;
    height: 34px;
    padding: 7px;
  }

  .nav-btn button svg {
    width: 19px;
    height: 19px;
  }

  .search-bar-wrapper {
    width: 90%;
  }

  .search-bar {
    font-size: 0.9rem;
  }

  .search-bar::placeholder {
    font-size: 0.85rem;
  }

  .search-suggestions {
    max-height: 300px;
  }

  .search-suggestions li {
    padding: 10px 15px;
  }

  .search-thumb {
    width: 35px;
    height: 52px;
  }
}

@media screen and (max-width: 768px) {
  .card-main {
    width: 95vw;
    padding: 1rem;
    box-shadow: none;
  }

  .home {
    padding: 1rem;
  }

  .carousel-wrapper {
    width: 95%;
  }

  .buttons {
    flex-direction: column;
    width: 100%;
  }

  .buttons button {
    width: 100%;
  }

  .similar {
    padding: 20px 10px;
  }

  .similar h2 {
    font-size: 1.2rem;
    margin-bottom: 15px;
  }

  .similar-cards {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
  }

  .similar-card {
    width: calc(50% - 8px);
    height: auto;
    min-height: auto;
    padding: 8px;
    background-color: #252525;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
  }

  .similar-card img {
    width: 100%;
    height: 120px;
    object-fit: cover;
    border-radius: 8px;
    margin-bottom: 8px;
  }

  .similar-card input {
    width: 100%;
    font-size: 12px;
    padding: 6px 8px;
    border-radius: 6px;
    background: #1c1c1e;
    color: #fff;
    border: 1px solid #333;
    margin-bottom: 0;
  }

  .suggestions {
    width: 100%;
    left: 0;
    font-size: 11px;
    background: #1c1c1e;
    border: 1px solid #333;
    border-radius: 6px;
    margin-top: 4px;
    max-height: 180px;
  }

  .select-movie {
    margin-top: 20px;
    padding: 10px 20px;
    font-size: 14px;
  }

  /* Стили для навигационных стрелок */
  .nav-btn button {
    width: 32px;
    height: 32px;
    padding: 6px;
    background-color: rgba(77, 92, 255, 0.8);
  }

  .nav-btn button svg {
    width: 18px;
    height: 18px;
  }

  /* Стили для карточек результатов подбора */
  .movie-card {
    padding: 12px !important;
    flex-direction: column;
    align-items: center;
    text-align: left;
    box-shadow: none !important;
  }

  .movie-card .v-img {
    width: 100% !important;
    max-width: 200px !important;
    margin-bottom: 12px;
    border-radius: 8px;
  }

  .movie-card h2 {
    font-size: 1rem;
    margin-bottom: 6px;
    line-height: 1.2;
  }

  .movie-card .text-blue {
    font-size: 0.8rem;
    margin-bottom: 4px;
  }

  .movie-card .text-grey {
    font-size: 0.75rem;
    color: #999;
  }

  .movie-card .mb-1 {
    margin-bottom: 3px;
    font-size: 0.75rem;
  }

  .movie-card .mb-2 {
    margin-bottom: 6px;
    font-size: 0.75rem;
  }

  .movie-card .d-flex {
    gap: 8px !important;
  }

  .movie-card .add-favorite-btn {
    transform: scale(0.8);
  }

  .search-bar {
    font-size: 0.85rem;
  }

  .search-bar::placeholder {
    font-size: 0.8rem;
  }
}

@media screen and (max-width: 480px) {
  .card-main {
    margin: 0.5rem auto;
    padding: 0.5rem;
    box-shadow: none;
  }

  .home {
    padding: 0.5rem;
  }

  .carousel-wrapper {
    padding: 5px;
  }

  .similar {
    padding: 15px 8px;
  }

  .similar h2 {
    font-size: 1.1rem;
    margin-bottom: 12px;
  }

  .similar-cards {
    gap: 6px;
  }

  .similar-card {
    width: calc(50% - 6px);
    padding: 6px;
  }

  .similar-card img {
    height: 100px;
    margin-bottom: 6px;
  }

  .similar-card input {
    font-size: 11px;
    padding: 5px 6px;
  }

  .suggestions {
    max-height: 160px;
  }

  .select-movie {
    margin-top: 15px;
    padding: 8px 16px;
    font-size: 12px;
  }

  .search-bar {
    font-size: 0.8rem;
    padding: 10px 10px 10px 40px;
  }

  .search-bar::placeholder {
    font-size: 0.55rem;
  }

  .movie-card {
    padding: 8px !important;
    box-shadow: none !important;
  }

  .movie-card .v-img {
    max-width: 150px !important;
    margin-bottom: 8px;
  }

  .movie-card h2 {
    font-size: 0.9rem;
    margin-bottom: 4px;
  }

  .movie-card .text-blue {
    font-size: 0.7rem;
    margin-bottom: 3px;
  }

  .movie-card .text-grey {
    font-size: 0.65rem;
  }

  .movie-card .mb-1 {
    margin-bottom: 2px;
    font-size: 0.7rem;
  }

  .movie-card .mb-2 {
    margin-bottom: 4px;
    font-size: 0.7rem;
  }

  .movie-card div {
    font-size: 0.7rem;
    line-height: 1.2;
  }

  .movie-card .d-flex {
    gap: 6px !important;
  }

  .movie-card .add-favorite-btn {
    transform: scale(0.7);
  }

  .movie-card .pa-4 {
    padding: 8px !important;
  }

  /* Стили для контейнера с карточками */
  .movie-slider {
    width: 100%;
    padding: 0 4px;
  }

  .movie-slide {
    padding: 8px 4px;
  }

  /* Стили для навигационных стрелок */
  .nav-btn button {
    width: 28px;
    height: 28px;
    padding: 5px;
  }

  .nav-btn button svg {
    width: 16px;
    height: 16px;
  }
}

/* Стили для Swiper адаптивности */
@media screen and (max-width: 1200px) {
  .swiper-slide {
    width: 300px !important;
  }
}

@media screen and (max-width: 768px) {
  .swiper-slide {
    width: 250px !important;
  }
}

@media screen and (max-width: 480px) {
  .swiper-slide {
    width: 200px !important;
  }
}
</style>
