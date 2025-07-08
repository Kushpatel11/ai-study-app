from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")


def build_embeddings(chunks):
    return model.encode(chunks, convert_to_tensor=True)


def match_question_to_chunk(question, chapter_data):
    q_embed = model.encode(question, convert_to_tensor=True)
    sims = util.cos_sim(q_embed, chapter_data["embeds"])[0]
    best_idx = sims.argmax()
    return chapter_data["chunks"][best_idx], sims[best_idx].item()
