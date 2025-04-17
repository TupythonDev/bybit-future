import { FC, ReactNode } from "react";
import { IoCloseCircle } from "react-icons/io5";
import { motion } from "framer-motion";
import clsx from "clsx";

interface ModalProps {
    className?: string;
    isOpen: boolean;
    onClose: () => void;
    children: ReactNode;
}

export const Modal: FC<ModalProps> = ({ className = "", isOpen, onClose, children, }) => {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
            <motion.div
                className={clsx("bg-white rounded-xl shadow-lg p-6 relative max-w-lg w-full", className)} onClick={(e) => e.stopPropagation()}
                layout
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: .2 }}
            >
                <button className="absolute top-2 right-2 text-red-600 hover:text-red-400 text-xl" onClick={onClose}>
                    <IoCloseCircle />
                </button>
                {children}
            </motion.div>
        </div>
    )
}
