# summarizer.py

from transformers import pipeline

class DocumentSummarizer:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        # Initialize summarization pipeline
        self.summarizer = pipeline(
            "summarization",
            model=model_name,
            tokenizer=model_name,
            framework="pt",
            device=-1  # set to -1 for CPU
        )

    def chunk_text(self, text, max_tokens=512):
        """
        Split text into chunks of up to max_tokens words.
        """
        words = text.split()
        chunks = []
        for i in range(0, len(words), max_tokens):
            chunk = words[i:i + max_tokens]
            chunks.append(" ".join(chunk))
        return chunks

    def summarize_chunk(self, chunk, min_length=100, max_length=400):
        """
        Summarize a single chunk.
        """
        result = self.summarizer(
            chunk,
            min_length=min_length,
            max_length=max_length,
            do_sample=False,
            num_beams=5
        )
        return result[0]["summary_text"]

    def get_document_insights(self, text, doc_type=None, filename=None):
        """
        Full summarization workflow: clean, chunk, summarize, combine.
        """
        # 1. Preprocess text
        clean_text = text.replace("\n", " ").strip()

        # 2. Chunk if long
        chunks = self.chunk_text(clean_text, max_tokens=512)

        # 3. Summarize each chunk
        summaries = [self.summarize_chunk(chunk) for chunk in chunks]

        # 4. Combine chunk summaries
        combined_summary = " ".join(summaries)

        # 5. Final concise summarization if multiple chunks
        if len(chunks) > 1:
            final_summary = self.summarize_chunk(
                combined_summary,
                min_length=30,
                max_length=150
            )
        else:
            final_summary = combined_summary

        # Return consistent structure
        return {
            "summary": final_summary,
            "action_items": [],
            "deadlines": [],
            "risks": [],
            "priority": "Medium"
        }
