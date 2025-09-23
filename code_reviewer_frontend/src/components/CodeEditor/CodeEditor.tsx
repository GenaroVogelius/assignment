import { cn } from "@/lib/utils";
import React, { useEffect, useRef, useState } from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

interface CodeEditorProps {
  value: string;
  onChange: (value: string) => void;
  language: string;
  placeholder?: string;
  className?: string;
  minHeight?: string;
  required?: boolean;
}

// Language mapping for react-syntax-highlighter
const languageMap: Record<string, string> = {
  javascript: "javascript",
  typescript: "typescript",
  python: "python",
  java: "java",
  cpp: "cpp",
  c: "c",
  csharp: "csharp",
  php: "php",
  ruby: "ruby",
  go: "go",
  rust: "rust",
  swift: "swift",
  kotlin: "kotlin",
  scala: "scala",
  r: "r",
  matlab: "matlab",
  sql: "sql",
  html: "html",
  css: "css",
  scss: "scss",
  json: "json",
  xml: "xml",
  yaml: "yaml",
  markdown: "markdown",
  bash: "bash",
  powershell: "powershell",
};

export function CodeEditor({
  value,
  onChange,
  language,
  placeholder = "Paste your code here...",
  className,
  minHeight = "200px",
  required = false,
}: CodeEditorProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [textareaValue, setTextareaValue] = useState(value);

  // Update textarea value when prop changes
  useEffect(() => {
    setTextareaValue(value);
  }, [value]);

  const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newValue = e.target.value;
    setTextareaValue(newValue);
    onChange(newValue);
  };


  const handleKeyDown = (e: React.KeyboardEvent) => {
    // Handle tab key for indentation
    if (e.key === "Tab") {
      e.preventDefault();
      const textarea = textareaRef.current;
      if (textarea) {
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const newValue =
          textareaValue.substring(0, start) +
          "  " +
          textareaValue.substring(end);
        setTextareaValue(newValue);
        onChange(newValue);

        // Set cursor position after the inserted spaces
        setTimeout(() => {
          textarea.selectionStart = textarea.selectionEnd = start + 2;
        }, 0);
      }
    }
  };

  const mappedLanguage = languageMap[language.toLowerCase()] || "text";

  const LINE_HEIGHT = "1.6";

  return (
    <div
      className={cn(
        "relative border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden",
        "bg-white dark:bg-gray-900 shadow-sm hover:shadow-md transition-shadow duration-200",
        "focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-blue-500",
        className
      )}
    >
      {/* Syntax highlighted background */}
      <div className="absolute inset-0 pointer-events-none">
        <SyntaxHighlighter
          language={mappedLanguage}
          style={vscDarkPlus}
          customStyle={{
            margin: 0,
            padding: "10px 20px",
            background: "transparent",
            fontSize: "14px",
            lineHeight: LINE_HEIGHT,
            minHeight: minHeight,
            fontFamily:
              'ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace',
          }}
          showLineNumbers={true}
          wrapLines={true}
          wrapLongLines={true}
        >
          {textareaValue || placeholder}
        </SyntaxHighlighter>
      </div>

      {/* Editable textarea overlay */}
      <textarea
        ref={textareaRef}
        value={textareaValue}
        onChange={handleTextareaChange}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        required={required}
        className={cn(
          "relative w-full bg-transparent border-none outline-none resize-none font-mono text-sm",
          "text-transparent caret-blue-500 dark:caret-blue-400",
          "placeholder:text-transparent",
          "focus:ring-0 focus:outline-none",
          "overflow-hidden"
        )}
        style={{
          minHeight: minHeight,
          padding: "10px 18px",
          paddingLeft: "40px",
          lineHeight: LINE_HEIGHT,
          fontSize: "13px",
        }}
        spellCheck={false}
        autoComplete="off"
        autoCorrect="off"
        autoCapitalize="off"
      />
    </div>
  );
}
