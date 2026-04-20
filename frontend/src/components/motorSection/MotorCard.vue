<script setup lang="ts">
import { computed } from "vue";
import type { Motor } from '../../types/motor';
import BaseCard from '../base/BaseCard.vue';

const props = defineProps<{ motor: Motor }>()

const pwmPercent = computed(() =>
  Math.round((props.motor.pwm / 255) * 100)
)

</script>

<template>
    <BaseCard variant="light">
        <div class="flex flex-col items-start">
            <h2 class="text-xl font-bold mb-2">
                {{ motor.name }}
            </h2>
            <p>pwm: {{ pwmPercent }}%</p>
            <p>rpm: {{ motor.rpm }}</p>
            <p>mode: {{ motor.mode }}</p>
        </div>
    </BaseCard>
</template>