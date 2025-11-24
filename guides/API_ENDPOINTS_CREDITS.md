# Credits API Endpoints Reference

## Endpoint Overview

| Endpoint                     | Method | Auth             | Purpose                        |
| ---------------------------- | ------ | ---------------- | ------------------------------ |
| `/account/credit-packs/`     | GET    | ✅ Required      | List available credit packs    |
| `/account/purchase-credits/` | POST   | ✅ Required      | Create Stripe checkout session |
| `/account/stripe-webhook/`   | POST   | ❌ None (Stripe) | Process payment completion     |

---

## 1. List Credit Packs

### `GET /account/credit-packs/`

**Purpose:** Get all available credit packs with pricing and Stripe IDs

**Authentication:** Required (Token)

**Request:**

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/account/credit-packs/
```

**Response:**

```json
[
  {
    "id": 1,
    "name": "Starter Pack",
    "description": "Perfect for trying out the platform",
    "credits": 100,
    "price": 10,
    "price_per_credit": "0.10",
    "stripe_price_id": "price_1ABCdef123456789",
    "stripe_product_id": "prod_ABCdef123456"
  },
  {
    "id": 2,
    "name": "Pro Pack",
    "description": "Best value for regular users",
    "credits": 500,
    "price": 40,
    "price_per_credit": "0.08",
    "stripe_price_id": "price_2XYZabc987654321",
    "stripe_product_id": "prod_XYZabc987654"
  }
]
```

**Used By:** Frontend credits page on load

---

## 2. Purchase Credits

### `POST /account/purchase-credits/`

**Purpose:** Create a Stripe checkout session for purchasing credits

**Authentication:** Required (Token)

**Request:**

```bash
curl -X POST \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"price_id": "price_1ABCdef123456789"}' \
  http://localhost:8000/account/purchase-credits/
```

**Request Body:**

```json
{
  "price_id": "price_1ABCdef123456789"
}
```

**Response (Success):**

```json
{
  "checkout_url": "https://checkout.stripe.com/c/pay/cs_test_a1b2c3..."
}
```

**Response (Error):**

```json
{
  "message": "price_id is required"
}
```

**Status Codes:**

- `200 OK` - Checkout session created
- `400 Bad Request` - Missing price_id or Stripe error
- `401 Unauthorized` - No auth token

**Frontend Usage:**

```javascript
const response = await apiClient.post('/account/purchase-credits/', {
  price_id: pack.stripe_price_id,
})
window.open(response.data.checkout_url, '_blank')
```

**What It Does:**

1. Validates user is authenticated
2. Gets price_id from request
3. Creates Stripe checkout session with:
   - Payment method: card
   - Line item: selected price
   - Success URL: `/dashboard/credits?success=true`
   - Cancel URL: `/dashboard/credits?canceled=true`
   - Customer email: logged in user's email
   - Metadata: user email (for webhook)
4. Returns checkout URL to frontend

---

## 3. Stripe Webhook

### `POST /account/stripe-webhook/`

**Purpose:** Receive payment events from Stripe and add credits

**Authentication:** None (verified by Stripe signature)

**⚠️ This endpoint is called by Stripe, not your frontend**

**Request Headers:**

```
Content-Type: application/json
Stripe-Signature: t=timestamp,v1=signature...
```

**Request Body (Example):**

```json
{
  "id": "evt_1ABCdef123456789",
  "type": "checkout.session.completed",
  "data": {
    "object": {
      "id": "cs_test_a1b2c3d4e5f6g7h8",
      "customer_email": "user@example.com",
      "payment_status": "paid",
      "amount_total": 1000,
      "currency": "usd"
    }
  }
}
```

**Response:**

```json
{
  "status": "success"
}
```

**Status Codes:**

- `200 OK` - Event processed (even if errors occurred)
- `400 Bad Request` - Invalid signature or payload

**What It Does:**

1. **Receives webhook event from Stripe**
   - Extracts payload and signature
2. **Verifies signature (production)**

   - Uses `STRIPE_WEBHOOK_SECRET`
   - Prevents fake payment notifications
   - Skipped in dev if secret not configured

3. **Checks event type**

   - Only processes `checkout.session.completed`
   - Ignores other event types

4. **Extracts user email**

   - From `customer_email` or `customer_details.email`

5. **Finds user and account**

   - Gets `CustomUser` by email
   - Gets linked `Account`

6. **Gets price_id from line items**

   - Calls Stripe API to get line items
   - Extracts price_id from first item

7. **Finds credit pack**

   - Gets `CreditPack` by `stripe_price_id`

8. **Adds credits**

   - Calls `account.fill_credits(credits)`
   - Updates `credit_balance`
   - Sets `is_trial_user = False`

9. **Creates purchase record**

   - New `CreditPurchase` entry
   - Links account and credit pack
   - Stores quantity, price, timestamp

10. **Logs result**
    - Success: "Successfully added XXX credits to user@email.com"
    - Error: Detailed error message

**Security:**

- ✅ Signature verification in production
- ✅ CSRF exempt (uses Stripe signature)
- ✅ No authentication required (Stripe is authenticated)

**Error Handling:**

- Returns 200 even if processing fails (prevents Stripe retries)
- All errors logged for debugging
- Invalid signature returns 400

---

## Complete User Flow

### Step-by-Step

```
1. Frontend calls GET /account/credit-packs/
   ↓
   Displays available packs with "Purchase" buttons

