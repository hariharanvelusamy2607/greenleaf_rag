import logging
from datetime import datetime

from rag_pipeline import answer_question

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

if __name__ == "__main__":
    user_question = "What are the races in Project Greenleaf?"
    result = answer_question(user_question, top_k=5)
    logging.info("Prompt sent at %s", datetime.utcnow().isoformat())
    print("=== Model Response ===")
    print(result["answer"])
    print("\n=== Context Used ===")
    print(result["context"])
    print("Timestamp:", datetime.utcnow().isoformat())

