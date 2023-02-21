import { useEffect } from 'react';
import { useRouter } from 'next/router';

export default function Home() {
    const router = useRouter();

    // useEffect(() => {
    //     if (localStorage.getItem('User')) {
    //         router.push({
    //             pathname: '/environment'
    //         })
    //     }
    // })
    // return (
    //     <>
    //         <button>
    //             <a
    //                 className="login-link"
    //                 href={`https://github.com/login/oauth/authorize?scope=user repo&client_id=${process.env.GITHUB_CLIENT_ID}`}
    //             >Github Login</a>
    //         </button>
    //     </>
    // )
    return (
        <>
        </>
    )
}
