import { ChromaClient } from "chromadb";
import { randomUUID } from "crypto";

/**
 * VectorMemory - Chroma-backed vector memory for agents.
 *
 * Collections used:
 *  - agent_episodic: conversation/personal memories
 *  - agent_semantic: docs/knowledge
 */
export class VectorMemory {
  /**
   * @param {Object} config
   * @param {string} config.chromaUrl - e.g. "http://localhost:8000"
   * @param {(input: string) => Promise<number[]>} config.embeddingFn
   */
  constructor(config) {
    this.client = new ChromaClient({ path: config.chromaUrl });
    this.embeddingFn = config.embeddingFn;
    this.episodic = undefined;
    this.semantic = undefined;
  }

  async init() {
    this.episodic = await this.client.getOrCreateCollection({
      name: "agent_episodic",
      metadata: { "hnsw:space": "cosine" },
    });

    this.semantic = await this.client.getOrCreateCollection({
      name: "agent_semantic",
      metadata: { "hnsw:space": "cosine" },
    });
  }

  ensureCollections() {
    if (!this.episodic || !this.semantic) {
      throw new Error("VectorMemory not initialized; call init() first.");
    }
  }

  /**
   * Store a conversation message as episodic memory.
   * @param {Object} msg
   * @param {string} msg.userId
   * @param {"user"|"assistant"|"system"} msg.role
   * @param {string} msg.text
   * @param {string} msg.sessionId
   * @param {string} msg.source - e.g. "whatsapp", "webchat"
   * @param {number} [msg.importance] - 0..1 (default 0.5)
   * @param {string} [msg.timestamp] - ISO string (default now)
   */
  async storeMessage(msg) {
    this.ensureCollections();

    const importance = msg.importance ?? 0.5;
    // drop very low-importance noise
    if (importance < 0.2) return;

    const id = randomUUID();
    const embedding = await this.embeddingFn(msg.text);
    const timestamp = msg.timestamp || new Date().toISOString();

    await this.episodic.add({
      ids: [id],
      documents: [msg.text],
      metadatas: [
        {
          user_id: msg.userId,
          role: msg.role,
          source: msg.source,
          session_id: msg.sessionId,
          timestamp,
          importance,
        },
      ],
      embeddings: [embedding],
    });
  }

  /**
   * Recall episodic memories relevant to a query.
   * @param {Object} params
   * @param {string} params.userId
   * @param {string} params.query
   * @param {number} [params.k]
   * @param {number} [params.minImportance]
   */
  async recallEpisodic(params) {
    this.ensureCollections();

    const { userId, query, k = 8, minImportance = 0.3 } = params;
    const embedding = await this.embeddingFn(query);

    const res = await this.episodic.query({
      queryEmbeddings: [embedding],
      nResults: k,
      where: {
        $and: [
          { user_id: userId },
          { importance: { $gte: minImportance } },
        ],
      },
    });

    const docs = res.documents?.[0] ?? [];
    const metas = res.metadatas?.[0] ?? [];
    const dists = res.distances?.[0] ?? [];

    return docs.map((text, i) => ({
      text,
      metadata: metas[i],
      distance: dists[i],
    }));
  }

  /**
   * Store a long-form document into semantic knowledge.
   * @param {string} docId
   * @param {string} text
   * @param {Object} [baseMeta]
   */
  async storeDocument(docId, text, baseMeta = {}) {
    this.ensureCollections();

    const chunks = chunkText(text, 1000, 200);

    const ids = [];
    const docs = [];
    const metas = [];
    const embeds = [];

    for (let i = 0; i < chunks.length; i++) {
      const chunk = chunks[i];
      ids.push(`${docId}:${i}`);
      docs.push(chunk);
      metas.push({ ...baseMeta, doc_id: docId, chunk_index: i });
      embeds.push(await this.embeddingFn(chunk));
    }

    await this.semantic.add({
      ids,
      documents: docs,
      metadatas: metas,
      embeddings: embeds,
    });
  }

  /**
   * Search semantic knowledge.
   * @param {string} query
   * @param {number} [k]
   * @param {Object} [where]
   */
  async searchKnowledge(query, k = 10, where = {}) {
    this.ensureCollections();

    const embedding = await this.embeddingFn(query);

    const res = await this.semantic.query({
      queryEmbeddings: [embedding],
      nResults: k,
      where,
    });

    const docs = res.documents?.[0] ?? [];
    const metas = res.metadatas?.[0] ?? [];
    const dists = res.distances?.[0] ?? [];

    return docs.map((text, i) => ({
      text,
      metadata: metas[i],
      distance: dists[i],
    }));
  }
}

/**
 * Simple sentence-based text chunker.
 * @param {string} text
 * @param {number} [maxLen]
 * @param {number} [overlap] - currently unused, for future improvements
 */
function chunkText(text, maxLen = 1000, overlap = 200) {
  const sentences = text.split(/(?<=[.!?])\s+/);
  const chunks = [];
  let current = "";

  for (const sentence of sentences) {
    if ((current + " " + sentence).length > maxLen) {
      if (current) chunks.push(current.trim());
      current = sentence;
    } else {
      current += (current ? " " : "") + sentence;
    }
  }
  if (current.trim()) chunks.push(current.trim());

  return chunks;
}
