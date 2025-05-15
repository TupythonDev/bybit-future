import { useState } from "react";
import { AuthModal } from "./Modals/AuthModal";

export function Header() {
    const [openAuthModal, setAuthModal] = useState(false)

    return (
        <header className="shadow-lg rounded bg-gradient-to-tl from-slate-900 to-slate-800 text-orange-400 min-h-40 flex items-center justify-between px-8">
            <h1 className="text-7xl">
                <a href=""><img src="logo-bybitgenius.png" className="w-96" alt="logo" /></a>
            </h1>
            <button onClick={() => setAuthModal(true)} className="hover:text-gray-700 text-2xl cursor-pointer">Login | Register</button>
            <AuthModal openAuthModal={openAuthModal} setAuthModal={setAuthModal} />
        </header>
    )
}