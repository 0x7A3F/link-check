<script setup lang="ts">
import { ref } from "vue";

const apiResult = ref<{ message: string; status: string } | null>(null);
const apiError = ref("");

async function testApi() {
    apiError.value = "";

    try {
        apiResult.value = await $fetch("http://localhost:8000/api/health");
    } catch (error) {
    apiError.value = error instanceof Error ? error.message : "Api Request Failed";
    }
}

definePageMeta({
  layout: "dashboard",
});
</script>

<template>
  <uDashboardPanel>
    <template #header>
      <uDashboardNavbar title="Home Page" icon="i-lucide-house" />
    </template>

    <div class="p-4">
      <label for="search" class="mb-2 block font-medium text-sm">Search</label>
      <input
        id="search"
        type="text"
        placeholder="Look up URL..."
        class="w-full rounded border border-gray-300 px-3 py-2 outline-none focus:border-blue-500"
      />
    </div>

    <button class="mt-3 rounded bg-blue-600 px-3 py-2 text-white" @click="testApi">
        Test API
    </button>

    <p v-if="apiResult" class="mt-3">{{ apiResult.message }} ({{ apiResult.status }})</p>
    <p v-if="apiError" class="mt-3 text-red-600">{{ apiError }}</p>
  </uDashboardPanel>
</template>
