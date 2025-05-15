import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Header } from "./components/Header";

export function App() {
    return (
        <div className="bg-gradient-to-b from-gray-800 to-gray-900 min-h-screen">
            <BrowserRouter>
                <Header />
                <main >
                    <Routes>
                        <Route path="/" element={""} />
                        <Route path="/order-placer" element={""} />
                    </Routes>
                </main >
            </BrowserRouter>
        </div>
    )
}