<script setup lang="ts">
defineProps<{ loading: boolean }>();
const url = defineModel<string>({ required: true });
const token = defineModel<string>("token", { required: true });
const clipboardError = ref("");
const turnstile = ref<{ reset: () => void } | null>(null);
defineEmits<{ submit: [] }>();

async function pasteFromClipboard() {
    clipboardError.value = "";

    if (!navigator.clipboard?.readText) {
        clipboardError.value = "Clipboard access is not supported by this browser.";
        return;
    }

    try {
        const text = (await navigator.clipboard.readText()).trim();
        if (!text) {
            clipboardError.value = "Your clipboard is empty.";
            return;
        }

        url.value = text;
    } catch {
        clipboardError.value = "Could not access the clipboard. Check your browser permissions and try again.";
    }
}

defineExpose({
    resetTurnstile: () => turnstile.value?.reset(),
});
</script>

<template>
    <form class="flex flex-col gap-3" @submit.prevent="$emit('submit')">
        <UInput
            v-model="url"
            size="xl"
            type="url"
            icon="i-lucide-link"
            placeholder="https://example.com/free-iphone"
            :disabled="loading"
            required
        >
            <template #trailing>
                <UButton
                    type="button"
                    size="sm"
                    color="neutral"
                    variant="ghost"
                    square
                    icon="i-lucide-clipboard"
                    aria-label="Paste from clipboard"
                    title="Paste from clipboard"
                    :disabled="loading"
                    @click="pasteFromClipboard"
                />
            </template>
        </UInput>

        <UAlert
            v-if="clipboardError"
            color="error"
            variant="subtle"
            icon="i-lucide-circle-alert"
            title="Could not paste URL"
            :description="clipboardError"
        />

        <NuxtTurnstile
            ref="turnstile"
            v-model="token"
            :options="{ appearance: 'interaction-only' }"
        />

        <UButton
            type="submit"
            size="xl"
            icon="i-lucide-search"
            :loading="loading"
            :disabled="!token"
        >
            Check
        </UButton>
    </form>
</template>