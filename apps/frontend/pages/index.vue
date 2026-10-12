<script setup lang="ts">
definePageMeta({
  layout: 'dashboard'
})
</script>

<template>
  <uDashboardPanel>
    <template #header>
      <uDashboardNavbar title="Home Page" icon="i-lucide-house"/>
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
  </uDashboardPanel>
</template>