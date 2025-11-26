# Stripe Webhook Events Guide

## Currently Handled Events

### ✅ `checkout.session.completed` (Required)

**When it fires:**

- After a customer successfully completes a checkout session
- Payment has been processed and confirmed
- This is the **primary event** for adding credits

**What happens:**

- Credits are added to user account
- `CreditPurchase` record is created
- User marked as non-trial

**Event structure:**

```json
{
  "id": "evt_1ABCdef123456789",
  "type": "checkout.session.completed",
  "data": {
    "object": {
      "id": "cs_test_xxx",
      "customer_email": "user@example.com",
      "payment_status": "paid",
      "amount_total": 1000,
      "currency": "usd",
      "metadata": {
        "user_email": "user@example.com"
      }
    }
  }
}
```

**Status in code:** ✅ Implemented

---

## Other Events You Might Receive

### ⚠️ `checkout.session.async_payment_succeeded` (Optional but Recommended)

**When it fires:**

- For asynchronous payment methods (bank transfers, SEPA, etc.)
- Payment was initially pending, now succeeded
- **Important:** This can fire AFTER `checkout.session.completed`

**Why handle it:**

- Some payment methods (bank transfers) take time to process
- Initial `checkout.session.completed` might have `payment_status: "unpaid"`
- This event confirms payment actually succeeded

**Recommendation:** Add handler to avoid missing credits for async payments

**Event structure:**

```json
{
  "type": "checkout.session.async_payment_succeeded",
  "data": {
    "object": {
      "id": "cs_test_xxx",
      "customer_email": "user@example.com",
      "payment_status": "paid"
    }
  }
}
```

---

### ⚠️ `checkout.session.async_payment_failed` (Optional)

**When it fires:**

- Async payment method failed after initial checkout
- Customer needs to retry payment

**Why handle it:**

- Track failed payments
- Send notification to user
- Log for analytics

**Recommendation:** Optional - mainly for logging/notifications

---

### ⚠️ `payment_intent.succeeded` (Alternative - Not Recommended)

**When it fires:**

- Payment intent succeeded
- More granular than checkout.session.completed

**Why NOT use it:**

- Checkout sessions are higher-level and easier to work with
- `checkout.session.completed` is sufficient for one-time payments
- Payment intents are more complex (subscriptions, partial payments, etc.)

**Recommendation:** Stick with `checkout.session.completed`

---

### ⚠️ `payment_intent.payment_failed` (Optional)

**When it fires:**

- Payment failed (card declined, insufficient funds, etc.)

**Why handle it:**

- Track failed payment attempts
- Send user notification
- Analytics

**Recommendation:** Optional - for better UX/analytics

---

### ⚠️ `charge.refunded` (Important for Refunds)

**When it fires:**

- Full or partial refund issued
- Customer gets money back

**Why handle it:**

- **Remove credits** if refunded
- Update `CreditPurchase` record
- Maintain accurate credit balance

**Recommendation:** **Should implement** if you allow refunds

**Event structure:**

```json
{
  "type": "charge.refunded",
  "data": {
    "object": {
      "id": "ch_xxx",
      "amount_refunded": 1000,
      "refunded": true,
      "metadata": {
        "checkout_session_id": "cs_test_xxx"
      }
    }
  }
}
```

---

## Recommended Event Configuration

### Minimum (Current Implementation)

**Stripe Dashboard → Webhooks → Select Events:**

- ✅ `checkout.session.completed`

**Why:** Covers 95% of successful credit purchases

---

### Recommended (Production Ready)

**Stripe Dashboard → Webhooks → Select Events:**

- ✅ `checkout.session.completed` (Primary)
- ✅ `checkout.session.async_payment_succeeded` (Async payments)
- ✅ `charge.refunded` (If you allow refunds)

**Why:**

- Handles all payment methods (card, bank transfer, etc.)
- Handles refunds properly
- Covers edge cases

---

### Comprehensive (Full Coverage)

**Stripe Dashboard → Webhooks → Select Events:**

- ✅ `checkout.session.completed`
- ✅ `checkout.session.async_payment_succeeded`
- ✅ `checkout.session.async_payment_failed`
- ✅ `charge.refunded`
- ✅ `payment_intent.payment_failed`

**Why:**

- Complete payment lifecycle tracking
- Better analytics
- Better user notifications
- Full audit trail

---

## Event Flow Diagram

### Successful Payment (Card - Immediate)

```
User completes checkout
    ↓
checkout.session.completed (payment_status: "paid")
    ↓
✅ Credits added immediately
```

### Successful Payment (Bank Transfer - Delayed)

```
User completes checkout
    ↓
checkout.session.completed (payment_status: "unpaid")
    ↓
[Wait for bank processing...]
    ↓
checkout.session.async_payment_succeeded
    ↓
✅ Credits added now
```

### Failed Payment

