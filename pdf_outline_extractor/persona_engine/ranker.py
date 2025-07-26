# persona_engine/ranker.py
from sentence_transformers import SentenceTransformer, util
import torch

class SectionRanker:
    def __init__(self, model_name='paraphrase-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def rank_sections(self, sections, persona, job, top_k=5):
        query = f"{persona} needs to {job}"
        query_embedding = self.model.encode(query, convert_to_tensor=True)

        results = []
        for section in sections:
            section_text = section["text"]
            section_embedding = self.model.encode(section_text, convert_to_tensor=True)
            score = util.pytorch_cos_sim(query_embedding, section_embedding).item()
            section["similarity_score"] = score
            results.append(section)

        # Sort by similarity
        results.sort(key=lambda x: x["similarity_score"], reverse=True)

        # Assign rank
        for i, sec in enumerate(results[:top_k]):
            sec["importance_rank"] = i + 1

        return results[:top_k]
