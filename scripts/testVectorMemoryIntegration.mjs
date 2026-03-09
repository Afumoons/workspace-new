import { VectorMemory } from "../memory/vectorMemory.mjs";

// Dummy embedding function for the integration smoke test: avoids external API.
async function dummyEmbed(text) {
  // fixed-length vector with deterministic pseudo-random values based on text
  const len = 64;
  const out = new Array(len).fill(0);
  let seed = 0;
  for (let i = 0; i < text.length; i++) {
    seed = (seed * 31 + text.charCodeAt(i)) >>> 0;
  }
  for (let i = 0; i < len; i++) {
    seed = (seed * 1664525 + 1013904223) >>> 0;
    out[i] = (seed % 1000) / 1000; // 0..0.999
  }
  return out;
}

async function main() {
  const memory = new VectorMemory({
    chromaUrl: "http://localhost:8000",
    embeddingFn: dummyEmbed,
  });

  console.log("[int-test] Initializing VectorMemory...");
  await memory.init();
  console.log("[int-test] Initialized.");

  // 1) Store a test message
  console.log("[int-test] Storing test message...");
  await memory.storeMessage({
    userId: "test-user",
    role: "user",
    text: "Afu likes aggressive trading strategies and uses Binance.",
    sessionId: "test-session-1",
    source: "integration-test",
    importance: 0.8,
  });
  console.log("[int-test] Stored test message.");

  // 2) Recall with a related query
  console.log("[int-test] Recalling with query 'trading on Binance'...");
  const results = await memory.recallEpisodic({
    userId: "test-user",
    query: "trading on Binance",
    k: 5,
    minImportance: 0.3,
  });

  console.log("[int-test] Recall results:");
  console.dir(results, { depth: null });

  console.log("[int-test] Done.");
}

main().catch((err) => {
  console.error("[int-test] Error:", err);
  process.exit(1);
});
