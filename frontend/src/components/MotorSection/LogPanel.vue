<script setup lang="ts">
import BaseCard from '../base/BaseCard.vue';


defineProps<{
    logs: string[]
}>()
</script>

<template>
    <BaseCard variant="light" class="min-h-0 flex-1">
        <div class="flex h-full min-h-0 flex-col">
            <h2 class="text-xl font-bold mb-2">Logs</h2>

            <div class="min-h-0 flex-1 overflow-y-auto">
                <ul v-if="logs.length > 0" class="space-y-2">
                    <li v-for="(log, index) in logs" :key="index"
                        class="rounded-md bg-white px-3 py-2 text-sm shadow-sm">
                        {{ log }}
                    </li>
                </ul>

                <p v-else class="text-sm text-gray-500">
                    No logs available.
                </p>
            </div>
        </div>
    </BaseCard>
</template>