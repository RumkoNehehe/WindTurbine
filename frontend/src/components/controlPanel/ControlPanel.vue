<script setup lang="ts">
import BaseCard from '../base/BaseCard.vue';
import BaseButton from '../base/BaseButton.vue';
import StatusBadge from './StatusBadge.vue';

defineProps<{
    isConnected: boolean,
    isRecording: boolean
    lastUpdate: string
}>()

const emit = defineEmits<{
    (e: 'start-recording'): void
    (e: 'stop-recording'): void
}>()

</script>

<template>
    <BaseCard variant="dark" class="p-4 flex flex-col items-center gap-4">
        <StatusBadge :variant="isConnected ? 'success' : 'danger'"
            :label="isConnected ? 'Connected' : 'Disconnected'" />
        <p class="text-lg font-semibold">
            Last update: {{ lastUpdate }}
        </p>
        <BaseButton variant="primary" @click="emit('start-recording')">
            Start recording
        </BaseButton>

        <BaseButton variant="danger" @click="emit('stop-recording')">
            Stop recording
        </BaseButton>

        <StatusBadge :variant="isRecording ? 'success' : 'neutral'" :label="isRecording ? 'Recording On' : 'Recording Off'"/>
    </BaseCard>
</template>