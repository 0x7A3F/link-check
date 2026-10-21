<script setup lang="ts">
import { ref } from 'vue';
import ReportModal from './ReportModal.vue';

const isModalOpen = ref(false);
</script>

<template>
    <UButton
        color="neutral"
        variant="outline"
        icon="i-lucide-flag"
        @click="isModalOpen = true"
    >
        Report URL
    </UButton>

    <ReportModal v-model:open="isModalOpen" />
</template>