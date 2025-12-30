# Bug: bugsdotjar-repairllama-hadoop-49b4c0b3-TP1-CP1-2-f27f5394bd

## Summary
- Total patch files: **1**
- Unique patches: **1**
- Invalid/unparseable patch files: **0**

## Patch 1 (signature: `549ecf144b`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-hadoop-49b4c0b3-TP1-CP1-2-f27f5394bd/output/patches/0.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/hadoop/resourceestimator/translator/impl/LogParserUtil.java`

```diff
--- org/apache/hadoop/resourceestimator/translator/impl/LogParserUtil.java
+++ org/apache/hadoop/resourceestimator/translator/impl/LogParserUtil.java
@@ -93,7 +93,7 @@
     }
     InputStream inputStream = null;
     try {
-      inputStream = new FileInputStream(logFile);
+     inputStream = new FileInputStream(new File(logFile));
       logParser.parseStream(inputStream);
     } finally {
       if (inputStream != null) {
```

---

