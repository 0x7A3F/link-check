<script setup lang="ts">
import { onMounted, ref } from "vue";

const url = ref("");
const turnstileToken = ref("");
const checkForm = ref<{ resetTurnstile: () => void } | null>(null);
const loading = ref(false);
const result = ref<{ url: string, status: string, message: string } | null>(null);
const error = ref("");

onMounted(() => {
    $fetch("/api/visit", { method: "POST" }).catch(() => {});
});

async function checkUrl() {
    if (!url.value.trim()) return;

    loading.value = true;
    error.value = "";
    result.value = null;

    try {
        const parsedUrl = new URL(url.value);

        if (!["http:", "https:"].includes(parsedUrl.protocol)) {
            throw new Error("Only HTTP and HTTPS URLs are supported.")
        }

        const res = await fetch("/api/check", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                url: url.value,
                token: turnstileToken.value,
            })
        });

        if (!res.ok) {
            throw new Error(res.statusText || `Server: ${res.status}`);
        }

        result.value = await res.json();
    } catch (e) {
        error.value = e instanceof Error ? e.message : "Something went wrong";
    } finally {
        loading.value = false;
        turnstileToken.value = "";
        checkForm.value?.resetTurnstile();
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
            <UrlCheckForm
                ref="checkForm"
                v-model="url"
                v-model:token="turnstileToken"
                :loading="loading"
                @submit="checkUrl"
            />
        </UCard>

        <CheckFeedback :result="result" :error="error" />

        <div class="flex justify-end">
            <ReportButton />
        </div>
    </div>
</template>
