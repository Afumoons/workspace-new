// Prune low-importance, old episodic memories from Chroma (agent_episodic)
// Usage:
//   node scripts/pruneVectorMemory.mjs
//
// Behavior:
//   - Connects to Chroma at http://localhost:8000
//   - Targets collection "agent_episodic"
//   - Lists all items and deletes those matching:
//       importance < MIN_IMPORTANCE && timestamp < CUTOFF_DAYS_AGO
//
// Notes:
//   - This is a simple maintenance script, not optimized for huge datasets.

import { ChromaClient } from "chromadb";

const CHROMA_URL = process.env.CHROMA_URL || "http://localhost:8000";
const COLLECTION_NAME = "agent_episodic";

// Config: tweak as needed
const MIN_IMPORTANCE = parseFloat(process.env.MEMORY_PRUNE_MIN_IMPORTANCE ?? "0.3");
const CUTOFF_DAYS = parseInt(process.env.MEMORY_PRUNE_CUTOFF_DAYS ?? "30", 10);

function daysAgoDate(days) {
  const d = new Date();
  d.setDate(d.getDate() - days);
  return d;
}

async function main() {
  console.log(`[prune] Connecting to Chroma at ${CHROMA_URL} ...`);
  const client = new ChromaClient({ path: CHROMA_URL });

  const cutoffDate = daysAgoDate(CUTOFF_DAYS);
  console.log(
    `[prune] Pruning items with importance < ${MIN_IMPORTANCE} and timestamp < ${cutoffDate.toISOString()}`,
  );

  const collection = await client.getOrCreateCollection({ name: COLLECTION_NAME });

  // Fetch all ids + metadatas in batches
  const batchSize = 500;
  let offset = 0;
  let totalDeleted = 0;
  let totalScanned = 0;

  while (true) {
    const res = await collection.get({
      include: ["metadatas"],
      limit: batchSize,
      offset,
    });

    const ids = res.ids ?? [];
    const metas = res.metadatas ?? [];

    if (!ids.length) break;

    const toDelete = [];

    for (let i = 0; i < ids.length; i++) {
      const id = ids[i];
      const meta = metas[i] || {};

      const importance = typeof meta.importance === "number" ? meta.importance : parseFloat(meta.importance ?? "0");
      const ts = meta.timestamp ? new Date(meta.timestamp) : null;

      totalScanned++;

      if (!ts || Number.isNaN(ts.getTime())) {
        continue; // skip records without valid timestamp
      }

      if (importance < MIN_IMPORTANCE && ts < cutoffDate) {
        toDelete.push(id);
      }
    }

    if (toDelete.length) {
      console.log(`[prune] Deleting ${toDelete.length} items in this batch...`);
      await collection.delete({ ids: toDelete });
      totalDeleted += toDelete.length;
    }

    offset += batchSize;
  }

  console.log(`[prune] Scanned ${totalScanned} items, deleted ${totalDeleted}.`);
}

main().catch((err) => {
  console.error("[prune] Error:", err);
  process.exit(1);
});
