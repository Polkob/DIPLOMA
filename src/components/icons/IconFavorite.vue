<template>
  <svg
    class="icon"
    viewBox="0 0 576 512"
    xmlns="http://www.w3.org/2000/svg"
    :style="{ fill: filled ? '#42a5f5' : 'gray' }"
  >
    <defs>
        <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color: #9a5aff; stop-opacity: 1" />
          <stop offset="100%" style="stop-color:  #87edff; stop-opacity: 1" />
        </linearGradient>
      </defs>
    <path
      d="M316.7 17.8l65.43 132.4l146.4 21.29c26.27 3.796 36.79 36.09 17.75 54.59l-105.9 102.1l25.05 145.5c4.508 26.31-23.23 45.9-46.49 33.7L288 439.6l-130.9 68.7C133.8 520.5 106.1 500.9 110.6 474.6l25.05-145.5L29.72 226.1c-19.03-18.5-8.516-50.79 17.75-54.59l146.4-21.29l65.43-132.4C271.1-6.083 305-5.786 316.7 17.8z"
    />
  </svg>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  filled: Boolean
});
</script>

<style scoped>
.icon {
  width: 35px;
  height: 35px;
  padding: 3px;
  transition: fill 0.2s;
}
</style>