export default function Home() {
    return (
        <>
            <button>
                <a
                    className="login-link"
                    href={`https://github.com/login/oauth/authorize?scope=user repo&client_id=${process.env.GITHUB_CLIENT_ID}`}
                >Github Login</a>
            </button>
        </>
    )
}
