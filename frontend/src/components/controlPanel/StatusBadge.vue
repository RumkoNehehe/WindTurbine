<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
    variant: 'success' | 'danger' | 'neutral' | 'warning'
    label: string
}>()

const containerClasses = computed(() => {
    switch (props.variant) {
        case 'success':
            return 'bg-green-100 text-green-800'
        case 'danger':
            return 'bg-red-100 text-red-800'
        case 'warning':
            return 'bg-yellow-100 text-yellow-800'
        case 'neutral':
        default:
            return 'bg-gray-200 text-gray-800'
    }
})

const dotClasses = computed(() => {
    switch (props.variant) {
        case 'success':
            return 'bg-green-500'
        case 'danger':
            return 'bg-red-500'
        case 'warning':
            return 'bg-yellow-500'
        case 'neutral':
        default:
            return 'bg-gray-500'
    }
})
</script>

<template>
    <div :class="[
        'flex items-center gap-2 px-3 py-1 rounded-full text-sm font-semibold w-fit',
        containerClasses
    ]">
        <span :class="[
            'w-3 h-3 rounded-full',
            dotClasses
        ]"></span>
        <span>{{ label }}</span>
    </div>
</template>