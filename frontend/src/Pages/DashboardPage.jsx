
import {useState, useEffect} from "react";
import {useNavigate} from "react-router-dom";

function DashboardPage({API_URL}) {

    const [visitors, setVisitors] = useState([]);
    const [message, setMessage] = useState("");

    const navigate = useNavigate();

    function logout() {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");

        navigate("/");
    }

    async function refreshToken() {

        const refresh_token = localStorage.getItem("refresh_token");

        if (!refresh_token) {
            logout();
            return false;
        }

        try {
            const response = await fetch(`${API_URL}/refresh`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    refresh_token: refresh_token
                })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem("access_token", data.access_token);
                return true;
            }

            logout();
            return false;

        } catch (error) {
            setMessage("Unable to refresh login session");
            return false;
        }
    }

    async function loadVisitors() {

        let access_token = localStorage.getItem("access_token");

        if (!access_token) {
            logout();
            return;
        }

        try {
            let response = await fetch(`${API_URL}/visitors`, {
                headers: {
                    "token": access_token
                }
            });

            if (response.status === 401) {

                const refreshed = await refreshToken();

                if (!refreshed) {
                    return;
                }

                access_token = localStorage.getItem("access_token");

                response = await fetch(`${API_URL}/visitors`, {
                    headers: {
                        "token": access_token
                    }
                });
            }

            const data = await response.json();

            if (response.ok) {
                setVisitors(data);
                setMessage("");
            } else {
                setMessage(data.detail || "Unable to load visitors");
            }

        } catch (error) {
            setMessage("Unable to connect to server");
        }
    }

    useEffect(() => {
        loadVisitors();
    }, []);

    return (
        <>
            <h1>Visitor Dashboard</h1>

            <button onClick={logout}>Logout</button>

            <h2>Visitor Records</h2>

            {message && <p>{message}</p>}

            {!message && visitors.length === 0 && (
                <p>No visitor records found.</p>
            )}

            {visitors.length > 0 && (
                <table border="1" cellPadding="10">

                    <thead>
                        <tr>
                            <th>Visitor Name</th>
                            <th>Student Name</th>
                            <th>Room Number</th>
                            <th>Purpose</th>
                            <th>Visit Date</th>
                        </tr>
                    </thead>

                    <tbody>
                        {visitors.map((visitor) => (
                            <tr key={visitor.id}>
                                <td>{visitor.visitor_name}</td>
                                <td>{visitor.student_name}</td>
                                <td>{visitor.room_no}</td>
                                <td>{visitor.purpose}</td>
                                <td>{visitor.visit_date}</td>
                            </tr>
                        ))}
                    </tbody>

                </table>
            )}
        </>
    );
}

export default DashboardPage;
