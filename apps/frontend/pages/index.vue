<script setup lang="ts">
import { ref } from "vue";

const url = ref("");
const loading = ref(false);

async function checkUrl() {}
</script>

<template>
    <div class="mx-auto flex min-h-screen w-full max-w-2xl flex-col justify-center gap-6 px-4 py-10">
        <div class="text-center">
            <h1 class="text-3xl font-bold">Is this link sus?</h1>
            <p class="mt-2 text-muted">
                Paste a URL, and we check how likely it is to be a scam.
            </p>
        </div>

        <UCard>
            <form class="flex gap-2" @submit.prevent="checkUrl">
                <UInput
                    v-model="url"
                    class="flex-1"
                    size="xl"
                    icon="i-lucide-link"
                    placeholder="https://example.com/free-iphone"
                    :disabled="loading"
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
        </UCard>
    </div>
</template>
