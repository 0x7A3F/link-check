export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig(event);
    await $fetch(`${config.public.apiBase}/api/visit`, { method: "POST" });
    return { success: true };
});
