<script setup lang="ts">
import BaseCard from '../base/BaseCard.vue';
import type { Motor } from '@/types/motor';
import MotorList from './MotorList.vue';
import LogPanel from './LogPanel.vue';
import DataSourceToggle from '../chartPanel/DataSourceToggle.vue';
import type { DataSource } from '@/types/dataSource';
import MotorControl from './MotorControl.vue';
import type { Mode } from '@/types/mode';

defineProps<{
    motors: Motor[]
    logs: string[]
    dataSource: DataSource
    motorSource: DataSource
    isAdmin: boolean
    pwm: number
    mode: Mode
}>()

const emit = defineEmits<{
    (e: 'update:dataSource', value: DataSource): void
    (e: 'update:motorSource', value: DataSource): void
    (e: 'update:pwm', value: number): void
    (e: 'update:mode', value: 'forward' | 'backward' | 'brake'): void
    (e: 'apply'): void
}>()

</script>

<template>
    <BaseCard variant="dark" class="h-full min-h-0">
        <div class="flex h-full min-h-0 flex-col gap-4">
            <MotorList :motors="motors"></MotorList>
            <BaseCard variant="light" class="flex flex-col h-full min-h-0">
                <div class="flex justify-between mb-2">
                    <h2 v-if="dataSource === 'first'" class="text-xl font-bold">Logs</h2>
                    <h2 v-else class="text-xl font-bold">Control</h2>
                </div>

                <LogPanel v-if="dataSource === 'first'" :logs="logs"></LogPanel>
                <MotorControl v-else :datasource="motorSource" :labels="['Motor 1', 'Motor 2']" :pwm="pwm" :mode="mode"
                    @update:data-source="emit('update:motorSource', $event)" @update:mode="emit('update:mode', $event)"
                    @update:pwm="emit('update:pwm', $event)" @apply="emit('apply')"></MotorControl>
            </BaseCard>
        </div>
    </BaseCard>
</template>