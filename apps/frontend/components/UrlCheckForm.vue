<script setup lang="ts">
defineProps<{ loading: boolean }>();
const url = defineModel<string>({ required: true });
const token = defineModel<string>("token", { required: true });
const turnstile = ref<{ reset: () => void } | null>(null);
defineEmits<{ submit: [] }>();

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