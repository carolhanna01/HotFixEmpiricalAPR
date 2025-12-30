# Bug: bugsdotjar-repairllama-flink-42d8dde0-TP1-CP1-2-b222cced3e

## Summary
- Total patch files: **5**
- Unique patches: **3**
- Invalid/unparseable patch files: **2**

## Invalid / unparseable patch files
- `bugsdotjar-repairllama-flink-42d8dde0-TP1-CP1-2-b222cced3e/output/patches/0.patch` — empty diff
- `bugsdotjar-repairllama-flink-42d8dde0-TP1-CP1-2-b222cced3e/output/patches/4.patch` — empty diff

---

## Patch 1 (signature: `0e4c5f3cac`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-42d8dde0-TP1-CP1-2-b222cced3e/output/patches/1.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/table/filesystem/stream/StreamingFileWriter.java`

```diff
--- org/apache/flink/table/filesystem/stream/StreamingFileWriter.java
+++ org/apache/flink/table/filesystem/stream/StreamingFileWriter.java
@@ -70,7 +70,7 @@
 			long bucketCheckInterval,
 			StreamingFileSink.BucketsBuilder<RowData, String, ? extends
 					StreamingFileSink.BucketsBuilder<RowData, String, ?>> bucketsBuilder) {
-		this.bucketCheckInterval = bucketCheckInterval;
+		this.bucketCheckInterval = Math.max(1, bucketCheckInterval);
 		this.bucketsBuilder = bucketsBuilder;
 		setChainingStrategy(ChainingStrategy.ALWAYS);
 	}
```

---

## Patch 2 (signature: `655777536b`) CH:SYMPTOM-HIDER

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-42d8dde0-TP1-CP1-2-b222cced3e/output/patches/3.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/table/filesystem/stream/StreamingFileWriter.java`

```diff
--- org/apache/flink/table/filesystem/stream/StreamingFileWriter.java
+++ org/apache/flink/table/filesystem/stream/StreamingFileWriter.java
@@ -72,7 +72,7 @@
 					StreamingFileSink.BucketsBuilder<RowData, String, ?>> bucketsBuilder) {
 		this.bucketCheckInterval = bucketCheckInterval;
 		this.bucketsBuilder = bucketsBuilder;
-		setChainingStrategy(ChainingStrategy.ALWAYS);
+		setChainingStrategy(ChainingStrategy.NEVER);
 	}

 	@Override
```

---

## Patch 3 (signature: `85e776b879`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-42d8dde0-TP1-CP1-2-b222cced3e/output/patches/2.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/table/filesystem/stream/StreamingFileWriter.java`

```diff
--- org/apache/flink/table/filesystem/stream/StreamingFileWriter.java
+++ org/apache/flink/table/filesystem/stream/StreamingFileWriter.java
@@ -71,7 +71,7 @@
 			StreamingFileSink.BucketsBuilder<RowData, String, ? extends
 					StreamingFileSink.BucketsBuilder<RowData, String, ?>> bucketsBuilder) {
 		this.bucketCheckInterval = bucketCheckInterval;
-		this.bucketsBuilder = bucketsBuilder;
+		this.bucketsBuilder = bucketsBuilder.build();
 		setChainingStrategy(ChainingStrategy.ALWAYS);
 	}
```

---

