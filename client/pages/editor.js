import dynamic from 'next/dynamic';
import { useEffect, useRef, useState } from 'react';
import 'styles/index.module.css';
import { ClockLoader as Loader } from "react-spinners";
import { useRouter } from 'next/router';
import axios from 'axios';

const CodeTerminal = dynamic(() => import('../components/CodeTerminal'), {
    ssr: false
});

const CodeEditor = dynamic(() => import('../components/CodeEditor'), {
    ssr: false
})


export default function Editor() {

    const editorRef = useRef("");
    const terminalRef = useRef("");
    const [loading, setLoading] = useState(true);
    const router = useRouter();
    const { build_id, image_name, image_tag} = router.query;

    function handleEditorChange(newValue) {
        editorRef.current = newValue;
    }

    function handleTerminalKeyPress(newValue, term = null) {

        if (newValue === "Enter") {
            const inp = document.getElementById('filename');
            const filename = inp.value;
            if(filename === "") {
                alert("Filename not present");
            }
            axios.post(`http://localhost:8080/execute/req/${image_name}/`,
                {
                    "user_command": terminalRef.current,
                    "editor_content": editorRef.current,
                    "filename": filename
                }
            ).then((res) => {
                term.write(`\n${res['data']}\n`);
                term.write("$");
            }).catch(e => {
                console.log(e);
            })
            terminalRef.current = "";
        }
        else if (newValue === "Backspace") {
            terminalRef.current = terminalRef.current.slice(0, -1);
        }
        else {
            terminalRef.current += newValue;
        }
    }

    useEffect(() => {

        let build_status = "unfinished";

        function waitTillBuild(evtSource) {
            return new Promise((resolve) => {
                evtSource.addEventListener("end", (event) => {
                    build_status = "finished";
                    setLoading(false);
                    evtSource.close();
                    resolve();
                })
            })
        }
        
        const containerCreated = () => {
            let build_id = router.query.build_id;
            const evtSource = new EventSource(`http://localhost:8080/build_image/${build_id}`);
            evtSource.addEventListener("update", (event) => {
                console.log(event);
            })
            // evtSource.addEventListener("end", (event) => {
            //     build_status = "finished";
            //     setLoading(false);
            //     evtSource.close();
            // })
            waitTillBuild(evtSource).then(() => {
                console.log("Built");
            })
        }
        containerCreated();
        const startContainer = () => {
            let container_settings = {};
            axios.post("http://localhost:8080/create_container",
                {
                    'image_name': image_name,
                    'container_name': image_name,
                    'container_settings': container_settings
                }
            ).then((res) => {
                console.log(res);
            }).catch(e => {
                console.log(e);
            })
        }
        startContainer();
    }, [])


    return (
        <>
            <div id="index-root">
                <div id="root">
                    <div style={{display: "flex", justifyContent: "center", alignItems: "center", backgroundColor: "black", color: "white", padding: "10px"}}>
                        <div style={{}}> E D I T O R </div>
                    </div>
                    <div>
                        <input type='text' id='filename' placeholder='Enter filename'></input>
                    </div>
                    <div style={{ height: '500px', backgroundColor: 'black' }}>
                        {
                            loading ? (<Loader />) : <CodeEditor
                                codeEditorValue={editorRef.current}
                                onChange={handleEditorChange}
                                defaultLanguage={"java"}
                            />
                        }
                        {
                            loading ? (<Loader />) : <CodeTerminal
                                onKeyDown={handleTerminalKeyPress}
                            />
                        }
                    </div>
                </div>
            </div>
        </>
    )
}
