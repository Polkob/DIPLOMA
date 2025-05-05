<template>
    <div v-if="show" class="modal-backdrop">
      <div class="modal-content">
  
        <div v-if="step === 1">
          <label>Выберите жанр</label>
          <div class="choice-table">
            <div
              v-for="(code, name) in genres"
              :key="code"
              :class="['choice-row', { selected: genre === code }]"
              @click="selectGenre(code)"
            >
              {{ name }}
            </div>
          </div>
        </div>
  
        <div v-else-if="step === 2">
          <label>Год выпуска</label>
          <div class="choice-table year-choice-table">
            <div class="year-range-center">
              <input
                type="range"
                min="1900"
                max="2025"
                v-model.number="yearStart"
                :step="1"
                @input="fixYearRange"
              />
              <input
                type="range"
                min="1900"
                max="2025"
                v-model.number="yearEnd"
                :step="1"
                @input="fixYearRange"
              />
              <div class="year-values-centered">
                <input type="number" v-model.number="yearStart" min="1900" max="2025" @input="fixYearRange" />
                <span>—</span>
                <input type="number" v-model.number="yearEnd" min="1900" max="2025" @input="fixYearRange" />
              </div>
            </div>
          </div>
          <div class="modal-actions">
            <button v-if="step > 1" @click="step--">Назад</button>
            <button @click="confirmYear" :disabled="!canProceed">Подтвердить</button>
            <button @click="close">Отмена</button>
          </div>
        </div>
  
        <div v-else-if="step === 3">
          <label>Страна:</label>
          <input
            v-model="countrySearch"
            type="text"
            placeholder="Поиск страны..."
            class="country-search-input"
          />
          <div class="choice-table">
            <div
              v-for="[name, code] in sortedCountries"
              :key="code"
              :class="['choice-row', { selected: country === code }]"
              @click="selectCountry(code)"
            >
              {{ name }}
            </div>
          </div>
          <div class="modal-actions">
            <button v-if="step > 1" @click="step--">Назад</button>
            <button v-if="canProceed" @click="submit">Подобрать</button>
            <button @click="close">Отмена</button>
          </div>
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
  const yearStart = ref(2000)
  const yearEnd = ref(2020)
  const country = ref('')
  const countrySearch = ref('');
  
  const genres = {
    'Боевик': 28,
    'Приключения': 12,
    'Мультфильм': 16,
    'Комедия': 35,
    'Криминал': 80,
    'Документальный': 99,
    'Драма': 18,
    'Семейный': 10751,
    'Фэнтези': 14,
    'История': 36,
    'Ужасы': 27,
    'Музыка': 10402,
    'Детектив': 9648,
    'Мелодрама': 10749,
    'Научная фантастика': 878,
    'Телевизионный фильм': 10770,
    'Триллер': 53,
    'Военный': 10752,
    'Вестерн': 37
  }
  const countries = {
    'Австралия': 'AU',
    'Австрия': 'AT',
    'Азербайджан': 'AZ',
    'Албания': 'AL',
    'Алжир': 'DZ',
    'Ангола': 'AO',
    'Андорра': 'AD',
    'Аргентина': 'AR',
    'Армения': 'AM',
    'Афганистан': 'AF',
    'Багамы': 'BS',
    'Бангладеш': 'BD',
    'Барбадос': 'BB',
    'Бахрейн': 'BH',
    'Беларусь': 'BY',
    'Бельгия': 'BE',
    'Болгария': 'BG',
    'Боливия': 'BO',
    'Босния и Герцеговина': 'BA',
    'Ботсвана': 'BW',
    'Бразилия': 'BR',
    'Великобритания': 'GB',
    'Венгрия': 'HU',
    'Венесуэла': 'VE',
    'Вьетнам': 'VN',
    'Гаити': 'HT',
    'Гайана': 'GY',
    'Гамбия': 'GM',
    'Гана': 'GH',
    'Гватемала': 'GT',
    'Германия': 'DE',
    'Гондурас': 'HN',
    'Греция': 'GR',
    'Грузия': 'GE',
    'Дания': 'DK',
    'Доминикана': 'DO',
    'Египет': 'EG',
    'Израиль': 'IL',
    'Индия': 'IN',
    'Индонезия': 'ID',
    'Иордания': 'JO',
    'Ирак': 'IQ',
    'Иран': 'IR',
    'Ирландия': 'IE',
    'Исландия': 'IS',
    'Испания': 'ES',
    'Италия': 'IT',
    'Казахстан': 'KZ',
    'Камбоджа': 'KH',
    'Канада': 'CA',
    'Катар': 'QA',
    'Кения': 'KE',
    'Кипр': 'CY',
    'Киргизия': 'KG',
    'Китай': 'CN',
    'Колумбия': 'CO',
    'Корея': 'KR',
    'Коста-Рика': 'CR',
    'Куба': 'CU',
    'Кувейт': 'KW',
    'Латвия': 'LV',
    'Ливан': 'LB',
    'Литва': 'LT',
    'Люксембург': 'LU',
    'Маврикий': 'MU',
    'Мадагаскар': 'MG',
    'Малайзия': 'MY',
    'Мальта': 'MT',
    'Марокко': 'MA',
    'Мексика': 'MX',
    'Молдова': 'MD',
    'Монако': 'MC',
    'Монголия': 'MN',
    'Намибия': 'NA',
    'Непал': 'NP',
    'Нигерия': 'NG',
    'Нидерланды': 'NL',
    'Никарагуа': 'NI',
    'Новая Зеландия': 'NZ',
    'Норвегия': 'NO',
    'ОАЭ': 'AE',
    'Оман': 'OM',
    'Пакистан': 'PK',
    'Панама': 'PA',
    'Парагвай': 'PY',
    'Перу': 'PE',
    'Польша': 'PL',
    'Португалия': 'PT',
    'Россия': 'RU',
    'Румыния': 'RO',
    'Саудовская Аравия': 'SA',
    'Сербия': 'RS',
    'Сингапур': 'SG',
    'Сирия': 'SY',
    'Словакия': 'SK',
    'Словения': 'SI',
    'США': 'US',
    'Таджикистан': 'TJ',
    'Таиланд': 'TH',
    'Тунис': 'TN',
    'Турция': 'TR',
    'Узбекистан': 'UZ',
    'Украина': 'UA',
    'Уругвай': 'UY',
    'Филиппины': 'PH',
    'Финляндия': 'FI',
    'Франция': 'FR',
    'Хорватия': 'HR',
    'Чехия': 'CZ',
    'Чили': 'CL',
    'Швейцария': 'CH',
    'Швеция': 'SE',
    'Шри-Ланка': 'LK',
    'Эквадор': 'EC',
    'Эстония': 'EE',
    'ЮАР': 'ZA',
    'Япония': 'JP'
  };
  
  const canProceed = computed(() => {
    if (step.value === 1) return genre.value
    if (step.value === 2) return yearStart.value && yearEnd.value && yearStart.value <= yearEnd.value
    if (step.value === 3) return country.value
    return false
  })
  
  const close = () => emit('close')
  
  const submit = () => {
    emit('submit', {
      genre: genre.value,
      yearStart: yearStart.value,
      yearEnd: yearEnd.value,
      country: country.value
    })
    close()
  }
  
  const selectGenre = (code) => {
    genre.value = code;
    step.value++;
  };
  
  const confirmYear = () => {
    if (canProceed.value) step.value++;
  };
  
  const selectCountry = (code) => {
    country.value = code;
    if (canProceed.value) submit();
  };
  
  const fixYearRange = () => {
    if (yearStart.value > yearEnd.value) {
      [yearStart.value, yearEnd.value] = [yearEnd.value, yearStart.value]
    }
  }
  
  const sortedCountries = computed(() => {
    return Object.entries(countries)
      .filter(([name]) => name.toLowerCase().includes(countrySearch.value.toLowerCase()))
      .sort((a, b) => a[0].localeCompare(b[0], 'ru'));
  });
  
  watch(() => props.show, (val) => {
    if (val) {
      step.value = 1
      genre.value = ''
      yearStart.value = 2000
      yearEnd.value = 2020
      country.value = ''
    }
  })
  </script>
  
  <style scoped>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 2000;
  }
  .modal-content {
    background: #1e1e1e;
    border-radius: 16px;
    padding: 32px 32px 24px 32px;
    width: 80%;
    max-width: 900px;
    min-width: 350px;
    min-height: 340px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    display: flex;
    flex-direction: column;
    align-items: stretch;
  }
  .choice-table {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin: 16px 0;
    max-height: 300px;
    overflow-y: auto;
  }
  .choice-table::-webkit-scrollbar {
    width: 0;
    background: transparent;
  }
  .choice-table {
    scrollbar-width: none;
  }
  .choice-row {
    background: #181818;
    color: #fff;
    padding: 12px 18px;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s;
    border: 1px solid #333;
  }
  .choice-row.selected,
  .choice-row:hover {
    background: #440087;
    color: #fff;
    border-color: #8e2de2;
  }
  .year-choice-table {
    max-height: none;
    align-items: center;
    justify-content: center;
    padding: 24px 0;
  }
  .year-range-center {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 18px;
    width: 100%;
  }
  .year-range-center input[type="range"] {
    width: 80%;
    accent-color: #8e2de2;
  }
  .year-values-centered {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    font-size: 1.4rem;
    color: #fff;
  }
  .year-values-centered input[type="number"] {
    width: 90px;
    background: #222;
    color: #fff;
    border: 1px solid #444;
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 1.2rem;
    text-align: center;
    -webkit-appearance: none;
    -moz-appearance: textfield;
    appearance: textfield;
  }
  .year-values-centered input[type="number"]::-webkit-inner-spin-button,
  .year-values-centered input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
  .year-values-centered input[type="number"] {
    -moz-appearance: textfield;
  }
  .modal-actions {
    margin-top: 42px;
    display: flex;
    justify-content: space-between;
  }
  .country-search-input {
    width: 100%;
    margin-bottom: 12px;
    padding: 10px 14px;
    border-radius: 8px;
    border: 1px solid #333;
    background: #222;
    color: #fff;
    font-size: 1rem;
    outline: none;
  }
  .country-search-input:focus {
    border-color: #8e2de2;
  }
  </style>
  