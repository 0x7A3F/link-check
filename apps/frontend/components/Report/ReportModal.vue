<script setup lang="ts">
const isOpen = defineModel<boolean>('open', { required: true });
</script>

<template>
    <UModal
        v-model:open="isOpen"
        title="Report URL"
        description="Let us know about a suspicious or unsafe link."
    >
        <template #body>
            <p class="text-sm text-muted">
                WIP
            </p>
        </template>
    </UModal>
</template>
