# Bug: hadoop_31ebccc9_2025-11-05_19-19-49

## Summary
- Total patch files: **6**
- Unique patches: **3**
- Patch files missing `<patched>` blocks: **3**

## Patch files with no `<patched>` blocks
- `hadoop_31ebccc9_2025-11-05_19-19-49/output_1/patch_raw_0.md`
- `hadoop_31ebccc9_2025-11-05_19-19-49/output_1/patch_raw_1.md`
- `hadoop_31ebccc9_2025-11-05_19-19-49/output_1/patch_raw_2.md`

---

## Patch 1 (signature: `07a8477082`)

**Source patch_raw files (duplicates):**
- `hadoop_31ebccc9_2025-11-05_19-19-49/output_0/patch_raw_2.md`

**Modifications:**

### `dev-support/determine-flaky-tests-hadoop.py`

**Block 1:**

```python
70 numRunsToExamine = 0
...
157 def find_flaky_tests(jenkins_url, job_name, num_prev_days):
158     numRunsToExamine = len(list_builds(jenkins_url, job_name))
...
```

**Block 2:**

```python
125     logging.error("Could not fetch: %s" % url)
126     error_count += 1
...
```

**Block 3:**

```python
142     logging.error("    Could not open testReport, check " +
143         jobConsoleOutput + " for why it was reported failed")
144     error_count += 1
...
```

---

## Patch 2 (signature: `522bbdd81b`)

**Source patch_raw files (duplicates):**
- `hadoop_31ebccc9_2025-11-05_19-19-49/output_0/patch_raw_0.md`

**Modifications:**

### `dev-support/determine-flaky-tests-hadoop.py`

**Block 1:**

```python
70 numRunsToExamine = 0
...
157 def find_flaky_tests(jenkins_url, job_name, num_prev_days):
158     numRunsToExamine = len(list_builds(jenkins_url, job_name))
...
```

**Block 2:**

```python
76 error_count = 0
...
125     logging.error("Could not fetch: %s" % url)
126     error_count += 1
...
```

**Block 3:**

```python
138     if not summary_mode:
139       logging.error("    Could not open testReport, check " +
140         jobConsoleOutput + " for why it was reported failed")
141     error_count += 1
142     raise
...
```

---

## Patch 3 (signature: `b771c53c51`)

**Source patch_raw files (duplicates):**
- `hadoop_31ebccc9_2025-11-05_19-19-49/output_0/patch_raw_1.md`

**Modifications:**

### `dev-support/determine-flaky-tests-hadoop.py`

**Block 1:**

```python
70 numRunsToExamine = 0
...
157 def find_flaky_tests(jenkins_url, job_name, num_prev_days):
158     numRunsToExamine = len(list_builds(jenkins_url, job_name))
...
```

**Block 2:**

```python
76 error_count = 0
...
125     logging.error("Could not fetch: %s" % url)
    error_count += 1
...
```

**Block 3:**

```python
141     if not summary_mode:
142       logging.error("    Could not open testReport, check " +
143         jobConsoleOutput + " for why it was reported failed")
    error_count += 1
...
```

---

