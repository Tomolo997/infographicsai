# Stripe Credits Webhook - Changes Summary

## What Was Built

A webhook integration that automatically adds credits to user accounts when they complete a Stripe payment.

## Files Changed

### 1. `app/account/views.py`

#### Added to `PurchaseCreditsView`:
```python
metadata={
    'user_email': request.user.email,
}
```
Added metadata to track which user made the purchase.

#### New Class: `StripeWebhookView`
- Receives webhook events from Stripe
- Verifies webhook signature (production security)
- Listens for `checkout.session.completed` event
- Processes successful payments

#### New Method: `handle_successful_payment(session)`
- Gets user by email from checkout session
- Gets credit pack by `stripe_price_id`
- Calls `account.fill_credits(credits)` - adds credits + marks as non-trial
- Creates `CreditPurchase` record for audit trail

**Lines added:** ~80 lines

### 2. `app/account/urls.py`

Added webhook endpoint:
```python
path("stripe-webhook/", views.StripeWebhookView.as_view(), name="stripe_webhook"),
```

**Lines added:** 1 line

### 3. `app/app/settings/development.py`

Added:
```python
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')  # Optional in dev
```

**Lines added:** 1 line

### 4. `app/app/settings/production.py`

Added:
```python
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')  # Required in production
```

**Lines added:** 1 line

### 5. Documentation (New Files)

- `guides/STRIPE_CREDITS_WEBHOOK_SETUP.md` - Complete setup guide
- `guides/STRIPE_CREDITS_QUICK_TEST.md` - Quick testing guide
- `guides/STRIPE_CREDITS_CHANGES.md` - This file

## How It Works

### Flow Diagram

```
User                  Frontend              Backend               Stripe
 |                       |                     |                     |
 | Click "Purchase"      |                     |                     |
 |---------------------->|                     |                     |
 |                       | POST /purchase-     |                     |
 |                       | credits/            |                     |
 |                       |-------------------->|                     |
 |                       |                     | Create Checkout     |
 |                       |                     | Session             |
 |                       |                     |-------------------->|
 |                       |                     |<--------------------|
 |                       |<--------------------|                     |
 |                       |  {checkout_url}     |                     |
 | Open Stripe Checkout  |                     |                     |
 |------------------------------------------------------>|            |
 |                       |                     |                     |
 | Enter Card Details    |                     |                     |
 | Complete Payment      |                     |                     |
 |------------------------------------------------------>|            |
 |                       |                     |                     |
 |                       |                     |    Webhook Event    |
 |                       |                     |<--------------------|
 |                       |                     | POST /stripe-       |
 |                       |                     | webhook/            |
 |                       |                     |                     |
 |                       |                     | ✓ Verify signature  |
 |                       |                     | ✓ Get user by email |
 |                       |                     | ✓ Find credit pack  |
 |                       |                     | ✓ Add credits       |
 |                       |                     | ✓ Create purchase   |
 |                       |                     |                     |
 |                       |                     |-------------------->|
 |                       |                     |   200 OK            |
```

### Models Used

**Account** (already existed):
- `fill_credits(credits: int)` - Adds credits and marks user as non-trial
  - Sets `credit_balance += credits`
  - Sets `is_trial_user = False`

**CreditPack** (already existed):
- Stores credit pack information
- `stripe_price_id` links to Stripe price

**CreditPurchase** (already existed):
- Records each purchase for audit trail
- Links to `Account` and `CreditPack`
- Stores `quantity` and `price`

## Environment Variables

Add to your `.env` file:

```bash
# Required (get from Stripe Dashboard)
STRIPE_SECRET_KEY=sk_test_xxxxx  # or sk_live_xxxxx for production
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxx  # or pk_live_xxxxx

# Required for production, optional for dev
STRIPE_WEBHOOK_SECRET=whsec_xxxxx
```

## Testing

### Development (using Stripe CLI)
```bash
# Install and login
brew install stripe/stripe-cli/stripe
stripe login

# Forward webhooks
stripe listen --forward-to localhost:8000/account/stripe-webhook/

# Copy webhook secret to .env
STRIPE_WEBHOOK_SECRET=whsec_xxxxx
```

### Test Purchase
1. Go to `http://localhost:3000/dashboard/credits`
2. Click "Purchase"
3. Use test card: `4242 4242 4242 4242`
4. Complete payment
5. Check logs for: "Successfully added XXX credits to user@email.com"

## Production Setup

1. Create webhook in Stripe Dashboard:
   - URL: `https://yourdomain.com/account/stripe-webhook/`
   - Event: `checkout.session.completed`

2. Copy signing secret to production environment

3. Deploy

4. Test with test mode first, then small live purchase

## Security

- **Development:** Signature verification optional (logs warning)
- **Production:** Signature verification REQUIRED
  - Prevents fake webhook attacks
  - Verifies events come from Stripe
  - Uses `STRIPE_WEBHOOK_SECRET`

## What Happens on Successful Payment

1. User completes payment on Stripe
2. Stripe sends `checkout.session.completed` event
3. Webhook receives and verifies signature
4. Gets user email from session
5. Gets price_id from line items
6. Finds matching `CreditPack` by `stripe_price_id`
7. Calls `account.fill_credits(pack.credits)`:
   - Adds credits to balance
   - Sets `is_trial_user = False`
8. Creates `CreditPurchase` record:
   - Links to account and pack
   - Stores quantity and price
   - Records timestamp
9. Logs success message

## Error Handling

All errors are logged but don't fail the webhook (returns 200):
- User not found → Log error
- Credit pack not found → Log error
- No line items → Log error
- Any exception → Log error

This prevents Stripe from retrying valid events that have data issues.

## Total Code Added

- **~83 lines** of production code
- **~300 lines** of documentation
- **Minimal changes** to existing codebase
- **No database migrations needed** (models already existed)
- **No frontend changes needed**

## Dependencies

All dependencies already installed:
- `stripe==10.7.0` (already in requirements.txt)
- Django, DRF (already configured)

No new packages needed!

