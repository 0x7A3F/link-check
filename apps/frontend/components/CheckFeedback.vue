<script setup lang="ts">
defineProps<{
  result: { url: string; status: string; message: string } | null;
  error: string;
}>();
</script>

<template>
  <UAlert
    v-if="result"
    :color="result.status === 'ok' ? 'success' : 'error'"
    variant="subtle"
    :icon="result.status === 'ok'
      ? 'i-lucide-shield-check'
      : 'i-lucide-shield-alert'"
    :title="result.status.toUpperCase()"
    :description="result.message"
  />

  <UAlert
    v-if="error"
    color="error"
    variant="subtle"
    icon="i-lucide-circle-alert"
    title="Error"
    :description="error"
  />
</template>