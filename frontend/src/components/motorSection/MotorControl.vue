<script setup lang="ts">
import { computed } from "vue";
import BaseToggle from "../base/BaseToggle.vue";
import BaseButton from "../base/BaseButton.vue";
import type { Mode } from "@/types/mode";
import type { MotorTarget } from "@/types/motorTarget";
import type {ManualMotorControlState  } from "@/types/states/ManualMotorControlState";

const props = defineProps<{
    manualControl: ManualMotorControlState
}>();

const emit = defineEmits<{
    (e: "update:motor-target", value: MotorTarget): void;
    (e: "update:pwm", value: number): void;
    (e: "update:mode", value: Mode): void;
    (e: "apply"): void;
    (e: "stop-system"): void;
}>();

function handleSliderInput(event: Event) {
    const target = event.target as HTMLInputElement
    const percent = Number(target.value)

    const pwm = Math.round((percent / 100) * 255)
    emit("update:pwm", pwm)
}

function handleNumberInput(event: Event) {
    const target = event.target as HTMLInputElement
    const percent = Number(target.value)

    const pwm = Math.round((percent / 100) * 255)
    emit("update:pwm", pwm)
}

function setMode(value: Mode) {
    emit("update:mode", value);
}

const pwmPercent = computed(() =>
    Math.max(0, Math.min(100, Math.round((props.manualControl.pwm / 255) * 100)))
);

const motorTargetOptions = [
    { label: "Motor 1", value: "motor1" },
    { label: "Motor 2", value: "motor2" },
] as const
</script>

<template>
    <div class="flex flex-col gap-4">
        <BaseToggle
            :model-value="manualControl.motorTarget"
            :options="motorTargetOptions"
            @update:model-value="emit('update:motor-target', $event as MotorTarget)"
        />

        <div class="flex flex-col">
            <label class="text-sm font-semibold text-gray-800 mb-1">
                PWM %
            </label>

            <input
                type="range"
                min="0"
                max="100"
                :value="pwmPercent"
                class="mb-1"
                @input="handleSliderInput"
            />

            <input
                type="number"
                min="0"
                max="100"
                class="w-28 rounded-xl bg-white px-3 py-2 text-sm shadow-sm outline-none"
                :value="pwmPercent"
                @input="handleNumberInput"
            />
        </div>

        <div class="flex flex-col">
            <label class="text-sm font-semibold text-gray-800 mb-1">
                Mode
            </label>

            <div class="flex w-full rounded-2xl bg-gray-300 p-1">
                <button
                    class="flex-1 rounded-xl px-4 py-2 font-semibold transition"
                    :class="
                        manualControl.mode === 'FORWARD'
                            ? 'bg-gray-700 text-white'
                            : 'bg-transparent text-gray-700'
                    "
                    @click="setMode('FORWARD')"
                >
                    Forward
                </button>

                <button
                    class="flex-1 rounded-xl px-4 py-2 font-semibold transition"
                    :class="
                        manualControl.mode === 'REVERSE'
                            ? 'bg-gray-700 text-white'
                            : 'bg-transparent text-gray-700'
                    "
                    @click="setMode('REVERSE')"
                >
                    Backward
                </button>

                <button
                    class="flex-1 rounded-xl px-4 py-2 font-semibold transition"
                    :class="
                        manualControl.mode === 'BRAKE'
                            ? 'bg-gray-700 text-white'
                            : 'bg-transparent text-gray-700'
                    "
                    @click="setMode('BRAKE')"
                >
                    Brake
                </button>
            </div>
        </div>

        <div class="flex flex-row justify-between">
            <div>
                <BaseButton variant="primary" @click="emit('apply')">
                    Send command
                </BaseButton>
            </div>
            <div>
                <BaseButton variant="danger" @click="emit('stop-system')">
                    Stop system
                </BaseButton>
            </div>
        </div>
    </div>
</template>
