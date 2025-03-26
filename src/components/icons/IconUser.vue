<template>
  <svg class="icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <title />
    <circle cx="12" cy="8" r="4" fill="gray" />
    <defs>
      <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color: #9a5aff; stop-opacity: 1" />
        <stop offset="100%" style="stop-color: #87edff; stop-opacity: 1" />
      </linearGradient>
    </defs>
    <path
      d="M20,19v1a1,1,0,0,1-1,1H5a1,1,0,0,1-1-1V19a6,6,0,0,1,6-6h4A6,6,0,0,1,20,19Z"
      fill="gray"
    />
  </svg>
</template>

<script>
export default {
  name: "IconUser",
};
</script>

<style scoped>
.icon {
    width: 35px;
    height: 35px;
}
</style>
