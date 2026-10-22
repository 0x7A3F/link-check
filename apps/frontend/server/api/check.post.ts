export default defineEventHandler(async (event) => {
    const body = await readBody<{ url?: string; token?: string }>(event);

    if (!body?.url || !body.token) {
        throw createError({
            statusCode: 400,
            statusMessage: "A URL and Turnstile token are required.",
        });
    }

    const verification = await verifyTurnstileToken(body.token, event);
    if (!verification.success) {
        throw createError({
            statusCode: 403,
            statusMessage: "Turnstile verification failed. Please try again.",
        });
    }

    const config = useRuntimeConfig(event);
    return await $fetch(`${config.public.apiBase}/api/check`, {
        method: "POST",
        body: { url: body.url },
    });
});
