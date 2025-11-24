# Stripe Credits Webhook Setup Guide

## Overview

This guide explains how to set up Stripe webhooks for credit purchases in both development and production environments.

## Architecture

### Flow
1. User clicks "Purchase" on a credit pack
2. Frontend calls `/account/purchase-credits/` with `price_id`
3. Backend creates Stripe Checkout Session
4. User completes payment on Stripe
5. Stripe sends webhook event to `/account/stripe-webhook/`
6. Webhook handler:
   - Verifies webhook signature
   - Identifies the user by email
   - Finds the credit pack by price_id
   - Calls `account.fill_credits(credits)`
   - Creates `CreditPurchase` record

### Models Updated
- `Account.fill_credits(credits)` - Adds credits and marks user as non-trial
- `CreditPurchase` - Records the purchase for audit trail

---

## Development Setup (Testing)

### 1. Install Stripe CLI

```bash
# macOS
brew install stripe/stripe-cli/stripe

# Linux/Windows - Download from:
# https://stripe.com/docs/stripe-cli
```

### 2. Login to Stripe CLI

```bash
stripe login
```

This will open a browser to authorize the CLI with your Stripe account.

### 3. Forward Webhooks to Local Server

```bash
# Start your Django server first (port 8000)
python manage.py runserver

# In another terminal, forward webhooks
stripe listen --forward-to localhost:8000/account/stripe-webhook/
```

You'll see output like:
```
> Ready! Your webhook signing secret is whsec_xxxxx (^C to quit)
```

### 4. Set Webhook Secret in Environment

Copy the `whsec_xxxxx` value and add to your `.env` file:

```bash
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
```

**Note:** In development, the webhook signature verification is optional. If `STRIPE_WEBHOOK_SECRET` is not set, the webhook will still work but will log a warning.

### 5. Test the Flow

#### Option A: Use Stripe Test Cards

1. Go to your app: `http://localhost:3000/dashboard/credits`
2. Click "Purchase" on any credit pack
3. Use test card: `4242 4242 4242 4242`
   - Any future expiry date
   - Any 3-digit CVC
   - Any postal code
4. Complete payment
5. Check your terminal logs for webhook processing

#### Option B: Trigger Test Events via CLI

```bash
# Trigger a test checkout.session.completed event
stripe trigger checkout.session.completed
```

### 6. Verify Credits Were Added

```bash
# Django shell
python manage.py shell

from account.models import Account, CreditPurchase
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(email='your-test-email@example.com')
account = Account.objects.get(user=user)

print(f"Credit Balance: {account.credit_balance}")
print(f"Is Trial User: {account.is_trial_user}")

# Check purchase records
purchases = CreditPurchase.objects.filter(account=account)
for p in purchases:
    print(f"Purchase: {p.credit_pack.name} - {p.quantity} credits for ${p.price}")
```

---

## Production Setup

### 1. Configure Stripe Webhook Endpoint

Go to: https://dashboard.stripe.com/webhooks

1. Click "Add endpoint"
2. Enter your webhook URL: `https://yourdomain.com/account/stripe-webhook/`
3. Select events to listen to:
   - `checkout.session.completed`
4. Click "Add endpoint"

### 2. Get Webhook Signing Secret

After creating the endpoint:
1. Click on the endpoint in the Stripe Dashboard
2. Click "Reveal" under "Signing secret"
3. Copy the `whsec_xxxxx` value

### 3. Set Environment Variables

Add to your production environment:

```bash
# Required
STRIPE_SECRET_KEY=sk_live_xxxxx
STRIPE_PUBLISHABLE_KEY=pk_live_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx  # From step 2

# Already configured
FRONTEND_URL=https://yourdomain.com
```

**Important:** In production, `STRIPE_WEBHOOK_SECRET` is required for security. The webhook will verify the signature to ensure events are coming from Stripe.

### 4. Deploy and Verify

After deployment:

