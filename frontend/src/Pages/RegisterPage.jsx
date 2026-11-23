
import {useState} from "react";
import {Link, useNavigate} from "react-router-dom";

function RegisterPage({API_URL}) {

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");

    const navigate = useNavigate();

    async function handleRegister(e) {
        e.preventDefault();

        try {
            const response = await fetch(`${API_URL}/register`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username,
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (response.ok) {
                alert("Registration successful!");
                navigate("/");
            } else {
                setMessage(data.detail || "Registration failed");
            }

        } catch (error) {
            setMessage("Unable to connect to server");
        }
    }

    return (
        <>
            <h1>Staff Registration</h1>

            <form onSubmit={handleRegister}>

                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />

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

                <button type="submit">Register</button>

            </form>

            <p>{message}</p>

            <p>
                Already registered? <Link to="/">Login here</Link>
            </p>
        </>
    );
}

export default RegisterPage;
