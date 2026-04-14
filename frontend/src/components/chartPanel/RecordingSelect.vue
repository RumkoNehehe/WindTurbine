<script setup lang="ts">
defineProps<{
    modelValue: string
    recordings: string[]
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: string): void
}>()

function handleChange(event: Event) {
    const target = event.target as HTMLSelectElement
    emit('update:modelValue', target.value)
}
</script>

<template>
    <div class="flex flex-col gap-2">
        <label class="text-sm font-semibold text-gray-800">
            Recording
        </label>

        <select class="rounded-xl bg-gray-300 px-4 py-3 font-semibold text-gray-800 outline-none" :value="modelValue"
            @change="handleChange">
            <option disabled value="">
                Select a recording
            </option>

            <option v-for="recording in recordings" :key="recording" :value="recording">
                {{ recording }}
            </option>
        </select>
    </div>
</template>