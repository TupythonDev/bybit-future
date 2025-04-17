import { useState, Dispatch, SetStateAction } from "react";
import { Modal } from "../Modal";
import { Login } from "../Auth/Login";
import { Register } from "../Auth/Register";
import { AnimatePresence, motion } from "framer-motion"

interface AuthModalProps {
    openAuthModal: boolean
    setAuthModal: Dispatch<SetStateAction<boolean>>
}

export function AuthModal({ openAuthModal, setAuthModal }: AuthModalProps) {
    const [activeComponent, setActiveComponent] = useState<"register" | "login">("register")
    const style: string = "flex flex-col h-full justify-evenly"

    return (
        <AnimatePresence>
            {openAuthModal && (
                <Modal isOpen={openAuthModal} onClose={() => setAuthModal(false)}>
                    <div className="flex justify-evenly p-2">
                        <button onClick={() => setActiveComponent("register")} className="cursor-pointer">Registro</button>
                        <button onClick={() => setActiveComponent("login")} className="cursor-pointer">Login</button>
                    </div>
                    <motion.div className="animar">
                        <AnimatePresence mode="wait">
                            {activeComponent === "login" ? (
                                <motion.div
                                    key="login"
                                    initial={{ opacity: 0, x: 50 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    exit={{ opacity: 0, x: -50 }}
                                    transition={{ duration: 0.3 }}
                                >
                                    <Login className={style} />
                                </motion.div>
                            ) : (
                                <motion.div
                                    key="register"
                                    initial={{ opacity: 0, x: -50 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    exit={{ opacity: 0, x: 50 }}
                                    transition={{ duration: 0.3 }}
                                >
                                    <Register className={style} />
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </motion.div>
                </Modal >
            )}
        </AnimatePresence>
    )
}