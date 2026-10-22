<script setup lang="ts">
const isOpen = defineModel<boolean>('open', { required: true });

const reportUrl = ref('');
const reportReason = ref('');
const token = ref('');
const loading = ref(false);
const success = ref(false);
const error = ref('');
const turnstile = ref<{ reset: () => void } | null>(null);

async function submitReport() {
    loading.value = true;
    success.value = false;
    error.value = '';

    try {
        await $fetch('/api/report', {
            method: 'POST',
            body: {
                url: reportUrl.value,
                reason: reportReason.value,
                token: token.value,
            },
        });

        success.value = true;
        reportUrl.value = '';
        reportReason.value = '';
    } catch (cause) {
        const fetchError = cause as { data?: { statusMessage?: string }; message?: string };
        error.value = fetchError.data?.statusMessage || fetchError.message || 'Could not send the report.';
    } finally {
        loading.value = false;
        token.value = '';
        turnstile.value?.reset();
    }
}
</script>

<template>
    <UModal
        v-model:open="isOpen"
        title="Report URL"
        description="Let us know about a suspicious or unsafe link."
    >
        <template #body>
            <form class="flex flex-col gap-3" @submit.prevent="submitReport">
                <UInput
                    v-model="reportUrl"
                    type="url"
                    label="URL"
                    placeholder="Enter the URL you want to report"
                    required
                    :disabled="loading"
                />

                <UTextarea
                    v-model="reportReason"
                    label="Reason"
                    placeholder="Enter the reason for reporting this URL"
                    required
                    :disabled="loading"
                />

                <NuxtTurnstile
                    ref="turnstile"
                    v-model="token"
                    :options="{ appearance: 'interaction-only' }"
                />

                <UAlert v-if="success" color="success" title="Report sent. Thank you!" />
                <UAlert v-if="error" color="error" title="Report could not be sent" :description="error" />

                <UButton
                    color="primary"
                    type="submit"
                    :loading="loading"
                    :disabled="!token || loading"
                >
                    Submit Report
                </UButton>
            </form>
        </template>
    </UModal>
</template>
