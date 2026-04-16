<script setup lang="ts">
defineProps<{
  variant?: 'primary' |'success' | 'danger' | 'neutral' | 'disabled' | 'warning'
}>()
</script>

<template>
  <button
    :class="[
      'px-4 py-2 rounded-xl font-semibold text-white',
      variant === 'primary' && 'bg-blue-500',
      variant === 'success' && 'bg-green-500',
      variant === 'danger' && 'bg-red-500',
      variant === 'neutral' && 'bg-gray-500',
      variant === 'warning' && 'bg-yellow-500',
      variant === 'disabled' && 'bg-amber-950'
    ]"
  >
    <slot></slot>
  </button>
</template>