```
User attempts checkout
    ↓
Payment fails (card declined, etc.)
    ↓
payment_intent.payment_failed
    ↓
❌ No credits added
(Log for analytics)
```

### Refund

```
Admin issues refund
    ↓
charge.refunded
    ↓
✅ Remove credits from account
```

---

## Implementation Recommendations

### Current Code (Minimal)

```python
# Only handles checkout.session.completed
if event['type'] == 'checkout.session.completed':
    session = event['data']['object']
    self.handle_successful_payment(session)
```

### Recommended Enhancement

```python
# Handle multiple events
if event['type'] == 'checkout.session.completed':
    session = event['data']['object']
    # Only process if payment is actually paid
    if session.get('payment_status') == 'paid':
        self.handle_successful_payment(session)

elif event['type'] == 'checkout.session.async_payment_succeeded':
    session = event['data']['object']
    self.handle_successful_payment(session)

elif event['type'] == 'charge.refunded':
    charge = event['data']['object']
    self.handle_refund(charge)
```

---

## Event Frequency

### Expected Frequency (Normal Operations)

| Event                                      | Frequency         | Notes                |
| ------------------------------------------ | ----------------- | -------------------- |
| `checkout.session.completed`               | ~95% of purchases | Most common          |
| `checkout.session.async_payment_succeeded` | ~5% of purchases  | Bank transfers, etc. |
| `charge.refunded`                          | <1% of purchases  | Rare                 |
| `payment_intent.payment_failed`            | ~2-5% of attempts | Declined cards, etc. |

---

## Testing Events

### Test `checkout.session.completed`

```bash
# Stripe CLI
stripe trigger checkout.session.completed
```

### Test `checkout.session.async_payment_succeeded`

```bash
# Stripe CLI
stripe trigger checkout.session.async_payment_succeeded
```

### Test `charge.refunded`

```bash
# Create a test payment first, then:
stripe trigger charge.refunded
```

### Test in Stripe Dashboard

1. Go to Developers → Webhooks
2. Click on your endpoint
3. Click "Send test webhook"
4. Select event type
5. Send

---

## Event Ordering

### Important: Events Can Arrive Out of Order

**Scenario:**

1. `checkout.session.completed` arrives first (payment_status: "unpaid")
2. `checkout.session.async_payment_succeeded` arrives later

**Solution:**

- Check `payment_status` in `checkout.session.completed`
- Only add credits if `payment_status == "paid"`
- Or handle both events idempotently (check if credits already added)

### Idempotency

**Best Practice:** Make webhook handlers idempotent

```python
def handle_successful_payment(self, session):
    # Check if already processed
    session_id = session['id']
    existing = CreditPurchase.objects.filter(
        stripe_session_id=session_id
    ).first()

    if existing:
        logger.info(f"Payment already processed: {session_id}")
        return

    # Process payment...
```

**Note:** You'd need to add `stripe_session_id` field to `CreditPurchase` model for this.

---

## Production Checklist

### Events to Configure

- [ ] `checkout.session.completed` ✅ (Required)
- [ ] `checkout.session.async_payment_succeeded` (Recommended)
- [ ] `charge.refunded` (If allowing refunds)
- [ ] `payment_intent.payment_failed` (Optional - analytics)

### Code to Add

- [ ] Handle `checkout.session.async_payment_succeeded`
- [ ] Handle `charge.refunded` (remove credits)
- [ ] Add idempotency check (prevent duplicate credits)
- [ ] Add `stripe_session_id` to `CreditPurchase` model (optional)

### Monitoring

- [ ] Monitor webhook deliveries in Stripe Dashboard
- [ ] Set up alerts for failed webhooks
- [ ] Log all events received (even if not handled)
- [ ] Track event frequency

---

## Summary

### Currently Handling

- ✅ `checkout.session.completed` - Primary event for adding credits

### Should Also Handle (Recommended)

- ⚠️ `checkout.session.async_payment_succeeded` - For bank transfers
- ⚠️ `charge.refunded` - If you allow refunds

### Optional (Nice to Have)

- ⚠️ `checkout.session.async_payment_failed` - For notifications
- ⚠️ `payment_intent.payment_failed` - For analytics

### Not Needed

- ❌ `payment_intent.succeeded` - Redundant with checkout.session.completed
- ❌ Most other events - Not relevant for one-time credit purchases

---

## Quick Reference

**Minimum Setup:**

```
checkout.session.completed
```

**Recommended Setup:**

```
checkout.session.completed
checkout.session.async_payment_succeeded
charge.refunded
```

**Full Setup:**

```
checkout.session.completed
checkout.session.async_payment_succeeded
checkout.session.async_payment_failed
charge.refunded
payment_intent.payment_failed
```

---

**Current Status:** ✅ Handling `checkout.session.completed` - sufficient for most cases!

**Next Steps:** Consider adding `checkout.session.async_payment_succeeded` for better coverage.

