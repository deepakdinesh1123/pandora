import React, { useRef, useState } from "react";
import "styles/app.module.css";

import Editor from "@monaco-editor/react";

export default function CodeEditor(props) {
  const [theme, setTheme] = useState("vs-dark");
  const editorRef = useRef(null);

  function handleEditorChange(event) {
    props.onChange(editorRef.current.getValue());
  }

  function handleEditorDidMount(editor, monaco) {
    editorRef.current = editor;
  }

  return (
    <>
      <div className="codeeditor" style={{ height: '660px' }}>
        <Editor
          height="calc(100% - 0px)" // By default, it fully fits with its parent
          theme={theme}
          defaultLanguage="dockerfile"
          value={props.codeEditorValue}
          onMount={handleEditorDidMount}
          onChange={handleEditorChange}
        />
      </div>
    </>
  );
}
