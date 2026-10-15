<script setup lang="ts">
import { ref } from "vue";

const API_URL = "http://localhost:8000";

const url = ref("");
const loading = ref(false);
const result = ref<{ url: string, status: string, message: string } | null>(null);
const error = ref("");

async function checkUrl() {
    loading.value = true;
    error.value = "";
    result.value = null;

    try {
        const res = await fetch(`${API_URL}/api/check`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: url.value })
        });

        if (!res.ok) throw new Error(`Server: ${res.status}`);

        result.value = await res.json();
    } catch (e) {
        error.value = e instanceof Error ? e.message : "Something went wrong";
    }  finally {
        loading.value = false;
    }
}
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

        <UAlert
            v-if="result"
            color="info"
            variant="subtle"
            icon="i-lucide-construction"
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
    </div>
</template>
