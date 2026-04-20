<script setup lang="ts">
import BaseCard from "../base/BaseCard.vue";
import type { Motor } from "@/types/motor";
import MotorList from "./MotorList.vue";
import LogPanel from "./LogPanel.vue";
import MotorControl from "./MotorControl.vue";
import type { Mode } from "@/types/mode";
import MotorRegulation from "./MotorRegulation.vue";
import BaseButton from "../base/BaseButton.vue";
import type { LeftPanelView } from "@/types/leftPanelView";
import type { MotorTarget } from "@/types/motorTarget";
import type { ManualMotorControlState } from "@/types/states/ManualMotorControlState";
import type { MotorRegulationState } from "@/types/states/regulationState";

defineProps<{
    motors: Motor[];
    logs: string[];
    isAdmin: boolean;
    isRegulation: boolean;
    leftPanelView: LeftPanelView;
    manualControl: ManualMotorControlState;
    regulationControl: MotorRegulationState;
}>();

const emit = defineEmits<{
    (e: "update:motor-toggle-data", value: MotorTarget): void;
    (e: "update:pwm", value: number): void;
    (e: "update:mode", value: Mode): void;
    (e: "apply"): void;
    (e: "stop-system"): void;
    (e: "update:motor-target", value: MotorTarget): void;
    (e: "update:target-rpm", value: number): void;
    (e: "update:kp", value: number): void;
    (e: "update:ki", value: number): void;
    (e: "update:kd", value: number): void;
    (e: "update:mode2", value: Mode): void;
    (e: "start-regulation"): void;
    (e: "stop-regulation"): void;
    (e: "toggle-regulation"): void;
}>();
</script>

<template>
    <BaseCard variant="dark" class="h-full min-h-0">
        <div class="flex h-full min-h-0 flex-col gap-4">
            <MotorList :motors="motors"></MotorList>
            <BaseCard variant="light" class="flex flex-col h-full min-h-0">
                <div class="flex justify-between mb-2">
                    <h2 class="text-xl font-bold">
                        <template v-if="leftPanelView === 'logs'">
                            Logs
                        </template>

                        <template v-else>
                            {{ isRegulation ? "Regulation" : "Control" }}
                        </template>
                    </h2>

                    <BaseButton
                        v-if="leftPanelView === 'control'"
                        @click="emit('toggle-regulation')"
                        variant="primary"
                    >
                        {{ isRegulation ? "Control" : "Regulation" }}
                    </BaseButton>
                </div>

                <LogPanel
                    v-if="leftPanelView === 'logs'"
                    :logs="logs"
                ></LogPanel>
                <MotorControl
                    v-else-if="
                        leftPanelView === 'control' && isRegulation === false
                    "
                    :manual-control="manualControl"
                    @update:toggle-data="
                        emit('update:motor-toggle-data', $event)
                    "
					@update:motor-target="emit('update:motor-toggle-data', $event)"
                    @update:mode="emit('update:mode', $event)"
                    @update:pwm="emit('update:pwm', $event)"
                    @apply="emit('apply')"
                    @stop-system="emit('stop-system')"
                ></MotorControl>
                <MotorRegulation
                    v-else-if="
                        leftPanelView === 'control' && isRegulation === true
                    "
                    :regulation-control="regulationControl"
                    @start-regulation="emit('start-regulation')"
                    @stop-regulation="emit('stop-regulation')"
                    @update:kd="emit('update:kd', $event)"
                    @update:ki="emit('update:ki', $event)"
                    @update:kp="emit('update:kp', $event)"
                    @update:mode2="emit('update:mode2', $event)"
                    @update:target-rpm="emit('update:target-rpm', $event)"
                    @update:motor-target="emit('update:motor-target', $event)"
                ></MotorRegulation>
            </BaseCard>
        </div>
    </BaseCard>
</template>
