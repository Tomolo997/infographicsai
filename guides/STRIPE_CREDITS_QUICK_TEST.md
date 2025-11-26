# Quick Test Guide - Stripe Credits

## 1-Minute Setup (Development)

### Install Stripe CLI

```bash
brew install stripe/stripe-cli/stripe  # macOS
stripe login
```

### Start Webhook Forwarding

```bash
# Terminal 1: Django server
cd /Users/ovsenjak/Desktop/infoai
source env/bin/activate
cd app
python manage.py runserver

# Terminal 2: Stripe webhook forwarding
stripe listen --forward-to localhost:8000/account/stripe-webhook/
```

**Copy the webhook secret** from Terminal 2 output (starts with `whsec_`)

### Add to .env

```bash
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx  # From above
```

## Test Purchase Flow

### 1. Open Credits Page

```
http://localhost:3000/dashboard/credits
```

### 2. Click "Purchase" on Any Pack

### 3. Use Test Card

```
Card: 4242 4242 4242 4242
Expiry: Any future date (e.g., 12/34)
CVC: Any 3 digits (e.g., 123)
ZIP: Any 5 digits (e.g., 12345)
```

### 4. Complete Payment

### 5. Verify Credits Added

**Check terminal logs** - you should see:

```
Successfully added XXX credits to user@example.com
```

**Check in Django shell:**

```bash
python manage.py shell
```

```python
from account.models import Account, CreditPurchase
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(email='your-email@example.com')
account = user.account

print(f"Credits: {account.credit_balance}")
print(f"Trial user: {account.is_trial_user}")  # Should be False

# Check purchases
purchases = CreditPurchase.objects.filter(account=account)
for p in purchases:
    print(f"{p.created_at}: {p.credit_pack.name} - {p.quantity} credits")
```

## Common Test Cards

| Card Number         | Scenario                      |
| ------------------- | ----------------------------- |
| 4242 4242 4242 4242 | Success                       |
| 4000 0000 0000 9995 | Declined (insufficient funds) |
| 4000 0025 0000 3155 | Requires authentication       |

Full list: https://stripe.com/docs/testing

## Troubleshooting

### "No webhook secret found"

- Make sure `.env` has `STRIPE_WEBHOOK_SECRET=whsec_xxxxx`
- Restart Django server after adding it

### Credits Not Added

1. Check Terminal 2 (stripe listen) - is event received?
2. Check Terminal 1 (Django) - any errors?
3. Verify email matches: Checkout email = Account email

### Test Without Stripe CLI

You can test without webhook forwarding - just manually trigger the webhook:

```bash
curl -X POST http://localhost:8000/account/stripe-webhook/ \
  -H "Content-Type: application/json" \
  -d '{
    "type": "checkout.session.completed",
    "data": {
      "object": {
        "id": "cs_test_xxx",
        "customer_email": "user@example.com"
      }
    }
  }'
```

Note: This won't have real line items, so it will fail at finding the price_id.

## Production Testing

### Test Mode (Safe)

1. Go to Stripe Dashboard → Developers → Webhooks
2. Create endpoint: `https://yourdomain.com/account/stripe-webhook/`
3. Select: `checkout.session.completed`
4. Copy signing secret to production env
5. Use test cards (4242...) in production app

### Live Mode (Real Money)

1. Switch Stripe Dashboard to Live mode
2. Create webhook endpoint for live
3. Use real card with small amount
4. Verify credits added
5. Refund if needed (Stripe Dashboard → Payments)

## What Was Changed

**Minimal changes made:**

1. `app/account/views.py`:

   - Added `metadata` to checkout session
   - Added `StripeWebhookView` class (handles webhook)
   - Added `handle_successful_payment()` method

2. `app/account/urls.py`:

   - Added route: `stripe-webhook/`

3. `app/app/settings/`:
   - Added `STRIPE_WEBHOOK_SECRET` to dev/prod settings

That's it! No database changes, no frontend changes.

