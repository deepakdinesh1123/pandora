import dynamic from 'next/dynamic';
import { useEffect, useState } from 'react';
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

    const [editorValue, setEditorValue] = useState(null);
    const [terminalValue, setTerminalValue] = useState("");
    const [loading, setLoading] = useState(true);
    const router = useRouter();

    function handleEditorChange(newValue) {
        setEditorValue(newValue);
    }

    function handleTerminalKeyPress(newValue) {
        setTerminalValue(terminalValue + newValue);
        console.log(terminalValue);
    }

    useEffect(() => {
        const containerCreated = () => {
            let build_id = router.query.build_id;
            let build_status = "unfinished";


            const evtSource = new EventSource(`http://localhost:8080/build_image/${build_id}`);
            evtSource.addEventListener("update", (event) => {
                console.log(event);
            })
            evtSource.addEventListener("end", (event) => {
                build_status = "finished";
                setLoading(false);
                evtSource.close();
            })
        }
        containerCreated();
        const startContainer = () => {
            let image_name = router.query.image_name;
            let container_name = "sleep";
            let container_settings = {};

            axios.post("http://localhost:8080/create_container",
                {
                    'image_name': image_name,
                    'container_name': container_name,
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
                    <div>
                        <p style={{ color: 'black', margin: '4px', padding: '5px', border: '1px solid black' }}>Navbar</p>
                    </div>
                    <div style={{ height: '500px', backgroundColor: 'black' }}>
                        {
                            loading ? (<Loader />) : <CodeEditor
                                codeEditorValue={editorValue}
                                onChange={handleEditorChange}

                            />
                        }
                        {
                            loading ? (<Loader />) : <CodeTerminal
                                terminalValue={terminalValue}
                                onKeyDown={handleTerminalKeyPress}
                            />
                        }
                    </div>
                </div>
            </div>
        </>
    )
}
