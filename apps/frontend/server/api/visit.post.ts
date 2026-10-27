export default defineEventHandler(async (event) => {
    const ip = getRequestHeader(event, "cf-connecting-ip")
        || getRequestIP(event, { xForwardedFor: true })
        || "";

    const config = useRuntimeConfig(event);
    await $fetch(`${config.public.apiBase}/api/visit`, {
        method: "POST",
        body: { ip },
    }).catch(() => {});

    setResponseStatus(event, 204);
    return null;
});
