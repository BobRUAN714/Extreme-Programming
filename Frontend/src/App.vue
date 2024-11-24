<template>
  <div class="container">
    <h1>Address Book</h1>
    <contact-list />
  </div>
</template>

<script setup lang="ts">
import ContactList from './components/ContactList.vue'
</script>

<style>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
</style>