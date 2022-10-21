import React, { useEffect } from "react";
import { Terminal } from "xterm";
import { AttachAddon } from "xterm-addon-attach";
import { FitAddon } from "xterm-addon-fit";
import { WebLinksAddon } from "xterm-addon-web-links";

import "xterm/css/xterm.css";

let term;


const fitAddon = new FitAddon();

export default function CodeTerminal(props) {

  const openInitTerminal = () => {
    const terminalContainer = document.getElementById("xterm");
    while (terminalContainer.children.length) {
      terminalContainer.removeChild(terminalContainer.children[0]);
    }

    const isWindows =
      ["Windows", "Win16", "Win32", "WinCE"].indexOf(navigator.platform) >= 0;
    term = new Terminal({
      windowsMode: isWindows,
      convertEol: true,
      fontFamily: `'Fira Mono', monospace`,
      fontSize: 16,
      fontWeight: 400,
      rendererType: "canvas"
    });

    term.setOption("theme", {
      background: "black",
      foreground: "white"
    });

    term.loadAddon(fitAddon);
    const webLinksAddon = new WebLinksAddon();
    term.loadAddon(webLinksAddon);

    term.open(terminalContainer);

    term.element.style.padding = "20px";

    fitAddon.fit();
    term.focus();
    term.write("$");

    term.onKey(key => {
      const char = key.domEvent.key;
      if (char === "Enter") {
        props.onKeyDown(term, "Enter");
        term.write("\n$");
      } else if (char === "Backspace") {
        props.onKeyDown(term, "Backspace");
        term.write("\b \b");
      } else {
        props.onKeyDown(term, char);
        term.write(char);
      }
    });

  };


  const windowChange = () => {
    fitAddon.fit();
  };
  useEffect(() => {
    openInitTerminal();
    window.addEventListener("resize", windowChange);
  }, []);

  return (
    <div className="freeaiterm-wrap">
      <div id="xterm" style={{ height: "80%", width: "100%" }}/>
    </div>
  )
}
