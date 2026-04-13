<script setup lang="ts">
import type { Motor } from '../../types/motor';
import BaseCard from '../Base/BaseCard.vue';

defineProps<{ motor: Motor }>()

</script>

<template>
    <BaseCard variant="light">
        <div class="flex flex-col items-start">
            <h2 class="text-xl font-bold mb-2">
                {{ motor.name }}
            </h2>
            <p>pwm: {{ motor.pwm }}</p>
            <p>rpm: {{ motor.rpm }}</p>
        </div>
    </BaseCard>
</template>