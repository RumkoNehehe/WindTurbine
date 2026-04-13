<script setup lang="ts">
defineProps<{
  variant?: 'primary' | 'danger' | 'neutral' | 'disabled'
}>()
</script>

<template>
  <button
    :class="[
      'px-4 py-2 rounded-xl font-semibold text-white',
      variant === 'primary' && 'bg-green-500',
      variant === 'danger' && 'bg-red-500',
      variant === 'neutral' && 'bg-gray-500',
      variant === 'disabled' && 'bg-amber-950'
    ]"
  >
    <slot></slot>
  </button>
</template>