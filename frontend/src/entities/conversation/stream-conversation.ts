export async function streamConversation(
  payload: any,
  onMessage: (msg: any) => void,
  onDone: () => void,
  onError: (e: any) => void
) {
  const res = await fetch("http://127.0.0.1:8080/conversation/stream", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok || !res.body) {
    onError(new Error(`HTTP error ${res.status}`));
    return;
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder("utf-8");

  function processChunk(chunk: string) {
    const jsons = chunk
      .split("data: ")
      .map((c) => c.trim())
      .filter((c) => c);
    for (const json of jsons) {
      try {
        console.log("json", json);
        onMessage(json);
      } catch (error) {
        console.error("process chunk error", error);
      }
    }
  }

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      processChunk(decoder.decode(value, { stream: true }));
    }
    processChunk("");
    onDone();
  } catch (e) {
    onError(e);
  }
}
