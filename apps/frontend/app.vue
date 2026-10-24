<script setup lang="ts">
useSeoMeta({
    title: 'Link Check',
    ogImage: '/favicon.gif',
})

useHead({
    link: [
        { rel: 'icon', type: 'image/gif', href: '/favicon.gif' },
    ],
})
</script>

<template>
    <UApp>
        <NuxtPage />
    </UApp>
</template>