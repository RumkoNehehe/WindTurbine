<script setup lang="ts">
import BaseCard from '../base/BaseCard.vue';
import type { Motor } from '@/types/motor';
import MotorList from './MotorList.vue';
import LogPanel from './LogPanel.vue';
import DataSourceToggle from '../base/BaseToggle.vue';
import type { ToggleData } from '@/types/dataSource';
import MotorControl from './MotorControl.vue';
import type { Mode } from '@/types/mode';

defineProps<{
    motors: Motor[]
    logs: string[]
    controlsToggleData: ToggleData
    motorToggleData: ToggleData
    isAdmin: boolean
    pwm: number
    mode: Mode
}>()

const emit = defineEmits<{
    (e: 'update:motor-toggle-data', value: ToggleData): void
    (e: 'update:pwm', value: number): void
    (e: 'update:mode', value: Mode): void
    (e: 'apply'): void
    (e: 'stop-system'): void
}>()

</script>

<template>
    <BaseCard variant="dark" class="h-full min-h-0">
        <div class="flex h-full min-h-0 flex-col gap-4">
            <MotorList :motors="motors"></MotorList>
            <BaseCard variant="light" class="flex flex-col h-full min-h-0">
                <div class="flex justify-between mb-2">
                    <h2 v-if="controlsToggleData === 'first'" class="text-xl font-bold">Logs</h2>
                    <h2 v-else class="text-xl font-bold">Control</h2>
                </div>

                <LogPanel v-if="controlsToggleData === 'first'" :logs="logs"></LogPanel>
                <MotorControl v-else :toggleData="motorToggleData" :labels="['Motor 1', 'Motor 2']" :pwm="pwm" :mode="mode"
                    @update:toggle-data="emit('update:motor-toggle-data', $event)" @update:mode="emit('update:mode', $event)"
                    @update:pwm="emit('update:pwm', $event)" @apply="emit('apply')" @stop-system="emit('stop-system')"></MotorControl>
            </BaseCard>
        </div>
    </BaseCard>
</template>