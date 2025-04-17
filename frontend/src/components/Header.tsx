interface HeaderProps {
    onAuthClick: () => void;
}

export function Header({ onAuthClick }: HeaderProps) {
    return (
        <header className="bg-gray-900 text-2xl min-h-40 flex items-center justify-between px-8">
            <h1 className="text-7xl">
                <a href="">Bybit PlaceOrder</a>
            </h1>
            <button onClick={onAuthClick} className="hover:text-gray-700 text-2xl cursor-pointer">Login | Register</button>
        </header>
    )
}