# Bug: bugsdotjar-repairllama-flink-d0fbd344-TP1-CP1-0-2f78a499be

## Summary
- Total patch files: **5**
- Unique patches: **4**
- Invalid/unparseable patch files: **1**

## Invalid / unparseable patch files
- `bugsdotjar-repairllama-flink-d0fbd344-TP1-CP1-0-2f78a499be/output/patches/2.patch` — empty diff

---

## Patch 1 (signature: `60376bd795`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-d0fbd344-TP1-CP1-0-2f78a499be/output/patches/4.patch`

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
+		this.vector = new TimestampColumnVector();
 	}

 	@Override
```

---

## Patch 2 (signature: `70699d411d`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-d0fbd344-TP1-CP1-0-2f78a499be/output/patches/1.patch`

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
+		this.doubleVector = vector;
 	}

 	@Override
```

---

## Patch 3 (signature: `995da0e0a8`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-d0fbd344-TP1-CP1-0-2f78a499be/output/patches/0.patch`

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

## Patch 4 (signature: `9e9350e45d`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-d0fbd344-TP1-CP1-0-2f78a499be/output/patches/3.patch`

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