2. User clicks "Purchase" button
   ↓
   Frontend calls POST /account/purchase-credits/
   Body: { price_id: "price_xxx" }
   ↓
   Backend creates Stripe checkout session
   ↓
   Returns { checkout_url: "https://..." }

3. Frontend opens checkout_url in new tab
   ↓
   User enters card details
   ↓
   Completes payment

4. Stripe processes payment
   ↓
   Payment successful
   ↓
   Stripe calls POST /account/stripe-webhook/
   (In background, user doesn't see this)
   ↓
   Webhook adds credits to account
   ↓
   User is redirected to success page

5. Frontend shows success message
   ↓
   User refreshes to see new credit balance
```

### Timing

- **Step 1-3:** Immediate (< 1 second)
- **Step 4:** 2-10 seconds (payment processing)
- **Webhook:** Usually < 1 second after payment
- **Total:** ~3-15 seconds from click to credits added

---

## Testing the Endpoints

### 1. Test List Credit Packs

```bash
# Get your auth token first
TOKEN=$(curl -X POST http://localhost:8000/account/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user@example.com","password":"password"}' \
  | jq -r '.token')

# List packs
curl -H "Authorization: Token $TOKEN" \
  http://localhost:8000/account/credit-packs/
```

### 2. Test Purchase Credits

```bash
# Create checkout session
curl -X POST \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"price_id": "price_1ABCdef123456789"}' \
  http://localhost:8000/account/purchase-credits/

# Open the checkout_url in a browser
```

### 3. Test Webhook (Development)

```bash
# First, start webhook forwarding
stripe listen --forward-to localhost:8000/account/stripe-webhook/

# Then complete a test purchase or trigger event
stripe trigger checkout.session.completed
```

---

## Frontend Integration

### Vue/Nuxt Example (Already Implemented)

```vue
<script setup>
import apiClient from '~/client/apiClient'

const creditPacks = ref([])
const isLoading = ref(false)

// Fetch available packs
const fetchCreditPacks = async () => {
  const response = await apiClient.get('/account/credit-packs/')
  creditPacks.value = response.data
}

// Handle purchase
const handlePurchase = async (pack) => {
  try {
    isLoading.value = true

    const response = await apiClient.post('/account/purchase-credits/', {
      price_id: pack.stripe_price_id,
    })

    // Open Stripe checkout
    window.open(response.data.checkout_url, '_blank')
  } catch (error) {
    console.error('Error:', error)
    alert('Failed to initiate purchase')
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchCreditPacks()
})
</script>
```

---

## Monitoring & Debugging

### Check Webhook Deliveries

Stripe Dashboard → Developers → Webhooks → Your endpoint → Recent deliveries

### Check Logs

```bash
# Django logs
tail -f /path/to/django.log | grep -i stripe

# Look for:
# ✅ "Successfully added XXX credits to user@email.com"
# ❌ "User not found: email@example.com"
# ❌ "Credit pack not found for price_id: price_xxx"
```

### Verify Credits Added

```python
python manage.py shell

from account.models import Account, CreditPurchase
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(email='user@example.com')
account = user.account

print(f"Balance: {account.credit_balance}")
print(f"Trial: {account.is_trial_user}")

# Recent purchases
purchases = CreditPurchase.objects.filter(account=account).order_by('-created_at')[:5]
for p in purchases:
    print(f"{p.created_at}: {p.credit_pack.name} - {p.quantity} credits - ${p.price}")
```

---

## Common Issues

### "price_id is required"

- Missing `price_id` in request body
- Check frontend is sending correct field

### "Failed to create checkout session"

- Invalid `price_id` (doesn't exist in Stripe)
- Stripe API key not set or invalid
- Network issue connecting to Stripe

### Webhook not called

- Stripe CLI not running (dev)
- Webhook not configured in Stripe Dashboard (prod)
- URL not accessible from internet (prod)

### Credits not added

- Check webhook logs for errors
- User email mismatch
- Credit pack missing `stripe_price_id`
- Price ID not matching any pack

---

## Security Checklist

### Development

- ✅ Use test mode keys (`sk_test_`, `pk_test_`)
- ✅ Stripe CLI for webhook forwarding
- ✅ `STRIPE_WEBHOOK_SECRET` optional (logs warning)

### Production

- ✅ Use live mode keys (`sk_live_`, `pk_live_`)
- ✅ HTTPS required for webhook endpoint
- ✅ `STRIPE_WEBHOOK_SECRET` REQUIRED
- ✅ Webhook signature verification enabled
- ✅ Monitor webhook deliveries regularly
- ✅ Set up alerts for failed webhooks

---

**Ready to test!** See `guides/STRIPE_CREDITS_QUICK_TEST.md` for step-by-step testing guide.
