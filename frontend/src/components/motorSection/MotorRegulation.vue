<script setup lang="ts">
import BaseToggle from "../base/BaseToggle.vue";
import BaseButton from "../base/BaseButton.vue";
import type { Mode } from "@/types/mode";
import type { MotorTarget } from "@/types/motorTarget";
import type {MotorRegulationState  } from "@/types/states/regulationState";

const props = defineProps<{
    regulationControl: MotorRegulationState

}>();

const emit = defineEmits<{
    (e: "update:motor-target", value: MotorTarget): void;
    (e: "update:target-rpm", value: number): void;
    (e: "update:kp", value: number): void;
    (e: "update:ki", value: number): void;
    (e: "update:kd", value: number): void;
    (e: "update:mode2", value: Mode): void;
    (e: "start-regulation"): void;
    (e: "stop-regulation"): void;
}>();

function handleNumberInput(
    event: Event,
    key: "target-rpm" | "kp" | "ki" | "kd",
) {
    const target = event.target as HTMLInputElement;
    const value = Number(target.value);

    switch (key) {
        case "target-rpm":
            emit("update:target-rpm", value);
            break;
        case "kp":
            emit("update:kp", value);
            break;
        case "ki":
            emit("update:ki", value);
            break;
        case "kd":
            emit("update:kd", value);
            break;
    }
}

function setMode(value: Mode) {
    emit("update:mode2", value);
}

const motorTargetOptions = [
    { label: "Motor 1", value: "motor1" },
    { label: "Motor 2", value: "motor2" },
] as const
</script>

<template>
    <div class="flex flex-col gap-2">
        <BaseToggle
            :model-value="regulationControl.motorTarget"
            :options="motorTargetOptions"
            @update:model-value="emit('update:motor-target', $event as MotorTarget)"
        />

        <div class="flex justify-between">
            <div class="flex flex-col">
                <label class="mb-1 text-sm font-semibold text-gray-800">
                    Target RPM
                </label>

                <input
                    type="number"
                    min="0"
                    class="w-32 rounded-xl bg-white px-3 py-2 text-sm shadow-sm outline-none"
                    :value="regulationControl.targetRpm"
                    @input="handleNumberInput($event, 'target-rpm')"
                />
            </div>
        <p
            v-if="regulationControl.isRegulating !== undefined"
            class="text-sm font-semibold text-gray-800"
        >
            Regulation:
            {{ regulationControl.isRegulating ? "Active" : "Stopped" }}
        </p>
        </div>

        <div class="grid grid-cols-3 gap-3">
            <div class="flex flex-col">
                <label class="mb-1 text-sm font-semibold text-gray-800">
                    Kp
                </label>

                <input
                    type="number"
                    step="0.01"
                    class="rounded-xl bg-white px-3 py-2 text-sm shadow-sm outline-none"
                    :value="regulationControl.kp"
                    @input="handleNumberInput($event, 'kp')"
                />
            </div>

            <div class="flex flex-col">
                <label class="mb-1 text-sm font-semibold text-gray-800">
                    Ki
                </label>

                <input
                    type="number"
                    step="0.01"
                    class="rounded-xl bg-white px-3 py-2 text-sm shadow-sm outline-none"
                    :value="regulationControl.ki"
                    @input="handleNumberInput($event, 'ki')"
                />
            </div>

            <div class="flex flex-col">
                <label class="mb-1 text-sm font-semibold text-gray-800">
                    Kd
                </label>

                <input
                    type="number"
                    step="0.01"
                    class="rounded-xl bg-white px-3 py-2 text-sm shadow-sm outline-none"
                    :value="regulationControl.kd"
                    @input="handleNumberInput($event, 'kd')"
                />
            </div>
        </div>

        <div class="flex flex-col">
            <label class="mb-1 text-sm font-semibold text-gray-800">
                Mode
            </label>

            <div class="flex w-full rounded-2xl bg-gray-300 p-1">
                <button
                    class="flex-1 rounded-xl px-4 py-2 font-semibold transition"
                    :class="
                        regulationControl.mode === 'FORWARD'
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
                        regulationControl.mode === 'REVERSE'
                            ? 'bg-gray-700 text-white'
                            : 'bg-transparent text-gray-700'
                    "
                    @click="setMode('REVERSE')"
                >
                    Backward
                </button>
            </div>
        </div>

        <div class="flex flex-row justify-between">
            <BaseButton variant="primary" @click="emit('start-regulation')">
                Start regulation
            </BaseButton>

            <BaseButton variant="danger" @click="emit('stop-regulation')">
                Stop regulation
            </BaseButton>
        </div>


    </div>
</template>
