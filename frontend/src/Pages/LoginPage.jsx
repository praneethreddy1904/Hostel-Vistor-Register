
import {useState} from "react";
import {Link, useNavigate} from "react-router-dom";

function LoginPage({API_URL}) {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");

    const navigate = useNavigate();

    async function handleLogin(e) {
        e.preventDefault();

        try {
            const response = await fetch(`${API_URL}/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: "",
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem("access_token", data.access_token);
                localStorage.setItem("refresh_token", data.refresh_token);

                navigate("/dashboard");
            } else {
                setMessage(data.detail || "Invalid email or password");
            }

        } catch (error) {
            setMessage("Unable to connect to server");
        }
    }

    return (
        <>
            <h1>Staff Login</h1>

            <form onSubmit={handleLogin}>

                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                <button type="submit">Login</button>

            </form>

            <p>{message}</p>

            <p>
                New staff? <Link to="/register">Register here</Link>
            </p>
        </>
    );
}

export default LoginPage;
