<script setup lang="ts">
const isOpen = defineModel<boolean>('open', { required: true });

const reportUrl = ref('');
const reportReason = ref('');
</script>

<template>
    <UModal
        v-model:open="isOpen"
        title="Report URL"
        description="Let us know about a suspicious or unsafe link."
    >
        <template #body>
            <p class="text-sm text-muted">
                <form
                    class="flex flex-col gap-2"
                >
                    <UInput
                        v-model="reportUrl"
                        label="URL"
                        placeholder="Enter the URL you want to report"
                        required
                    />

                    <UTextarea
                        v-model="reportReason"
                        label="Reason"
                        placeholder="Enter the reason for reporting this URL"
                        required
                    />

                    <UButton
                        color="primary"
                        type="submit"
                    >
                        Submit Report
                    </UButton>
                </form>
            </p>
        </template>
    </UModal>
</template>
