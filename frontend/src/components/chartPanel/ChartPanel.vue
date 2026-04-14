<script setup lang="ts">

import type { DataSource } from '@/types/dataSource';
import BaseCard from '../base/BaseCard.vue';
import DataSourceToggle from './DataSourceToggle.vue';
import RecordingSelect from './RecordingSelect.vue';

defineProps<{
    dataSource: DataSource
    selectedRecording: string
    recordings: string[]
}>()

const emit = defineEmits<{
    (e: 'update:dataSource', value: DataSource): void
    (e: 'update:selectedRecording', value: string): void
}>()
</script>

<template>
    <BaseCard variant="dark" class="flex h-full flex-col gap-4">
        <BaseCard variant="light" class="flex-1 min-h-0"></BaseCard>
        <BaseCard variant="light" class="flex">
            <div class="flex flex-row gap-4 justify-between w-full" >
                <div class="flex flex-col gap-2">
                    <label class="text-sm font-semibold text-gray-800">
                        Source
                    </label>

                    <DataSourceToggle :model-value="dataSource"
                        @update:model-value="emit('update:dataSource', $event)" />
                </div>

                <RecordingSelect v-if="dataSource === 'customData'" :model-value="selectedRecording"
                    :recordings="recordings" @update:model-value="emit('update:selectedRecording', $event)" />
            </div>
        </BaseCard>
    </BaseCard>
</template>