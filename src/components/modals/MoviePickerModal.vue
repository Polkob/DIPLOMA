<template>
    <div v-if="show" class="modal-backdrop">
      <div class="modal">
        <h2>Подбор фильма — шаг {{ step }}</h2>
  
        <div v-if="step === 1">
          <label for="genre">Жанр:</label>
          <select v-model="genre">
            <option disabled value="">Выберите жанр</option>
            <option v-for="g in genres" :key="g">{{ g }}</option>
          </select>
        </div>
  
        <div v-else-if="step === 2">
          <label for="year">Год выпуска:</label>
          <input v-model="year" type="number" min="1900" max="2025" />
        </div>
  
        <div v-else-if="step === 3">
          <label for="country">Страна:</label>
          <select v-model="country">
            <option disabled value="">Выберите страну</option>
            <option v-for="c in countries" :key="c">{{ c }}</option>
          </select>
        </div>
  
        <div class="modal-actions">
          <button v-if="step > 1" @click="step--">Назад</button>
          <button v-if="step < 3" @click="step++" :disabled="!canProceed">Далее</button>
          <button v-else @click="submit" :disabled="!canProceed">Подобрать</button>
          <button @click="close">Отмена</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, watch } from 'vue'
  
  const props = defineProps({
    show: Boolean
  })
  const emit = defineEmits(['close', 'submit'])
  
  const step = ref(1)
  const genre = ref('')
  const year = ref('')
  const country = ref('')
  
  const genres = {
  'Боевик': 28,
  'Комедия': 35,
  'Драма': 18,
  'Фэнтези': 12,
  'Ужасы': 27
};
const countries = {
  'США': 'US',
  'Россия': 'RU',
  'Франция': 'FR',
  'Япония': 'JP',
  'Корея': 'KR'
};
  
  const canProceed = computed(() => {
    if (step.value === 1) return genre.value
    if (step.value === 2) return year.value
    if (step.value === 3) return country.value
    return false
  })
  
  const close = () => emit('close')
  
  const submit = () => {
    emit('submit', {
      genre: genre.value,
      year: year.value,
      country: country.value
    })
    close()
  }
  
  // сброс при открытии заново
  watch(() => props.show, (val) => {
    if (val) {
      step.value = 1
      genre.value = ''
      year.value = ''
      country.value = ''
    }
  })
  </script>
  
  <style scoped>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .modal {
    background: rgb(0, 0, 0);
    padding: 20px;
    border-radius: 12px;
    width: 400px;
  }
  .modal-actions {
    margin-top: 20px;
    display: flex;
    justify-content: space-between;
  }
  </style>
  