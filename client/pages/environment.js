import { useEffect } from 'react';
import axios from 'axios';

export default function Environments() {
    // useEffect(async () => {
    //     const url = window.location.href;
    //     const code = url.slice(url.indexOf("=") + 1, url.length);
    //     if (code.length != url.length) {
    //         const resp = await axios({
    //             method: "post",
    //             url: "http://localhost:8080/authenticate/github/",
    //             params: {
    //                 code: code
    //             }
    //         })
    //         localStorage.setItem("User", "Logged in");
    //     }
    // }, []);

    // return (
    //     <div> Environments</div>
    // )
    return (
        <>
        </>
    )
}
