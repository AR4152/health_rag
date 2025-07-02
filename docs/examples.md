# Examples

## Query Without Context vs. With Context

Below is a demonstration of how the toolkit behaves when you query **without** and **with** your personal health documents.

First, create the vector store:

```bash
ml create_context health_rag sample_lab_report.pdf
```

Output:

```
Vector store saved to 'vector_store' with 6 chunks.
```


### Query **Without** Context

```bash
ml query health_rag "What is my RBC count? Is it normal?"
```

Output:

```
I'd be happy to help you understand your Red Blood Cell (RBC) count. However, I need to clarify that I'm a text-based AI and don't have access to your personal medical information.
That being said, I can provide general information on RBC counts and what's considered normal.

The RBC count, also known as the hematocrit (Hct), is a measure of the proportion of red blood cells in your blood. It's an important indicator of your overall health.

In adults, a normal RBC count is typically between 4.32 and 5.72 grams per deciliter (g/dL) or 4.3–5.7% of the total blood volume. For women, this range is slightly lower: 4.10–5.50 g/dL or 4.1–5.5%.

If your RBC count is outside this normal range, it may indicate an underlying condition that needs attention.
```


### Query **With** Context

```bash
ml query health_rag "What is my RBC count? Is it normal?" --vectorstore_path ./vector_store
```

Output:

```
Your RBC (Red Blood Cell) count is listed as 33.3, with a range of 33–73.

According to the table provided, your RBC count falls within the normal range of 33–73. Therefore, based on this information, your RBC count is normal.
```
