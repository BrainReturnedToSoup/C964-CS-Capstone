export interface SelectMenu_Interface {
    id: string;
    label: string;
    name: string;
    options: string[];
    onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void
}
