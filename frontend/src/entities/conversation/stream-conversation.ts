type Response = {
  is_final_message: boolean;
  conversation_id: string;
  text: string | null;
  state_id: string | null;
  current_node_id: string | null;
};

export async function streamConversation(
  payload: any,
  onMessage: (message: string | null, stateId: string | null, conversationId: string) => void,
  onDone: () => void,
  onError: (e: any) => void
) {
  const res = await fetch("/api/conversation/stream", {
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
  let buffer = "";

  function processResponse(json: string) {
    try {
      const obj = JSON.parse(json) as Response;
      onMessage(obj.text, obj.state_id, obj.conversation_id);
    } catch (e) {
      console.error("process response error", e, json);
      onError(e);
    }
  }

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      // Process all complete lines
      let newlineIndex;
      while ((newlineIndex = buffer.indexOf("\n")) >= 0) {
        const line = buffer.slice(0, newlineIndex).trim();
        buffer = buffer.slice(newlineIndex + 1);
        if (line) {
          processResponse(line);
        }
      }
    }

    // If something remains without a trailing newline
    if (buffer.trim()) {
      processResponse(buffer.trim());
    }
    onDone();
  } catch (e) {
    onError(e);
  }
}