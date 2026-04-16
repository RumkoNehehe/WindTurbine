<script setup lang="ts">
import { computed } from 'vue'
import DataSourceToggle from '../chartPanel/DataSourceToggle.vue'
import BaseButton from '../base/BaseButton.vue'
import type { DataSource } from '@/types/dataSource'
import type { Mode } from '@/types/mode'

const props = defineProps<{
    datasource: DataSource
    labels: [string, string]
    pwm: number
    mode: Mode
}>()

const emit = defineEmits<{
    (e: 'update:dataSource', value: DataSource): void
    (e: 'update:pwm', value: number): void
    (e: 'update:mode', value: Mode): void
    (e: 'apply'): void
}>()

function handleSliderInput(event: Event) {
    const target = event.target as HTMLInputElement
    emit('update:pwm', Number(target.value))
}

function handleNumberInput(event: Event) {
    const target = event.target as HTMLInputElement
    emit('update:pwm', Number(target.value))
}

function setMode(value: Mode) {
    emit('update:mode', value)
}

const clampedPwm = computed(() => Math.max(0, Math.min(100, props.pwm)))
</script>

<template>
    <div class="flex flex-col gap-2">
        <DataSourceToggle :model-value="datasource" :labels="labels"
            @update:model-value="emit('update:dataSource', $event)" />

        <div class="flex flex-col">
            <label class="text-sm font-semibold text-gray-800">
                PWM
            </label>

            <input type="range" min="0" max="100" :value="clampedPwm" @input="handleSliderInput" />

            <input type="number" min="0" max="100"
                class="w-28 rounded-xl bg-white px-3 py-2 text-sm shadow-sm outline-none" :value="clampedPwm"
                @input="handleNumberInput" />
        </div>

        <div class="flex flex-col">
            <label class="text-sm font-semibold text-gray-800">
                Mode
            </label>

            <div class="flex w-full rounded-2xl bg-gray-300 p-1">
                <button class="flex-1 rounded-xl px-4 py-2 font-semibold transition" :class="mode === 'forward'
                    ? 'bg-gray-700 text-white'
                    : 'bg-transparent text-gray-700'" @click="setMode('forward')">
                    Forward
                </button>

                <button class="flex-1 rounded-xl px-4 py-2 font-semibold transition" :class="mode === 'backward'
                    ? 'bg-gray-700 text-white'
                    : 'bg-transparent text-gray-700'" @click="setMode('backward')">
                    Backward
                </button>

                <button class="flex-1 rounded-xl px-4 py-2 font-semibold transition" :class="mode === 'brake'
                    ? 'bg-gray-700 text-white'
                    : 'bg-transparent text-gray-700'" @click="setMode('brake')">
                    Brake
                </button>
            </div>
        </div>

        <div>
            <BaseButton variant="primary" @click="emit('apply')">
                Apply changes
            </BaseButton>
        </div>
    </div>
</template>