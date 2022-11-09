import React, { useState } from "react";
import dynamic from 'next/dynamic';
import 'styles/index.module.css';
import { useRouter } from 'next/router';
import axios from 'axios';

const CodeEditor = dynamic(() => import('../components/CodeEditor'), {
  ssr: false
})


export default function Home() {
  const router = useRouter();
  const [editorValue, setEditorValue] = useState("# write your dockerfile here");

  function handleEditorChange(newValue, editor=null) {
    setEditorValue(newValue);
  }

  function submit(e) {
    e.preventDefault();
    axios.post("http://localhost:8080/build_image/",
      {
        "name": "container",
        "tag": "latest",
        "dockerfile": editorValue
      }
    ).then((res) => {
      if (res['data']['status'] == "success") {
        router.push({pathname: '/editor',
          query: {'build_id': res['data']['build_id'], 
          'image_name': 'container',
          'image_tag': 'latest'
        }
        });
      }
      else {
        alert("Fix errors in your dockerfile and submit again");
      }
    }).catch(e => {
      console.log(e);
    })
  }

  return (
    <>
      <div id="index-root">
        <div id="root">
          <div>
            <p style={{ color: 'black', margin: '4px', padding: '5px', border: '1px solid black' }}>Navbar</p>
            <button onClick={submit} > Submit</button>
          </div>

          <div style={{ height: '650px', backgroundColor: 'black' }}>
            < CodeEditor
              codeEditorValue={editorValue}
              onChange={handleEditorChange}
              defaultLanguage={"dockerfile"}
            />
          </div>
        </div>
      </div>
    </>
  )
}
