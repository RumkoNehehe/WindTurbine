<script setup lang="ts">
import { readonly } from 'vue';

defineProps<{
    modelValue: string
    options: readonly [
        { readonly label: string; readonly value: string },
        { readonly label: string; readonly value: string }
    ]
}>()

const emit = defineEmits<{
    (e: "update:model-value", value: string): void
}>()

function selectOption(value: string) {
    emit("update:model-value", value)
}
</script>

<template>
    <div class="flex rounded-2xl bg-gray-300 p-1">
        <button
            v-for="option in options"
            :key="option.value"
            class="flex-1 rounded-xl px-4 py-2 font-semibold transition"
            :class="
                modelValue === option.value
                    ? 'bg-gray-700 text-white'
                    : 'bg-transparent text-gray-700'
            "
            @click="selectOption(option.value)"
        >
            {{ option.label }}
        </button>
    </div>
</template>