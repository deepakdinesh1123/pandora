import React, { useState } from "react";
import dynamic from 'next/dynamic';
import 'styles/index.module.css';
import { useRouter } from 'next/router';
import axios from 'axios';
import { black } from "ansi-colors";

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
    const inp = document.getElementById("filename");
    const filename = inp.value;
    if(filename === "") {
      alert("Enter a name for your dockerfile");
    }
    axios.post("http://localhost:8080/build_image/",
      {
        "name": filename,
        "tag": "latest",
        "dockerfile": editorValue
      }
    ).then((res) => {
      if (res['data']['status'] == "success") {
        router.push({pathname: '/editor',
          query: {'build_id': res['data']['build_id'],
          'image_name': filename,
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

  const inputStyle = {
    width: "200px",
    marginRight: "10px",
    height: "22px",
    padding: "8px",
    borderRadius: "5px",
  }

  const divStyle = {
    marginTop: "10px"
  }

  const buttonStyle = {
    padding: "8px",
    height: "39px",
    width: "100px",
    borderRadius: "15px"
  }



  return (
    <>
      <div id="index-root" style={{backgroundColor: "black", padding: "5px"}}>
        <div id="root">
          <div style={{display: "flex", justifyContent: "center", alignItems: "center", backgroundColor: "black", color: "white", padding: "10px"}}>
            <div style={{}}>
              P A N D O R A
            </div>
          </div>
          <div style={{ height: '660px', backgroundColor: 'black' }}>
            < CodeEditor
              codeEditorValue={editorValue}
              onChange={handleEditorChange}
              defaultLanguage={"dockerfile"}
            />
          </div>
        </div>
        <div style={divStyle}>
            <input type="text" id="filename" placeholder="Enter the name of your dockerfile" style={inputStyle}></input>
            <button style={buttonStyle} onClick={submit} >Submit</button>
        </div>
      </div>
    </>
  )
}
