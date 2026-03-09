import { ChromaClient } from "chromadb";

async function main() {
  const client = new ChromaClient({ path: "http://localhost:8000" });

  console.log("[test] Connecting to Chroma at http://localhost:8000 ...");

  const hbRes = await fetch("http://localhost:8000/api/v2/heartbeat");
  if (!hbRes.ok) {
    throw new Error(`[test] Heartbeat failed: ${hbRes.status} ${hbRes.statusText}`);
  }
  console.log("[test] Heartbeat OK");

  const collectionName = "test_vector_memory";
  const collection = await client.getOrCreateCollection({
    name: collectionName,
    metadata: { "hnsw:space": "cosine" }
  });
  console.log(`[test] Using collection: ${collection.name}`);

  const id = "test-doc-1";
  const text = "This is a test document for vector memory.";
  const embedding = Array.from({ length: 64 }, () => Math.random());

  await collection.add({
    ids: [id],
    documents: [text],
    embeddings: [embedding],
    metadatas: [{ source: "smoke-test", created_at: new Date().toISOString() }]
  });
  console.log("[test] Inserted test document");

  const queryResult = await collection.query({
    queryEmbeddings: [embedding],
    nResults: 3
  });

  console.log("[test] Query result:");
  console.dir(queryResult, { depth: null });

  console.log("[test] Done.");
}

main().catch((err) => {
  console.error("[test] Error:", err);
  process.exit(1);
});
