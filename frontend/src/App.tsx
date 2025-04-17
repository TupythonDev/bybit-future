import { useState } from "react";
import { Header } from "./components/Header";
import { AuthModal } from "./components/Modals/AuthModal";


export function App() {
    const [openAuthModal, setAuthModal] = useState(false)

    return (
        <div className="bg-gray-800 min-h-screen">
            <Header onAuthClick={() => setAuthModal(true)} />
            <AuthModal openAuthModal={openAuthModal} setAuthModal={setAuthModal} />
        </div >
    )
}