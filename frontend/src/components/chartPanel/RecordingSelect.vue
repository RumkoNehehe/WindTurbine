<script setup lang="ts">
import type { RecordingListItem } from '@/types/recordingListItem';

defineProps<{
    selectedRecording: number | null
    recordings: RecordingListItem[]
}>()

const emit = defineEmits<{
    (e: 'update:selected-recording', value: number): void
}>()

function handleChange(event: Event) {
    const target = event.target as HTMLSelectElement
    emit('update:selected-recording', Number(target.value))
}
</script>

<template>
    <div class="flex flex-col gap-2">
        <label class="text-sm font-semibold text-gray-800">
            Recording
        </label>

        <select class="rounded-xl bg-gray-300 px-4 py-3 font-semibold text-gray-800 outline-none" :value="selectedRecording"
            @change="handleChange">
            <option disabled value="">
                Select a recording
            </option>

            <option v-for="recording in recordings" :key="recording.id" :value="recording.id">
                {{ recording.name }}
            </option>
        </select>
    </div>
</template>