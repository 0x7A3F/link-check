<script setup lang="ts">
defineProps<{ loading: boolean }>();
const url = defineModel<string>({ required: true });
defineEmits<{ submit: [] }>();
</script>

<template>
    <form class="flex gap-2" @submit.prevent="$emit('submit')">
        <UInput
            v-model="url"
            class="flex-1"
            size="xl"
            type="url"
            icon="i-lucide-link"
            placeholder="https://example.com/free-iphone"
            :disabled="loading"
            required
        />

        <UButton
            type="submit"
            size="xl"
            icon="i-lucide-search"
            :loading="loading"
        >
            Check
        </UButton>
    </form>
</template>