<script setup lang="ts">
import BaseCard from '../base/BaseCard.vue';
import BaseButton from '../base/BaseButton.vue';

const emit = defineEmits<{
    (e: 'download-file'): void
}>()
</script>

<template>
    <BaseCard variant="light" class="flex justify-evenly">
        <BaseButton variant="neutral">
            Select a recording
        </BaseButton>

        <BaseButton variant="neutral" @click="emit('download-file')">
            Download file
        </BaseButton>
    </BaseCard>
</template>