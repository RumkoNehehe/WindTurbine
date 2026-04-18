<script setup lang="ts">

defineProps<{
    variant?: 'light' | 'dark'
}>()

</script>

<template>
  <div 
        :class="['rounded-2xl p-4 shadow',
            variant === 'dark' && 'bg-gray-400',
            variant === 'light' && 'bg-gray-200'
        ]">
    <slot></slot>
  </div>
</template>