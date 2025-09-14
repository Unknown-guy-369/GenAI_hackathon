import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import {
  Send,
  Plus,
  Share,
  Copy,
  ThumbsUp,
  ThumbsDown,
  MoreHorizontal,
  Menu,
  Search,
  BookOpen,
  Bot,
  Code,
  Folder,
  Mic,
  Upload,
} from "lucide-react";

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: "assistant",
      content: `I can help you create a modern chat interface similar to what you've shown. Based on the screenshot, I'll build a React component with a dark theme, sidebar navigation, and chat functionality with message bubbles.`,
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);

  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);
  const fileInputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

//   handle submission to backend

const handleSend = async (customContent) => {
  const content = customContent || inputValue.trim();

  if (content) {
    const newMessage = {
      id: messages.length + 1,
      type: "user",
      content,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, newMessage]);
    setInputValue("");

    try {
      // Send message to FastAPI backend
      const response = await axios.post("http://127.0.0.1:8000/c", {
        text: content,   // send as text (backend detects type automatically)
      });

      // Backend reply
      const aiResponse = {
        id: messages.length + 2,
        type: "assistant",
        content: `✅ Saved as ${response.data.input_type}: ${response.data.content}`,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, aiResponse]);
    } catch (error) {
      console.error("Error sending message:", error);
      const errorMessage = {
        id: messages.length + 2,
        type: "assistant",
        content: "⚠️ Backend error: Could not save input.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    }
  }
};

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Handle File Upload
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleSend(`📎 Uploaded file: ${file.name}`);
    }
  };

  // Handle Voice Recording
  const toggleRecording = async () => {
    if (!recording) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const recorder = new MediaRecorder(stream);
        const chunks = [];

        recorder.ondataavailable = (event) => {
          if (event.data.size > 0) chunks.push(event.data);
        };

        recorder.onstop = () => {
          const blob = new Blob(chunks, { type: "audio/webm" });
          const audioUrl = URL.createObjectURL(blob);
          handleSend(`🎤 Voice message: [Audio Clip](${audioUrl})`);
        };

        recorder.start();
        setMediaRecorder(recorder);
        setRecording(true);
      } catch (err) {
        console.error("Microphone access denied:", err);
      }
    } else {
      mediaRecorder.stop();
      setRecording(false);
    }
  };

  const sidebarItems = [
    { icon: Plus, label: "New chat", active: false },
    { icon: Search, label: "Search chats", active: false },
    // { icon: BookOpen, label: "Library", active: false },
    // { icon: Bot, label: "Sora", active: false },
    // { icon: Code, label: "GPTs", active: false },
    // { icon: Code, label: "GPT Chat Free Online", active: false },
    // { icon: Code, label: "Coding Assistant", active: true },
    // { icon: Folder, label: "Projects", active: false, badge: "NEW" },
  ];

  const chatHistory = [
    "AI powered tool explanation",
    "FastAPI decorator fix",
    "Input field route names",
    "ER diagrams overview",
    "Synchronization variable explanation",
    "Segment base and limit",
    "Group by clause explanation",
    "Prefix in FastAPI",
    "waitpid() explanation",
  ];

  return (
    <div className="flex h-screen w-screen bg-gray-900 text-white overflow-hidden">
      {/* Sidebar */}
      <div
        className={`${
          sidebarOpen ? "w-64" : "w-0"
        } transition-all duration-300 overflow-hidden bg-gray-800 border-r border-gray-700`}
      >
        <div className="p-4">
          <div className="flex items-center gap-2 mb-6">
            <div className="w-8 h-8 bg-gradient-to-br from-green-400 to-blue-500 rounded-lg"></div>
            <span className="font-semibold">Nodium</span>
          </div>

          {/* Navigation Items */}
          <div className="space-y-2 mb-6">
            {sidebarItems.map((item, index) => (
              <div
                key={index}
                className={`flex items-center gap-3 p-2 rounded-lg cursor-pointer hover:bg-gray-700 ${
                  item.active ? "bg-gray-700" : ""
                }`}
              >
                <item.icon size={16} />
                <span className="text-sm">{item.label}</span>
                {item.badge && (
                  <span className="ml-auto text-xs bg-blue-600 px-2 py-1 rounded">
                    {item.badge}
                  </span>
                )}
              </div>
            ))}
          </div>

          {/* Chat History */}
          <div className="border-t border-gray-700 pt-4">
            <h3 className="text-sm font-medium mb-3 text-gray-400">Chats</h3>
            <div className="space-y-1">
              {chatHistory.map((chat, index) => (
                <div
                  key={index}
                  className="p-2 text-sm text-gray-300 hover:bg-gray-700 rounded cursor-pointer truncate"
                >
                  {chat}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 hover:bg-gray-700 rounded-lg"
            >
              <Menu size={20} />
            </button>
            <h1 className="font-semibold">Nodium</h1>
          </div>
          <div className="flex items-center gap-2">
            <button className="flex items-center gap-2 px-3 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg">
              <Share size={16} />
              Share
            </button>
            <button className="p-2 hover:bg-gray-700 rounded-lg">
              <Copy size={16} />
            </button>
            <button className="p-2 hover:bg-gray-700 rounded-lg">
              <MoreHorizontal size={16} />
            </button>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 ps-25 pe-25 space-y-6">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.type === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-3xl ${
                  message.type === "user" ? "bg-blue-600" : "bg-gray-700"
                } rounded-2xl p-4`}
              >
                <div className="whitespace-pre-wrap">{message.content}</div>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 border-t border-gray-700">
          <div className="max-w-4xl mx-auto">
            <div className="relative">
              <div className="flex items-end gap-3 bg-gray-800 rounded-2xl p-3 border border-gray-600">
                {/* File Upload */}
                <button
                  onClick={() => fileInputRef.current.click()}
                  className="p-2 hover:bg-gray-700 rounded-lg"
                >
                  <Plus size={20} />
                </button>
                <input
                  type="file"
                  ref={fileInputRef}
                  className="hidden"
                  onChange={handleFileChange}
                />

                {/* Textarea */}
                <textarea
                  ref={textareaRef}
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask anything"
                  className="flex-1 bg-transparent resize-none outline-none min-h-[24px] max-h-32"
                  rows={1}
                />

                {/* Voice Recording */}
                <button
                  onClick={toggleRecording}
                  className={`p-2 rounded-lg ${
                    recording
                      ? "bg-red-600 hover:bg-red-500"
                      : "hover:bg-gray-700"
                  }`}
                >
                  <Mic size={20} />
                </button>

                {/* Send */}
                <button
                  onClick={() => handleSend()}
                  disabled={!inputValue.trim()}
                  className="p-2 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-600 disabled:cursor-not-allowed rounded-lg"
                >
                  <Send size={20} />
                </button>
              </div>
            </div>
            <div className="text-center mt-2">
              <p className="text-xs text-gray-400">
                Nodium can make mistakes. Check important info.
                <button className="text-gray-300 hover:underline ml-1">
                  See Cookie Preferences.
                </button>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
