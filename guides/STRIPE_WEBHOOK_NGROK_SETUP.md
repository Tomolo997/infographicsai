# Stripe Webhook with ngrok Setup

## Why Use ngrok?

Instead of using Stripe CLI forwarding, you can expose your local Django server directly to Stripe using ngrok. This is useful for:
- Testing webhooks in a more production-like environment
- Testing webhook signature verification
- Allowing Stripe Dashboard to send test webhooks directly

---

## Quick Setup

### 1. Start Your Django Server

```bash
cd /Users/ovsenjak/Desktop/infoai/app
python manage.py runserver
```

Your server should be running on `http://localhost:8000`

### 2. Start ngrok

In a **new terminal**, run:

```bash
ngrok http 8000
```

You'll see output like:
```
Session Status                online
Account                       Your Account (Plan: Free)
Version                       3.x.x
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok-free.app -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

### 3. Your Webhook URL

Your webhook URL will be:
```
https://abc123.ngrok-free.app/api/account/stripe-webhook/
```

**Note:** Replace `abc123.ngrok-free.app` with your actual ngrok domain (shown in the "Forwarding" line).

---

## Using the ngrok URL

### Option A: Stripe Dashboard (Recommended for Testing)

1. Go to: https://dashboard.stripe.com/webhooks
2. Click "Add endpoint"
3. Enter your ngrok URL:
   ```
   https://abc123.ngrok-free.app/api/account/stripe-webhook/
   ```
4. Select events:
   - `checkout.session.completed`
   - `checkout.session.async_payment_succeeded`
5. Click "Add endpoint"
6. Copy the **Signing secret** (starts with `whsec_`)
7. Add to your `.env`:
   ```bash
   STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
   ```

### Option B: Stripe CLI (Alternative)

You can still use Stripe CLI, but point it to your ngrok URL:

```bash
# Not needed if using Stripe Dashboard
stripe listen --forward-to https://abc123.ngrok-free.app/api/account/stripe-webhook/
```

---

## Important Notes

### ngrok URL Changes

⚠️ **Free ngrok URLs change every time you restart ngrok!**

- Each time you run `ngrok http 8000`, you get a new random URL
- You'll need to update the webhook URL in Stripe Dashboard each time
- Or use a **paid ngrok plan** for a static domain

### Keep ngrok Running

- Keep the ngrok terminal window open while testing
- If you close it, the webhook URL stops working
- Restart ngrok = new URL = update Stripe Dashboard

### Webhook Secret

- Get the signing secret from Stripe Dashboard (not from Stripe CLI)
- The secret is tied to the specific webhook endpoint
- Add it to your `.env` file

---

## Testing

### 1. Test Webhook from Stripe Dashboard

1. Go to: Stripe Dashboard → Developers → Webhooks
2. Click on your webhook endpoint
3. Click "Send test webhook"
4. Select: `checkout.session.completed`
5. Click "Send test webhook"
6. Check your Django logs for the webhook processing

### 2. Test with Real Purchase

1. Make a test purchase in your app
2. Use test card: `4242 4242 4242 4242`
3. Complete payment
4. Check Django logs for webhook event
5. Verify credits were added

### 3. Check ngrok Requests

Visit: `http://127.0.0.1:4040` (ngrok web interface)
- See all incoming requests
- Inspect request/response details
- Debug webhook issues

---

## Complete Setup Example

### Terminal 1: Django Server
```bash
cd /Users/ovsenjak/Desktop/infoai
source env/bin/activate
cd app
python manage.py runserver
```

### Terminal 2: ngrok
```bash
ngrok http 8000
```

**Output:**
```
Forwarding    https://abc123.ngrok-free.app -> http://localhost:8000
```

### Terminal 3: Check ngrok (Optional)
```bash
# Visit in browser
open http://127.0.0.1:4040
```

### Stripe Dashboard Setup

1. **Webhook URL:** `https://abc123.ngrok-free.app/api/account/stripe-webhook/`
2. **Events:**
   - `checkout.session.completed`
   - `checkout.session.async_payment_succeeded`
3. **Signing Secret:** Copy `whsec_xxxxx` to `.env`

---

## Troubleshooting

### "Webhook endpoint not reachable"

- ✅ Make sure Django server is running on port 8000
- ✅ Make sure ngrok is running and forwarding to port 8000
- ✅ Check ngrok URL is correct in Stripe Dashboard
- ✅ Try accessing the URL in browser: `https://abc123.ngrok-free.app/api/account/stripe-webhook/` (should return 400, not 404)

### "Invalid signature"

- ✅ Make sure `STRIPE_WEBHOOK_SECRET` is set in `.env`
- ✅ Make sure you copied the secret from the correct webhook endpoint
- ✅ Restart Django server after adding the secret

### "ngrok URL changed"

- ✅ Free ngrok URLs change on restart
- ✅ Update webhook URL in Stripe Dashboard
- ✅ Or use paid ngrok for static domain

### Webhook not received

- ✅ Check ngrok web interface: `http://127.0.0.1:4040`
- ✅ Check Django logs for errors
- ✅ Verify webhook URL in Stripe Dashboard matches ngrok URL
- ✅ Make sure events are selected in Stripe Dashboard

---

## ngrok vs Stripe CLI

| Feature | ngrok | Stripe CLI |
|---------|-------|------------|
| **Setup** | `ngrok http 8000` | `stripe listen --forward-to ...` |
| **URL** | Changes each restart (free) | Uses localhost |
| **Stripe Dashboard** | Can send test webhooks | No |
| **Signature Verification** | Full (uses Dashboard secret) | Uses CLI secret |
| **Best For** | Production-like testing | Quick local testing |

**Recommendation:** Use ngrok when you want to test with Stripe Dashboard. Use Stripe CLI for quick local testing.

---

## Production

For production, you don't need ngrok. Use your actual domain:

```
https://yourdomain.com/api/account/stripe-webhook/
```

Set this up in Stripe Dashboard with your production webhook secret.

---

## Quick Reference

**Your Development Webhook URL (with ngrok):**
```
https://[your-ngrok-domain].ngrok-free.app/api/account/stripe-webhook/
```

**To get your ngrok domain:**
```bash
ngrok http 8000
# Look for: Forwarding https://abc123.ngrok-free.app -> http://localhost:8000
```

**Full URL format:**
```
https://abc123.ngrok-free.app/api/account/stripe-webhook/
```

---

**Ready to test!** Start ngrok, add the URL to Stripe Dashboard, and start receiving webhooks! 🚀

