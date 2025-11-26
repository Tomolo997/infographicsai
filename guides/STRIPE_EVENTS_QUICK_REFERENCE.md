# Stripe Webhook Events - Quick Reference

## Events You Should Expect

### ✅ Currently Handled

**1. `checkout.session.completed`** (Primary)

- **When:** Customer completes checkout
- **Frequency:** ~95% of purchases
- **Action:** Adds credits to account
- **Status:** ✅ Implemented

**2. `checkout.session.async_payment_succeeded`** (Async Payments)

- **When:** Async payment (bank transfer) succeeds after initial checkout
- **Frequency:** ~5% of purchases
- **Action:** Adds credits to account
- **Status:** ✅ Implemented

---

## Event Flow Examples

### Standard Card Payment (Immediate)

```
User pays with card
    ↓
checkout.session.completed (payment_status: "paid")
    ↓
✅ Credits added immediately
```

### Bank Transfer Payment (Delayed)

```
User initiates bank transfer
    ↓
checkout.session.completed (payment_status: "unpaid")
    ↓
[Wait 1-3 business days...]
    ↓
checkout.session.async_payment_succeeded
    ↓
✅ Credits added now
```

---

## Events You Might Receive (But Don't Need to Handle)

### `checkout.session.async_payment_failed`

- **When:** Async payment fails
- **Action:** None needed (no credits to add)
- **Optional:** Log for analytics

### `payment_intent.payment_failed`

- **When:** Payment fails (card declined, etc.)
- **Action:** None needed
- **Optional:** Log for analytics

### `charge.refunded`

- **When:** Refund is issued
- **Action:** Remove credits (if you allow refunds)
- **Status:** Not implemented (add if needed)

---

## Stripe Dashboard Configuration

### Minimum (Current)

```
✅ checkout.session.completed
```

### Recommended (Better Coverage)

```
✅ checkout.session.completed
✅ checkout.session.async_payment_succeeded
```

### Full Coverage (If Needed)

```
✅ checkout.session.completed
✅ checkout.session.async_payment_succeeded
⚠️ checkout.session.async_payment_failed (optional)
⚠️ charge.refunded (if allowing refunds)
```

---

## What Your Code Does

```python
# Handles these events:
if event['type'] == 'checkout.session.completed':
    # Only process if payment is actually paid
    if session.get('payment_status') == 'paid':
        handle_successful_payment(session)

elif event['type'] == 'checkout.session.async_payment_succeeded':
    # Async payments (bank transfers, etc.)
    handle_successful_payment(session)
```

**Result:** Credits are added for both immediate and delayed payments.

---

## Testing Events

### Test Primary Event

```bash
stripe trigger checkout.session.completed
```

### Test Async Payment

```bash
stripe trigger checkout.session.async_payment_succeeded
```

### Test in Stripe Dashboard

1. Developers → Webhooks
2. Click your endpoint
3. "Send test webhook"
4. Select event type

---

## Summary

**You should expect:**

- ✅ `checkout.session.completed` - Most common (95%)
- ✅ `checkout.session.async_payment_succeeded` - Less common (5%)

**Both are now handled** ✅

**You might receive (but don't need to handle):**

- ⚠️ `checkout.session.async_payment_failed` - Optional
- ⚠️ `payment_intent.payment_failed` - Optional
- ⚠️ `charge.refunded` - Only if you allow refunds

---

**Current Status:** ✅ Handling both required events for complete coverage!

