<script setup lang="ts">
import BaseCard from '../base/BaseCard.vue';
import type { Motor } from '@/types/motor';
import MotorList from './MotorList.vue';
import LogPanel from './LogPanel.vue';
import DataSourceToggle from '../chartPanel/DataSourceToggle.vue';
import type { DataSource } from '@/types/dataSource';

defineProps<{
    motors: Motor[],
    logs: string[],
    dataSource: DataSource,
    isAdmin: boolean
}>()

const emit = defineEmits<{
    (e: 'update:dataSource', value: DataSource): void
}>()

</script>

<template>
    <BaseCard variant="dark" class="h-full min-h-0">
        <div class="flex h-full min-h-0 flex-col gap-4">
            <MotorList :motors="motors"></MotorList>
            <BaseCard variant="light" class="flex flex-col h-full min-h-0">
                <div class="flex justify-between mb-2">
                    <h2 class="text-xl font-bold">Logs</h2>

                    <DataSourceToggle v-if="isAdmin" :labels="['Logs', 'Control']" :model-value="dataSource"
                        @update:model-value="emit('update:dataSource', $event)" />
                </div>
                <LogPanel :logs="logs"></LogPanel>
            </BaseCard>
        </div>
    </BaseCard>
</template>