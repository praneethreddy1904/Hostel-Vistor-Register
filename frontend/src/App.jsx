import {Routes, Route, Link} from "react-router-dom";

import RegisterPage from "./Pages/RegisterPage.jsx";
import LoginPage from "./Pages/LoginPage.jsx";
import DashboardPage from "./Pages/DashboardPage.jsx";

const API_URL = "http://127.0.0.1:8004";

function App() {
    return (
        <>
            <nav>
                <Link to="/">Login</Link> |
                <Link to="/register"> Register</Link> |
                <Link to="/dashboard"> Dashboard</Link>
            </nav>

            <Routes>
                <Route path="/" element={<LoginPage API_URL={API_URL} />} />
                <Route path="/login" element={<LoginPage API_URL={API_URL} />} />
                <Route path="/register" element={<RegisterPage API_URL={API_URL} />} />
                <Route path="/dashboard" element={<DashboardPage API_URL={API_URL} />} />
                <Route path="*" element={<h1>404 Not Found</h1>} />
            </Routes>
        </>
    );
}

export default App;