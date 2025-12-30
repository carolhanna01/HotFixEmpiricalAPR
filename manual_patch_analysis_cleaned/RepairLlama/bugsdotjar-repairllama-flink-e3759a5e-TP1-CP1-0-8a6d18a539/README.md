# Bug: bugsdotjar-repairllama-flink-e3759a5e-TP1-CP1-0-8a6d18a539

## Summary
- Total patch files: **5**
- Unique patches: **4**
- Invalid/unparseable patch files: **1**

## Invalid / unparseable patch files
- `bugsdotjar-repairllama-flink-e3759a5e-TP1-CP1-0-8a6d18a539/output/patches/3.patch` — empty diff

---

## Patch 1 (signature: `3954ea3698`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-e3759a5e-TP1-CP1-0-8a6d18a539/output/patches/2.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/cep/operator/AbstractCEPPatternOperator.java`

```diff
--- org/apache/flink/cep/operator/AbstractCEPPatternOperator.java
+++ org/apache/flink/cep/operator/AbstractCEPPatternOperator.java
@@ -50,7 +50,7 @@
 			final TypeSerializer<IN> inputSerializer,
 			final boolean isProcessingTime) {
 		this.inputSerializer = inputSerializer;
-		this.isProcessingTime = isProcessingTime;
+		this.isProcessingTime = true;
 	}

 	public TypeSerializer<IN> getInputSerializer() {
```

---

## Patch 2 (signature: `6892a0bdba`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-e3759a5e-TP1-CP1-0-8a6d18a539/output/patches/0.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/cep/operator/AbstractCEPPatternOperator.java`

```diff
--- org/apache/flink/cep/operator/AbstractCEPPatternOperator.java
+++ org/apache/flink/cep/operator/AbstractCEPPatternOperator.java
@@ -48,7 +48,7 @@

 	public AbstractCEPPatternOperator(
 			final TypeSerializer<IN> inputSerializer,
-			final boolean isProcessingTime) {
+		final boolean isProcessingTime) {
 		this.inputSerializer = inputSerializer;
 		this.isProcessingTime = isProcessingTime;
 	}
```

---

## Patch 3 (signature: `94cf924c72`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-e3759a5e-TP1-CP1-0-8a6d18a539/output/patches/4.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/cep/operator/CEPPatternOperator.java`

```diff
--- org/apache/flink/cep/operator/CEPPatternOperator.java
+++ org/apache/flink/cep/operator/CEPPatternOperator.java
@@ -82,7 +82,7 @@

 	@Override
 	public void processWatermark(Watermark mark) throws Exception {
-		while(!priorityQueue.isEmpty() && priorityQueue.peek().getTimestamp() <= mark.getTimestamp()) {
+		while(!priorityQueue.isEmpty() && priorityQueue.peek().getTimestamp() < mark.getTimestamp()) {
 			StreamRecord<IN> streamRecord = priorityQueue.poll();

 			processEvent(nfa, streamRecord.getValue(), streamRecord.getTimestamp());
```

---

## Patch 4 (signature: `e5bed089c6`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-e3759a5e-TP1-CP1-0-8a6d18a539/output/patches/1.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/cep/operator/AbstractCEPPatternOperator.java`

```diff
--- org/apache/flink/cep/operator/AbstractCEPPatternOperator.java
+++ org/apache/flink/cep/operator/AbstractCEPPatternOperator.java
@@ -49,7 +49,7 @@
 	public AbstractCEPPatternOperator(
 			final TypeSerializer<IN> inputSerializer,
 			final boolean isProcessingTime) {
-		this.inputSerializer = inputSerializer;
+		this.inputSerializer = inputSerializer.duplicate();
 		this.isProcessingTime = isProcessingTime;
 	}
```

---

