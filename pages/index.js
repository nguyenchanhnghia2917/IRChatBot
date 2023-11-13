import Head from "next/head";
import Image from "next/image";
import { Inter } from "next/font/google";
import TypingAnimation from "./TypingAnimation";
import styles from "@/styles/Home.module.css";
import { CodeBlock, dracula, CopyBlock } from "react-code-blocks";
import { useState } from "react";
import axios from "axios";
const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  const [inputValue, setInputValue] = useState("");
  const [chatLog, setChatLog] = useState([]);
  const [isLoading, setIsLoanding] = useState(false);
  const splitMessage = (message) => {
    if (message.includes("cpp") || message.includes("python")) {
      const parts = message.split(/cpp|python/);
      const lastBacktickIndex = parts[1].lastIndexOf("```");

      const codePart = parts[1].split("```");

      return (
        <div>
          <div>{parts[0].replace(/```/g, "")}</div>
          <CodeBlock text={codePart[0]} showLineNumbers={false} />
          <div>{codePart[1].replace(/```/g, "")}</div>
        </div>
      );
    }
    return <div>{message}</div>;
  };
  const handleSubmit = (event) => {
    event.preventDefault();
    setChatLog((prevChatLog) => [
      ...prevChatLog,
      { type: "user", message: inputValue },
    ]);
    sendMessage(inputValue);
    setInputValue("");
  };

  const sendMessage = (message) => {
    const url = "http://127.0.0.1:5000/api/add";
    const header = {
      "Content-Type": "application/json",
    };

    const data = {
      string1: message
    };
    setIsLoanding(true);
    axios
      .post(url, data, { headers: header })
      .then((response) => {
        console.log(response);
        setChatLog((prevChatLog) => [
          ...prevChatLog,
          { type: "bot", message: response.data.result },
        ]);
        setIsLoanding(false);
      })
      .catch((error) => {
        setChatLog((prevChatLog) => [
          ...prevChatLog,
          { type: "bot", message: 'Tôi không biết' },
        ]);
        setIsLoanding(false);
        console.log(error);
      });
  };
  return (
    <>
      <div className=" flex justify-center items-center h-screen  ">
        <div className="  flex flex-col h-screen bg-gray-900  w-2/4   rounded-lg shadow-lg  ">
          <h1 className="bg-gradient-to-r from-blue-500 to-green-500 text-transparent bg-clip-text text-center py-3 font-bold text-6xl">
            ChatGPT
          </h1>

          <div className="bg-gradient-to-r from-blue-500 to-green-500 flex-grow p-6 overflow-y-scroll">
            <div className="flex flex-col space-y-4">
              {chatLog.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${
                    message.type === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`${
                      message.type === "user" ? "bg-blue-400" : "bg-gray-800"
                    } rounded-lg p-4 text-white max-w-sm`}
                  >
                    {message.type === "bot"
                      ? splitMessage(message.message)
                      : message.message}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div key={chatLog.length} className="flex justify-start">
                  <div className="bg-gray-800 rounded-lg p-4 text-white max-w-sm">
                    <TypingAnimation />
                  </div>
                </div>
              )}
            </div>
          </div>

          <form onSubmit={handleSubmit} className="flex-none p-6">
            <div className="flex rounded-lg border border-gray-700 bg-gray-800">
              <input
                type="text"
                className="flex-grow px-4 py-2 bg-transparent text-white focus:outline-none  "
                placeholder="Type your message..."
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
              />
              <button
                type="submit"
                className="bg-blue-500 rounded-lg px-4 py-2 text-white font-semibold focus:outline-none hover:bg-purple-600 transition-colors duration-300"
              >
                Send
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}
