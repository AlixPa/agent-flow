type Response = {
  is_final_message: boolean;
  conversation_id: string;
  text: string | null;
  state_id: string | null;
  current_node_id: string | null;
};

export async function streamConversation(
  payload: any,
  onMessage: (message: string | null, stateId: string | null) => void,
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

  function processResponse(json: string) {
    const obj = JSON.parse(json) as Response;

    try {
      onMessage(obj.text, obj.state_id);
    } catch (e) {
      console.error("process response error", e);
      onError(e);
    }
  }

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      processResponse(decoder.decode(value, { stream: true }));
    }
    onDone();
  } catch (e) {
    onError(e);
  }
}
