<script setup lang="ts">
const props = defineProps<{
  result: { url: string; status: string; message: string } | null;
  error: string;
}>();

const resultStatus = computed(() => props.result?.status.trim().toLowerCase());
const resultTitle = computed(() => {
  if (resultStatus.value === "ok") return "No warning signs detected";
  if (resultStatus.value === "suspicious") return "Potential warning signs found";
  return "Check result";
});
const resultColor = computed(() => {
  if (resultStatus.value === "ok") return "success";
  if (resultStatus.value === "suspicious") return "warning";
  return "neutral";
});
const resultIcon = computed(() => {
  if (resultStatus.value === "ok") return "i-lucide-shield-check";
  if (resultStatus.value === "suspicious") return "i-lucide-shield-alert";
  return "i-lucide-info";
});
</script>

<template>
  <div v-if="result" class="flex flex-col gap-3" role="status" aria-live="polite">
    <UAlert
      :color="resultColor"
      variant="subtle"
      :icon="resultIcon"
      :title="resultTitle"
      :description="result.message"
    />

    <p class="break-all text-sm text-muted">
      Checked URL: {{ result.url }}
    </p>

    <p class="text-sm text-muted">
      This check looks for known URL shorteners and suspicious words in the URL.
      No warning signs does not guarantee that a site is safe.
    </p>
  </div>

  <UAlert
    v-if="error"
    color="error"
    variant="subtle"
    icon="i-lucide-circle-alert"
    title="Error"
    :description="error"
  />
</template>