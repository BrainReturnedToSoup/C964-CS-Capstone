import type { Input_Interface } from "./interface";
import { ExclamationCircleIcon } from "@heroicons/react/16/solid";

function InputField({
  id,
  label,
  name,
  defaultVal,
  isValid,
  constrainErrorMessage,
  onChange,
}: Input_Interface) {
  return (
    <div>
      <label
        htmlFor={id}
        className="block text-sm/6 font-medium text-gray-900 dark:text-white"
      >
        {label}
      </label>
      <div className="mt-2 grid grid-cols-1">
        <input
          defaultValue={defaultVal}
          id={id}
          name={name}
          type="text"
          placeholder={defaultVal}
          aria-invalid={!isValid}
          aria-describedby="email-error"
          className={`col-start-1 row-start-1 block w-full rounded-md bg-white py-1.5 pl-3 pr-10 ${
            !isValid
              ? "text-red-900 outline-red-400 placeholder:text-red-300  focus-visible:outline-2 focus-visible:-outline-offset-2"
              : "text-gray-900 outline-gray-300 focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-indigo-600"
          } outline-1 -outline-offset-1 focus:outline-[1.5px]  `}
          onChange={onChange}
        />

        {!isValid && (
          <ExclamationCircleIcon
            aria-hidden="true"
            className="pointer-events-none col-start-1 row-start-1 mr-3 size-5 self-center justify-self-end text-red-500 sm:size-4 dark:text-red-400"
          />
        )}
      </div>
      {!isValid && (
        <p
          id={`${id}-error`}
          className="mt-2 text-sm text-red-600 dark:text-red-400"
        >
          {constrainErrorMessage}
        </p>
      )}
    </div>
  );
}

export { InputField };
