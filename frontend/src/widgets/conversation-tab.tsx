import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { streamConversation } from "@/entities/conversation/stream-conversation";
import { useState } from "react";

// Make them changable later
const userId = "user1";
const graphId = "graph1";

type Message = { text: string; author: "user" | "agent" };

export const ConversationTab = () => {
  const [input, setInput] = useState("");
  const conversationId = self.crypto.randomUUID();
  const [messages, setMessages] = useState<Message[]>([]);
  const [stateId, setStateId] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);

  const initializeConversation = () => {
    if (messages.length > 0) return;
    streamConversation(
      {
        user_id: userId,
        graph_id: graphId,
        conversation_id: conversationId,
      },
      // onMessage
      (_message, stateId) => {
        if (stateId) {
          setStateId(stateId);
        }
      },
      // onDone
      () => {
        console.log(`Conversation initialized. id: ${conversationId}`);
      },
      // onError
      (err) => {
        // Show some feedback to users later
        console.error("error", err);
      }
    );
  };

  const handleChange: React.ChangeEventHandler<HTMLTextAreaElement> = (e) => {
    setInput(e.target.value);
  };

  const handleClickButton = () => {
    setMessages((prev) => [...prev, { text: input, author: "user" }]);
    setIsStreaming(true);
    streamConversation(
      {
        user_id: userId,
        graph_id: graphId,
        conversation_id: conversationId,
        state_id: stateId,
        user_message: input,
      },
      // onMessage
      (message, stateId) => {
        if (message) {
          setMessages((prev) => [...prev, { text: message, author: "agent" }]);
        }
        if (stateId) {
          setStateId(stateId);
        }
      },
      // onDone
      () => {
        console.log(`Conversation initialized. id: ${conversationId}`);
        setIsStreaming(false);
      },
      // onError
      (err) => {
        // Show some feedback to users later
        console.error("error", err);
        setIsStreaming(false);
      }
    );
    setInput("");
  };

  return (
    <div className="h-full p-8 flex flex-col">
      {messages.map((m) => {
        return (
          <div
            key={m.text}
            className={`p-2 rounded-lg ${
              m.author === "user" ? "ml-auto bg-gray-400" : ""
            }`}
          >
            <p>{m.text}</p>
          </div>
        );
      })}
      <div className="flex flex-col gap-2 absolute bottom-6 left-2 right-2">
        <Textarea
          onClick={messages.length > 0 ? undefined : initializeConversation}
          value={input}
          onChange={handleChange}
          disabled={isStreaming}
        />
        <div className="flex justify-end">
          <Button onClick={handleClickButton} size="icon">
            ↑
          </Button>
        </div>
      </div>
    </div>
  );
};
