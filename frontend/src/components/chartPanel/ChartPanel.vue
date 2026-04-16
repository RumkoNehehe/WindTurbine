<script setup lang="ts">

import type { DataSource } from '@/types/dataSource';
import BaseCard from '../base/BaseCard.vue';
import DataSourceToggle from './DataSourceToggle.vue';
import RecordingSelect from './RecordingSelect.vue';
import LineChart from './LineChart.vue';
import BaseButton from '../base/BaseButton.vue';

defineProps<{
    dataSource: DataSource
    selectedRecording: string
    isPaused: boolean
    points: {
        label: string,
        motor1: number,
        motor2: number
    }[]
    recordings: string[]
}>()

const emit = defineEmits<{
    (e: 'update:dataSource', value: DataSource): void
    (e: 'update:selectedRecording', value: string): void
    (e: 'upload-file'): void
    (e: 'resume-dataFlow'): void
    (e: 'pause-dataFlow'): void
    (e: 'clear-chart'): void
}>()
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

                    <DataSourceToggle :labels="['Live', 'Recorded']" :model-value="dataSource"
                        @update:model-value="emit('update:dataSource', $event)" />
                </div>

                <div v-if="dataSource === 'first'" class="flex flex-col gap-2 h-full">
                    <label class="text-sm font-semibold text-gray-800">
                        Data flow
                    </label>
                    <div class="pt-1">
                        <BaseButton v-if="isPaused" variant="primary" class="flex-1" @click="emit('resume-dataFlow')">
                            Resume
                        </BaseButton>

                        <BaseButton v-else-if="!isPaused" variant="warning" class="flex-1 p-1"
                            @click="emit('pause-dataFlow')">
                            Pause
                        </BaseButton>
                    </div>
                </div>

                <div class="flex flex-col gap-2 h-full">
                    <label class="text-sm font-semibold text-gray-800">
                        Chart data
                    </label>
                    <div class="pt-1">
                        <BaseButton variant="danger" @click="emit('clear-chart')" class="flex-1">
                            Clear
                        </BaseButton>
                    </div>
                </div>

                <div v-if="dataSource === 'second'" class="flex flex-col gap-2 h-full">
                    <label class="text-sm font-semibold text-gray-800">
                        Custom data
                    </label>
                    <div class="pt-1">
                        <BaseButton variant="primary" @click="emit('upload-file')" class="flex-1">
                            Upload file
                        </BaseButton>
                    </div>
                </div>

                <RecordingSelect v-if="dataSource === 'second'" :model-value="selectedRecording"
                    :recordings="recordings" @update:model-value="emit('update:selectedRecording', $event)" />
            </div>
        </BaseCard>
    </BaseCard>
</template>