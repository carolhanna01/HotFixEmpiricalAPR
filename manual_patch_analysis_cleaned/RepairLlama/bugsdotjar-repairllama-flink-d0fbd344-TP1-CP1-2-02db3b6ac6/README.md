# Bug: bugsdotjar-repairllama-flink-d0fbd344-TP1-CP1-2-02db3b6ac6

## Summary
- Total patch files: **5**
- Unique patches: **4**
- Invalid/unparseable patch files: **1**

## Invalid / unparseable patch files
- `bugsdotjar-repairllama-flink-d0fbd344-TP1-CP1-2-02db3b6ac6/output/patches/2.patch` — empty diff

---

## Patch 1 (signature: `8c5088e37f`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-d0fbd344-TP1-CP1-2-02db3b6ac6/output/patches/1.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/orc/vector/OrcDoubleColumnVector.java`

```diff
--- org/apache/flink/orc/vector/OrcDoubleColumnVector.java
+++ org/apache/flink/orc/vector/OrcDoubleColumnVector.java
@@ -31,7 +31,7 @@

 	public OrcDoubleColumnVector(DoubleColumnVector vector) {
 		super(vector);
-		this.vector = vector;
+		this.vector = new DoubleColumnVector();
 	}

 	@Override
```

---

## Patch 2 (signature: `995da0e0a8`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-d0fbd344-TP1-CP1-2-02db3b6ac6/output/patches/0.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/orc/vector/OrcDoubleColumnVector.java`

```diff
--- org/apache/flink/orc/vector/OrcDoubleColumnVector.java
+++ org/apache/flink/orc/vector/OrcDoubleColumnVector.java
@@ -30,7 +30,7 @@
 	private DoubleColumnVector vector;

 	public OrcDoubleColumnVector(DoubleColumnVector vector) {
-		super(vector);
+		super((BytesColumnVector) vector);
 		this.vector = vector;
 	}
```

---

## Patch 3 (signature: `9b02ef6d6c`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-d0fbd344-TP1-CP1-2-02db3b6ac6/output/patches/4.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/orc/vector/OrcTimestampColumnVector.java`

```diff
--- org/apache/flink/orc/vector/OrcTimestampColumnVector.java
+++ org/apache/flink/orc/vector/OrcTimestampColumnVector.java
@@ -33,7 +33,7 @@

 	public OrcTimestampColumnVector(TimestampColumnVector vector) {
 		super(vector);
-		this.vector = vector;
+		this.vector = (TimestampColumnVector) vector;
 	}

 	@Override
```

---

## Patch 4 (signature: `9e9350e45d`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-d0fbd344-TP1-CP1-2-02db3b6ac6/output/patches/3.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/orc/vector/OrcTimestampColumnVector.java`

```diff
--- org/apache/flink/orc/vector/OrcTimestampColumnVector.java
+++ org/apache/flink/orc/vector/OrcTimestampColumnVector.java
@@ -32,7 +32,7 @@
 	private TimestampColumnVector vector;

 	public OrcTimestampColumnVector(TimestampColumnVector vector) {
-		super(vector);
+		super((BytesColumnVector) vector);
 		this.vector = vector;
 	}
```

---

