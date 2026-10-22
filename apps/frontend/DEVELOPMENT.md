# frontend

Thanks for contributing to my project, this is how you get a development environment running.

> [!TIP]
> Need help? I'll be happy to help you via email: hi@sander.tf

## Things you Need
- Node.js
- NPM for dependencies

## Setting up the environment
Navigate to the `apps/frontend/` directory with `cd apps/frontend`.

### Copy Example Files
Copy the example files to their correct destination. Please fill them in after copying them.

```bash
Copy-Item .env.example .env
```

Set `NUXT_PUBLIC_TURNSTILE_SITE_KEY` to your Cloudflare Turnstile site key and
`NUXT_TURNSTILE_SECRET_KEY` to its secret key. The secret is used only by the
Nuxt server to verify tokens; never expose it as a public variable.

For URL reports, also set `NUXT_RESEND_API_KEY`, `NUXT_REPORT_TO_EMAIL`, and
`NUXT_EMAIL_FROM`. The sender address must use a domain verified in Resend.
These settings are server-only. The root `.env.example` includes the same
settings for Docker Compose.

### Install node dependencies
The frontend is built with Nuxt, we need to install those dependencies.

```bash
npm install
```