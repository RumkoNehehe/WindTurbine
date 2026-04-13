<script setup lang="ts">
import BaseCard from '../base/BaseCard.vue';
import RecordingActionsMenu from './RecordingActionsMenu.vue';


</script>

<template>
    <BaseCard variant="dark" class="space-y-4">
       <BaseCard variant="light" class="h-60"></BaseCard>
        <RecordingActionsMenu></RecordingActionsMenu>
    </BaseCard>
</template>