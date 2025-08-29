import type { SelectMenu_Interface } from "./interface";
import { ChevronDownIcon } from "@heroicons/react/16/solid";

function SelectMenu({ id, label, options, onChange }: SelectMenu_Interface) {
  return (
    <div>
      <label
        htmlFor={id}
        className="block text-sm/6 font-medium text-gray-900 dark:text-white"
      >
        {label}
      </label>
      <div className="mt-2 grid grid-cols-1">
        <select
          id={id}
          name="location"
          defaultValue={options[0]}
          className="hover:cursor-pointer col-start-1 row-start-1 w-full appearance-none rounded-md bg-white py-1.5 pl-3 pr-8 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-indigo-600 sm:text-sm/6 "
          onChange={onChange}
        >
          {options.map((option) => (
            <option className="hover:cursor-pointer" value={option}>
              {option}
            </option>
          ))}
        </select>
        <ChevronDownIcon
          aria-hidden="true"
          className="pointer-events-none hover:cursor-pointer col-start-1 row-start-1 mr-2 size-5 self-center justify-self-end text-gray-500 sm:size-4 dark:text-gray-400"
        />
      </div>
    </div>
  );
}

export { SelectMenu };
