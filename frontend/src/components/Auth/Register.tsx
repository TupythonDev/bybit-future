import { useState, FC, ChangeEvent, FormEvent } from "react";

interface FormData {
    name: string
    surname: string
    email: string
    password: string
    phone: string
    cpf: string
    birthday: string
}

interface FormProps {
    className?: string
}

export const Register: FC<FormProps> = ({ className }) => {
    const [formData, setFormData] = useState<FormData>(
        {
            name: "",
            surname: "",
            email: "",
            password: "",
            phone: "",
            cpf: "",
            birthday: "",
        }
    )

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;

        if (name === "birthday") {
            const rawValue = value.replace(/\D/g, "").slice(0, 8)
            let formattedValue = rawValue

            if (rawValue.length > 2) {
                formattedValue = `${rawValue.slice(0, 2)}/${rawValue.slice(2)}`
            }
            if (rawValue.length > 4) {
                formattedValue = `${rawValue.slice(0, 2)}/${rawValue.slice(2, 4)}/${rawValue.slice(4)}`;
            }

            setFormData((prev) => ({ ...prev, [name]: formattedValue }))
        } else if (name === "cpf") {
            const rawValue = value.replace(/\D/g, "").slice(0, 11)
            let formattedValue = rawValue;

            if (rawValue.length > 3) {
                formattedValue = `${rawValue.slice(0, 3)}.${rawValue.slice(3)}`;
            }
            if (rawValue.length > 6) {
                formattedValue = `${rawValue.slice(0, 3)}.${rawValue.slice(3, 6)}.${rawValue.slice(6)}`;
            }
            if (rawValue.length > 9) {
                formattedValue = `${rawValue.slice(0, 3)}.${rawValue.slice(3, 6)}.${rawValue.slice(6, 9)}-${rawValue.slice(9)}`;
            }

            setFormData((prev) => ({ ...prev, [name]: formattedValue }))
        } else if (name === "phone") {
            const rawValue = value.replace(/\D/g, "").slice(0, 11)
            let formattedValue = rawValue;

            if (rawValue.length > 0) {
                formattedValue = `(${rawValue.slice(0, 2)}`;
            }
            if (rawValue.length >= 3) {
                formattedValue += `) ${rawValue.slice(2, 7)}`;
            }
            if (rawValue.length >= 8) {
                formattedValue += `-${rawValue.slice(7)}`;
            }

            setFormData((prev) => ({ ...prev, [name]: formattedValue }))
        } else {
            setFormData((prevFormData) => (
                {
                    ...prevFormData,
                    [name]: value
                }
            ))
        }
    }

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault()
        console.log("Formulario enviado:", formData)
    }

    const formFields = [
        { name: "name", label: "Nome" },
        { name: "surname", label: "Sobrenome" },
        { name: "email", label: "Email" },
        { name: "password", label: "Senha", type: "password" },
        { name: "phone", label: "Telefone", type: "tel" },
        { name: "cpf", label: "CPF" },
        { name: "birthday", label: "Data de Nascimento", type: "text" }
    ]

    return (
        <form className={className} onSubmit={handleSubmit}>
            {formFields.map((field) => (
                <div className="flex flex-col" key={field.name}>
                    <input
                        type={field.type || "text"}
                        id={field.name}
                        name={field.name}
                        value={formData[field.name as keyof FormData]}
                        onChange={handleChange}
                        placeholder={field.label}
                        className="p-2 rounded text-center"
                        required
                    />
                </div>
            ))}
            <button className="cursor-pointer p-2" type="submit">Registrar</button>
        </form>
    )
}