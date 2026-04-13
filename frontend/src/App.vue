<script setup lang="ts">
import { ref } from 'vue';
import MotorSection from './components/MotorSection/MotorSection.vue';
import type { Motor } from './types/motor'

const motors = ref<Motor[]>([
  { name: 'Motor1', pwm: 120, rpm: 240 },
  { name: 'Motor2', pwm: 50, rpm: 110 }
])

const logs = ref<string[]>(['nehehe', 'nehehe', 'hekjfshej'])

</script>

<template>
  <div class="min-h-screen bg-gray-800 p-6">
    <div class="max-w-7xl mx-auto bg-gray-700 rounded-2xl p-6">

      <h1 class="text-3xl font-bold text-center mb-6">
        Ovládanie elektrárne
      </h1>

      <div class="grid grid-cols-3 gap-6">
        <MotorSection :motors="motors" :logs="logs"></MotorSection>
        <!-- PLACEHOLDER -->
        <div></div>
        <!-- PLACEHOLDER -->
        <div></div>
      </div>

    </div>
  </div>
</template>

<style scoped></style>
