# Debugging Dashboard Generation Issue

## Issue

After clicking "Generate", the API returns 201 but nothing is displayed.

## Debugging Added

I've added comprehensive logging to help identify the issue:

### 1. Console Logging

Open your browser console (F12) and look for these logs after clicking "Generate":

```
handleGenerate
API Response: {infographs: [...], total_submitted: 1, credits_used: 1}
Processing infographs: [{id: 123, request_id: "...", status: "processing"}]
Results initialized: [{id: 123, status: "processing", ...}]
hasResults before: false
isGenerating before: true
hasResults after: true
isGenerating after: false
Starting polling for infograph: 123
```

### 2. On-Page Debug Info

You should see this line appear above the results:

```
DEBUG: hasResults=true, isGenerating=false, results.length=1
```

### 3. Empty Results Warning

If the results array is empty, you'll see:

```
⚠️ Results array is empty! Check console for API response.
```

---

## What to Check

### Step 1: Check API Response Structure

In the console, look for `API Response:`. It should look like:

```javascript
{
  infographs: [
    {
      id: 123,
      request_id: "fal-abc-123",
      status: "processing",
      status_url: "..."
    }
  ],
  total_submitted: 1,
  credits_used: 1
}
```

**If it's different**, the response structure doesn't match what the frontend expects.

### Step 2: Check State Variables

Look for these logs:

- `hasResults after: true` - Should be TRUE
- `isGenerating after: false` - Should be FALSE
- `Results initialized: [...]` - Should have array with items

### Step 3: Check if Polling Starts

Look for:

```
Starting polling for infograph: 123
```

If you don't see this, polling isn't starting.

---

## Common Issues & Solutions

### Issue 1: API Returns Different Structure

**Symptom:** Console shows `Fallback: Using response.data directly`

**Cause:** API response doesn't have `response.data.infographs` array

**Solution:** Check backend response format in `app/infographs/views.py`

**Expected backend response:**

```python
return Response({
    "infographs": [
        {
            "id": infograph.id,
            "request_id": infograph.fal_request_id,
            "status": infograph.status,
        }
    ],
    "total_submitted": len(infographs),
    "credits_used": total_credits_needed,
}, status=status.HTTP_201_CREATED)
```

### Issue 2: Results Array is Empty

**Symptom:** `results.length=0` in debug info

**Cause:** API response doesn't contain infographs, or mapping failed

**Solution:** Check console for `API Response:` - if infographs array is empty, backend issue

### Issue 3: hasResults Still False

**Symptom:** No results grid appears, `hasResults=false` in debug

**Cause:**

- API call failed (check console for errors)
- Response doesn't match expected structure
- Error was caught and hasResults wasn't set

**Solution:** Check for error messages in console

### Issue 4: isGenerating Still True

**Symptom:** Only see "Submitting..." skeleton, `isGenerating=true`

**Cause:** API call is hanging or errored before setting isGenerating=false

**Solution:**

- Check network tab for API call status
- Check for CORS errors
- Verify backend is running

---

## Step-by-Step Debugging Process

### 1. Open Browser DevTools

- Press F12
- Go to "Console" tab

### 2. Click "Generate"

### 3. Check Console Logs

Look for this sequence:

```
1. "handleGenerate"
2. "API Response: {...}"
3. "Processing infographs: [...]"
4. "Results initialized: [...]"
5. "hasResults after: true"
6. "isGenerating after: false"
7. "Starting polling for infograph: ..."
```

### 4. Check Network Tab

- Go to "Network" tab in DevTools
- Find the POST request to `/api/infographs/create/`
- Check:
  - **Status**: Should be `201 Created`
  - **Response**: Should have infographs array
  - **Time**: Should complete quickly (< 1s)

### 5. Check On-Page Debug

Look for:

```
DEBUG: hasResults=true, isGenerating=false, results.length=1
```

---

## Quick Diagnostic Commands

Open browser console and run these:

```javascript
// Check current state
console.log('hasResults:', hasResults.value)
console.log('isGenerating:', isGenerating.value)
console.log('results:', results.value)
console.log('results length:', results.value.length)

// Check polling intervals
console.log('Active polling:', pollingIntervals.value)
```

---

## Expected vs Actual

### ✅ Expected Behavior

1. Click "Generate"
2. See "Submitting..." for < 1 second
3. See result card(s) with "Live ●" indicator
4. See spinner + "Generating your infographic..."
5. After 30-60 seconds, see image with "✓ Ready" badge

### ❌ If Nothing Shows

**Possible causes:**

1. API response structure mismatch
2. Frontend state not updating (hasResults/isGenerating)
3. Results array is empty
4. Vue reactivity issue
5. Template rendering condition failing

---

## Backend Verification

Check the backend is returning correct structure:

### In `app/infographs/api/service.py` or `app/infographs/infographs/service.py`

Look for the return statement in `create_infograph`:

```python
return {
    "infographs": infographs,  # Must be an array
    "total_submitted": len(infographs),
    "credits_used": total_credits_needed,
}
```

### In `app/infographs/views.py`

Look for `InfographCreateAPIView`:

```python
result = infographs_api_service.create_infograph(**data)
return Response(result, status=status.HTTP_201_CREATED)
```

---

## Next Steps

1. **Run the app and click Generate**
2. **Check the console logs** - Screenshot them if needed
3. **Check the debug info** on the page
4. **Look for error messages**
5. **Check Network tab** for API response

Share the console output and we can identify the exact issue!

---

## Remove Debug Code Later

Once the issue is fixed, remove:

1. All `console.log()` statements in `handleGenerate`
2. The debug info line: `DEBUG: hasResults=...`
3. The empty results warning message

Or I can remove them for you once we fix the issue.
