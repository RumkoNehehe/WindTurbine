<script setup lang="ts">
import type { DataSource } from '@/types/dataSource'

defineProps<{
    modelValue: DataSource
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: DataSource): void
}>()

function setSource(value: DataSource) {
    emit('update:modelValue', value)
}
</script>

<template>
    <div class="flex w-full rounded-2xl bg-gray-300 p-1">
        <button class="flex-1 rounded-xl px-4 py-2 font-semibold transition" :class="modelValue === 'liveData'
            ? 'bg-gray-700 text-white'
            : 'bg-transparent text-gray-700'" @click="setSource('liveData')">
            Live
        </button>

        <button class="flex-1 rounded-xl px-4 py-2 font-semibold transition" :class="modelValue === 'customData'
            ? 'bg-gray-700 text-white'
            : 'bg-transparent text-gray-700'" @click="setSource('customData')">
            Recording
        </button>
    </div>
</template>