<script setup lang="ts">
import type { DataSource } from '@/types/dataSource'

defineProps<{
    modelValue: DataSource
    labels: [string,string]
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: DataSource): void
}>()

function setSource(value: DataSource) {
    emit('update:modelValue', value)
}
</script>

<template>
    <div class="flex rounded-2xl bg-gray-300 p-1">
        <button class="flex-1 rounded-xl px-4 py-2 font-semibold transition" :class="modelValue === 'first'
            ? 'bg-gray-700 text-white'
            : 'bg-transparent text-gray-700'" @click="setSource('first')">
            {{ labels[0] }}
        </button>

        <button class="flex-1 rounded-xl px-4 py-2 font-semibold transition" :class="modelValue === 'second'
            ? 'bg-gray-700 text-white'
            : 'bg-transparent text-gray-700'" @click="setSource('second')">
            {{ labels[1] }}
        </button>
    </div>
</template>