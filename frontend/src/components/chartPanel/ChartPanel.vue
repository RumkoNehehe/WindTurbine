<script setup lang="ts">
import type { ChartDataSource } from "@/types/chartDataSource";
import BaseCard from "../base/BaseCard.vue";
import DataSourceToggle from "../base/BaseToggle.vue";
import RecordingSelect from "./RecordingSelect.vue";
import LineChart from "./LineChart.vue";
import BaseButton from "../base/BaseButton.vue";

defineProps<{
    chartDataSource: ChartDataSource;
    selectedRecording: string;
    isPaused: boolean;
    points: {
        label: string;
        motor1: number;
        motor2: number;
    }[];
    recordings: string[];
}>();

const emit = defineEmits<{
    (e: "update:chart-data-source", value: ChartDataSource): void;
    (e: "update:selected-recording", value: string): void;
    (e: "upload-file", value: Event): void;
    (e: "resume-data-flow"): void;
    (e: "pause-data-flow"): void;
    (e: "clear-chart"): void;
}>();

const chartSourceOptions = [
    { label: "Live", value: "live" },
    { label: "Recorded", value: "recorded" },
] as const
</script>

<template>
    <BaseCard variant="dark" class="flex h-full flex-col gap-4">
        <BaseCard variant="light" class="flex-1 min-h-0">
            <div class="h-full">
                <LineChart :points="points" />
            </div>
        </BaseCard>
        <BaseCard variant="light" class="flex">
            <div class="flex flex-row gap-4 justify-between w-full">
                <div class="flex flex-col gap-2">
                    <label class="text-sm font-semibold text-gray-800">
                        Source
                    </label>

                    <DataSourceToggle
                        :model-value="chartDataSource"
                        :options="chartSourceOptions"
                        @update:model-value="emit('update:chart-data-source', $event as ChartDataSource)"
                    />
                </div>

                <div
                    v-if="chartDataSource === 'live'"
                    class="flex flex-col gap-2 h-full"
                >
                    <label class="text-sm font-semibold text-gray-800">
                        Data flow
                    </label>
                    <div class="pt-1">
                        <BaseButton
                            v-if="isPaused"
                            variant="primary"
                            class="flex-1"
                            @click="emit('resume-data-flow')"
                        >
                            Resume
                        </BaseButton>

                        <BaseButton
                            v-else-if="!isPaused"
                            variant="warning"
                            class="flex-1 p-1"
                            @click="emit('pause-data-flow')"
                        >
                            Pause
                        </BaseButton>
                    </div>
                </div>

                <div class="flex flex-col gap-2 h-full">
                    <label class="text-sm font-semibold text-gray-800">
                        Chart data
                    </label>
                    <div class="pt-1">
                        <BaseButton
                            variant="danger"
                            @click="emit('clear-chart')"
                            class="flex-1"
                        >
                            Clear
                        </BaseButton>
                    </div>
                </div>

                <div
                    v-if="chartDataSource === 'recorded'"
                    class="flex flex-col gap-2 h-full"
                >
                    <label class="text-sm font-semibold text-gray-800">
                        Custom data
                    </label>
                    <div class="pt-1">
                        <div class="flex flex-col gap-2">
                            <label
                                for="upload-recording"
                                class="cursor-pointer rounded-xl bg-gray-300 px-4 py-2 font-semibold text-gray-800"
                            >
                                Upload recording
                            </label>

                            <input
                                id="upload-recording"
                                type="file"
                                accept=".json,application/json"
                                class="hidden"
                                @change="emit('upload-file', $event)"
                            />
                        </div>
                    </div>
                </div>

                <RecordingSelect
                    v-if="chartDataSource === 'recorded'"
                    :selectedRecording="selectedRecording"
                    :recordings="recordings"
                    @update:selected-recording="
                        emit('update:selected-recording', $event)
                    "
                />
            </div>
        </BaseCard>
    </BaseCard>
</template>
