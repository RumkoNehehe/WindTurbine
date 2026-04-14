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
    <BaseCard variant="dark" class="h-full min-h-0">
        <div class="flex h-full min-h-0 flex-col gap-4">
            <MotorList :motors="motors"></MotorList>
            <LogPanel :logs="logs"></LogPanel>
        </div>
    </BaseCard>
</template>