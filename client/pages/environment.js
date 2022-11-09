import { useEffect } from 'react';
import axios from 'axios';

export default function Environments() {
    useEffect(async () => {
        const url = window.location.href;
        const code = url.slice(url.indexOf("=") + 1, url.length);
        if (code.length != url.length) {
            const resp = await axios({
                method: "post",
                url: "http://localhost:8080/authenticate/github/access_token/",
                params: {
                    code: code
                }
            })
            alert(resp);
        }
        else {
            // TODO write logic for already logged in users
        }
    }, []);

    return (
        <a
            className="login-link"
            href={`https://github.com/login/oauth/authorize?scope=user&client_id=${process.env.GITHUB_CLIENT_ID}`}
        >Github Login</a>
    )
}
