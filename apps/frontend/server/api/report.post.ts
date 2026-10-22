export default defineEventHandler(async (event) => {
    const body = await readBody<{ url?: string; reason?: string; token?: string }>(event);
    const url = body?.url?.trim();
    const reason = body?.reason?.trim();
    const token = body?.token;

    if (!url || !reason || !token || reason.length > 5000) {
        throw createError({
            statusCode: 400,
            statusMessage: 'A URL, a reason (up to 5000 characters), and a Turnstile token are required.',
        });
    }

    let parsedUrl: URL;
    try {
        parsedUrl = new URL(url);
    } catch {
        throw createError({
            statusCode: 400,
            statusMessage: 'Enter a valid URL.',
        });
    }

    if (!['http:', 'https:'].includes(parsedUrl.protocol)) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Only HTTP and HTTPS URLs can be reported.',
        });
    }

    const verification = await verifyTurnstileToken(token, event);
    if (!verification.success) {
        throw createError({
            statusCode: 403,
            statusMessage: 'Turnstile verification failed. Please try again.',
        });
    }

    const config = useRuntimeConfig(event);
    if (!config.reportToEmail || !config.emailFrom || !config.resend.apiKey) {
        throw createError({
            statusCode: 500,
            statusMessage: 'Email reporting is not configured on the server.',
        });
    }

    const { error } = await useResend().emails.send({
        from: config.emailFrom,
        to: config.reportToEmail,
        subject: `URL reported: ${parsedUrl.hostname}`,
        text: `A URL was reported.\n\nURL: ${parsedUrl.href}\n\nReason:\n${reason}`,
    });

    if (error) {
        console.error('Failed to send URL report email:', error);
        throw createError({
            statusCode: 502,
            statusMessage: 'The report email could not be sent. Please try again later.',
        });
    }

    return { success: true };
});
