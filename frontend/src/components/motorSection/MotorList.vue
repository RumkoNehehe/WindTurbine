<script setup lang="ts">
import MotorCard from '../motorSection/MotorCard.vue';
import type { Motor } from '@/types/motor';

defineProps<{
    motors: Motor[]
}>()
</script>

<template>
    <div class="grid grid-cols-2 gap-4">
        <MotorCard v-for="motor in motors" :key="motor.name" :motor="motor"></MotorCard>
    </div>
</template>