import { useState, ChangeEvent, FormEvent, FC } from "react";

interface FormData {
    email: string;
    password: string;
}

interface FormProps {
    className?: string
}

export const Login: FC<FormProps> = ({ className }) => {
    const [formData, setFormData] = useState<FormData>(
        {
            email: "",
            password: ""
        }
    )

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target
        setFormData((prevFormData) => (
            {
                ...prevFormData,
                [name]: value
            }
        ))
    }

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault()
        console.log("Formulario enviado:", formData)
    }

    const formFields = [
        { name: "email", placeholder: "E-Mail" },
        { name: "password", placeholder: "Senha", type: "password" }
    ]

    return (
        <form className={className} onSubmit={handleSubmit}>
            {formFields.map((field) => (
                <div className="flex flex-col gap-4 rounded border-2 border-green-400" key={field.name}>
                    <input
                        type={field.type || "text"}
                        id={field.name}
                        name={field.name}
                        value={formData[field.name as keyof FormData]}
                        onChange={handleChange}
                        placeholder={field.placeholder}
                        className="p-2 rounded text-center text-xl bg-white/10"
                        required
                    />
                </div>
            ))}
            <button className="cursor-pointer p-2 text-xl text-white/80 font-bold rounded bg-blue-700 hover:bg-blue-700/50" type="submit">Logar</button>
        </form>
    )
}