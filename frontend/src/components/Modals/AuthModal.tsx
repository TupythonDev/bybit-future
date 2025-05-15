import { useState, Dispatch, SetStateAction } from "react";
import { Modal } from "../Modal";
import { Login } from "../Auth/Login";
import { Register } from "../Auth/Register";
import { AnimatePresence, motion } from "framer-motion"

interface AuthHeaderProps {
    title: string
    description: string
    buttonText: string
    onButtonClick: () => void
}

interface AuthModalProps {
    openAuthModal: boolean
    setAuthModal: Dispatch<SetStateAction<boolean>>
}

export function AuthModal({ openAuthModal, setAuthModal }: AuthModalProps) {
    const [activeComponent, setActiveComponent] = useState<"register" | "login">("register")
    const style: string = "flex flex-col gap-4"

    return (
        <AnimatePresence>
            {openAuthModal && (
                <Modal className="flex flex-col gap-8 border-t-2 border-blue-500 text-white" isOpen={openAuthModal} onClose={() => setAuthModal(false)}>
                    <div className="flex justify-evenly p-2">
                        {activeComponent === "login" ? (
                            <AuthHeader
                                title="Faça login na sua conta."
                                description="Não tem uma conta?"
                                buttonText="Registro"
                                onButtonClick={() => setActiveComponent("register")}
                            />
                        ) : (
                            <AuthHeader
                                title="Crie uma conta de jogo"
                                description="Já possui uma conta?"
                                buttonText="Login"
                                onButtonClick={() => setActiveComponent("login")}
                            />
                        )}
                    </div>
                    <motion.div className="flex-1 flex justify-center">
                        <AnimatePresence mode="wait">
                            {activeComponent === "login" ? (
                                <motion.div
                                    key="login"
                                    initial={{ opacity: 0, x: 50 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    exit={{ opacity: 0, x: -50 }}
                                    transition={{ duration: 0.3 }}
                                    className="w-full"
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
                                    className="w-full"
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

function AuthHeader({ title, description, buttonText, onButtonClick }: AuthHeaderProps) {
    return (
        <div>
            <h1 className="text-4xl">{title}</h1>
            <div className="flex gap-4 items-center">
                <p className="text-white/50 text-xl">{description}</p>
                <button onClick={onButtonClick} className="cursor-pointer text-orange-400 text-2xl">{buttonText}</button>
            </div>
        </div>
    )
}