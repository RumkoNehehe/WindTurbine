<script setup lang="ts">
import BaseCard from '../base/BaseCard.vue';
import BaseButton from '../base/BaseButton.vue';
import StatusBadge from './StatusBadge.vue';
import DataSourceToggle from '../chartPanel/DataSourceToggle.vue';
import type { DataSource } from '@/types/dataSource';


defineProps<{
    dataSource: DataSource
    isConnected: boolean
    isRecording: boolean
    lastUpdate: string
    username: string
    isAdmin: boolean
}>()

const emit = defineEmits<{
    (e: 'update:dataSource', dataSource: DataSource): void
    (e: 'start-recording'): void
    (e: 'download-file'): void
    (e: 'save-file'): void
    (e: 'stop-recording'): void
    (e: 'log-off'): void
}>()

</script>

<template>
    <BaseCard variant="dark" class="p-4 flex flex-col items-center gap-4">
        <BaseCard variant="light" class="flex flex-col items-center">
            <StatusBadge :variant="isConnected ? 'success' : 'danger'"
                :label="isConnected ? 'Connected' : 'Disconnected'" />
            <p class="font-semibold">
                Last update: {{ lastUpdate }}
            </p>
        </BaseCard>

        <BaseCard variant="light" class="flex flex-col items-center gap-2">
            <BaseButton variant="success" @click="emit('start-recording')">
                Start recording
            </BaseButton>

            <BaseButton variant="danger" @click="emit('stop-recording')">
                Stop recording
            </BaseButton>

            <StatusBadge :variant="isRecording ? 'success' : 'neutral'"
                :label="isRecording ? 'Recording On' : 'Recording Off'" />

            <BaseButton variant="primary" @click="emit('save-file')">
                Save to database
            </BaseButton>

            <BaseButton variant="neutral" @click="emit('download-file')">
                Download recording
            </BaseButton>
        </BaseCard>

        <BaseCard variant="light" class="flex flex-col justify-end mt-auto items-center gap-2">
            <h3 class="text-md font-bold mb-2">
                Logged user: {{ username }}
            </h3>

            <DataSourceToggle v-if="isAdmin" :labels="['Logs', 'Control']" :model-value="dataSource"
                @update:model-value="emit('update:dataSource', $event)" />
            <BaseButton variant="danger" @click="emit('log-off')">
                Log Off
            </BaseButton>
        </BaseCard>
    </BaseCard>
</template>