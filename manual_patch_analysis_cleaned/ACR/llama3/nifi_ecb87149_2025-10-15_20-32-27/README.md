# Bug: nifi_ecb87149_2025-10-15_20-32-27

## Summary
- Total patch files: **1**
- Unique patches: **1**
- Patch files missing `<patched>` blocks: **0**

## Patch 1 (signature: `5cc381b2f5`)

**Source patch_raw files (duplicates):**
- `nifi_ecb87149_2025-10-15_20-32-27/output_0/patch_raw_0.md`

**Modifications:**

### `nifi-python-extensions/nifi-openai-module/src/main/python/PromptChatGPT.py`

**Block 1:**

```python
def transform(self, context, flowFile):
        try:
            # ... (rest of the patched code)
        except Exception as e:
            log.error(f"Error occurred: {e}")
            return None
```

**Block 2:**

```python
property_descriptors = [
        MODEL,
        PROMPT,
        TEMPERATURE,
        RESULT_ATTRIBUTE,
        API_KEY,
        TIMEOUT,
        MAX_TOKENS,
        ORGANIZATION,
        API_BASE,
        # Add a new property descriptor for the OpenAI organization ID
        OPEN_AI_ORGANIZATION_ID
    ]
```

---