1. Make a test purchase using test mode in Stripe Dashboard
2. Check your server logs for webhook events
3. Verify credits are added to user accounts
4. Monitor webhook deliveries in Stripe Dashboard

### 5. Monitor Webhook Health

In Stripe Dashboard > Webhooks:
- Check "Recent deliveries" tab
- Look for failed deliveries (red X)
- Click on failures to see error details
- Stripe will retry failed webhooks automatically

---

## Webhook Security

### Development
- Signature verification is optional (will log warning)
- Uses test mode keys and test cards
- No real money involved

### Production
- **Signature verification is REQUIRED**
- Set `STRIPE_WEBHOOK_SECRET` environment variable
- The webhook verifies that events come from Stripe
- Prevents malicious actors from triggering fake purchases

### How Signature Verification Works

```python
# In StripeWebhookView.post()
if webhook_secret:
    # Verifies the signature using STRIPE_WEBHOOK_SECRET
    event = stripe.Webhook.construct_event(
        payload, sig_header, webhook_secret
    )
else:
    # Development only - NOT SECURE
    event = json.loads(payload)
```

---

## Troubleshooting

### Webhook Not Receiving Events

1. **Check URL is accessible:**
   ```bash
   curl -X POST https://yourdomain.com/account/stripe-webhook/
   ```
   Should return 400 (not 404)

2. **Check Stripe Dashboard > Webhooks > Recent deliveries**
   - Are events being sent?
   - What's the response code?
   - View request/response details

3. **Check server logs for errors**

### Credits Not Being Added

1. **Check webhook logs:**
   ```python
   # In handle_successful_payment, all errors are logged
   logger.error(...)
   ```

2. **Common issues:**
   - User email doesn't match any account
   - Price ID doesn't match any CreditPack
   - CreditPack missing `stripe_price_id`

3. **Verify credit pack setup:**
   ```bash
   python manage.py shell
   
   from account.models import CreditPack
   packs = CreditPack.objects.all()
   for pack in packs:
       print(f"{pack.name}: {pack.stripe_price_id}")
   ```

### Signature Verification Failing

1. **Wrong webhook secret:** 
   - Each endpoint has unique secret
   - Copy from correct endpoint in Stripe Dashboard

2. **Request proxy/modification:**
   - Some proxies modify request body
   - Breaks signature verification
   - Configure proxy to pass through untouched

---

## Testing Checklist

### Development Testing
- [ ] Stripe CLI installed and logged in
- [ ] Webhook forwarding running
- [ ] Test purchase with card `4242 4242 4242 4242`
- [ ] Credits added to account
- [ ] `is_trial_user` changed to `False`
- [ ] `CreditPurchase` record created
- [ ] Webhook logs show success

### Production Testing
- [ ] Webhook endpoint created in Stripe Dashboard
- [ ] `STRIPE_WEBHOOK_SECRET` environment variable set
- [ ] Test mode purchase successful
- [ ] Live mode purchase successful (small amount)
- [ ] Webhook deliveries show green checkmarks
- [ ] Credits added correctly
- [ ] Purchase records accurate

---

## API Endpoints

### POST `/account/purchase-credits/`
- **Auth:** Required
- **Body:** `{ "price_id": "price_xxxxx" }`
- **Response:** `{ "checkout_url": "https://checkout.stripe.com/..." }`

### POST `/account/stripe-webhook/`
- **Auth:** None (verified by signature)
- **Body:** Stripe event payload
- **Events:** `checkout.session.completed`
- **Response:** `{ "status": "success" }`

---

## Credit Pack Setup

Ensure your credit packs have Stripe price IDs:

```bash
# Run the management command to sync with Stripe
python manage.py create_credit_packs
```

This creates/updates products and prices in Stripe and syncs the `stripe_price_id` to your database.

---

## Support

- Stripe Docs: https://stripe.com/docs/webhooks
- Stripe CLI: https://stripe.com/docs/stripe-cli
- Test Cards: https://stripe.com/docs/testing

