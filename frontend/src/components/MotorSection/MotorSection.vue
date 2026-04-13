<script setup lang="ts">
import BaseCard from '../base/BaseCard.vue';
import type { Motor } from '@/types/motor';
import MotorList from './MotorList.vue';
import LogPanel from './LogPanel.vue';

defineProps<{
    motors: Motor[],
    logs: string[]
}>()
</script>

<template>
    <BaseCard variant="dark" class="space-y-4">
        <MotorList :motors="motors"></MotorList>
        <LogPanel :logs="logs"></LogPanel>
    </BaseCard>
</template>