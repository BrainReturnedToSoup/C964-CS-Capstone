import { useRef, useState } from "react";

import { SelectMenu } from "./components/select/component";
import { InputField } from "./components/input/component";
import { Histogram } from "./components/visualization/histogram/component";

import "./App.css";

function App() {
  const [error, setError] = useState<string | null>(null);

  const [squareFeet, setSquareFeet] = useState<number | null>(null);
  const [numOfBedrooms, setNumOfBedrooms] = useState<number | null>(null);
  const [numOfBathrooms, setNumOfBathrooms] = useState<number | null>(null);
  const [neighborhoodType, setNeighborhoodType] = useState<string | null>(null);

  // square feet input field
  const [isEmpty, setIsEmpty] = useState<boolean>(true);
  const [isValid, setIsValid] = useState<boolean>(false);

  const predictionRequestRef = useRef<Promise<void> | null>(null); // used to prevent rapid click race condition; sidesteps any split hairs of the react rendering lifecycle
  const [predictionIsPending, setPredictionIsPending] =
    useState<boolean>(false); // used as part of disabling the submit button
  const [prediction, setPrediction] = useState<any | null>(null); // the actual prediction data as fetched on submission

  return (
    <div className="flex flex-col items-center">
      <div className="w-[450px] mt-[128px] mb-[64px] col-start-1 row-start-1 appearance-none rounded-md bg-white py-1.5 px-3 text-gray-900 outline-1 -outline-offset-1 outline-gray-300">
        <h1 className="text-center align-middle text-[1.25rem] font-bold text-gray-900 mt-4">
          Housing Price Predictor
        </h1>
        <div>
          {error && (
            <div>
              <p>{error}</p>
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation();

                  setError(null);
                }}
              >
                Close
              </button>
            </div>
          )}
        </div>
        <div>
          <div className="my-2">
            <InputField
              id={"square_feet"}
              name={"square_feet"}
              label={"Square feet"}
              defaultVal={"1000"}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                e.stopPropagation();

                if (e.target.value.length === 0) {
                  setIsEmpty(true);
                  setIsValid(true);
                  return;
                }

                const regex = /^\d+$/; // only whole numbers
                const isValidPattern = regex.test(e.target.value);

                if (!isValidPattern) {
                  setIsEmpty(false);
                  setIsValid(false);
                  return;
                }

                const squareFeet = Number(e.target.value);

                if (squareFeet > 3999) {
                  setIsEmpty(false);
                  setIsValid(false);
                  return;
                }

                setIsEmpty(false);
                setIsValid(true);
                setSquareFeet(Number(e.target.value));
              }}
              isValid={isValid || isEmpty}
              constrainErrorMessage={
                "Invalid input: Should only contain positive whole numbers, and not exceed 3999 ft^2"
              }
              // SquareFeet
            />
          </div>

          <div className="my-2">
            <SelectMenu
              id={"num_of_bedrooms"}
              name={"num_of_bedrooms"}
              label={"Number of bedrooms"}
              options={["2", "3", "4", "5"]}
              onChange={(e: React.ChangeEvent<HTMLSelectElement>) => {
                e.stopPropagation();

                setNumOfBedrooms(Number(e.target.value));
              }}
              // # of bed
            />
          </div>

          <div className="my-2">
            <SelectMenu
              id={"num_of_bathrooms"}
              name={"num_of_bathrooms"}
              label={"Number of bathrooms"}
              options={["1", "2", "3"]}
              onChange={(e: React.ChangeEvent<HTMLSelectElement>) => {
                e.stopPropagation();

                setNumOfBathrooms(Number(e.target.value));
              }}
              // # of bath
            />
          </div>

          <div className="my-2">
            <SelectMenu
              id={"neighborhood_type"}
              name={"neighborhood_type"}
              label={"Neighborhood type"}
              options={["Rural", "Suburb", "Urban"]}
              onChange={(e: React.ChangeEvent<HTMLSelectElement>) => {
                e.stopPropagation();

                setNeighborhoodType(e.target.value);
              }}
              // # neighborhood type
            />
          </div>

          <div className="my-4 flex justify-center items-center">
            <button
              disabled={isEmpty || !isValid || predictionIsPending}
              className="hover:cursor-pointer col-start-1 row-start-1 text-xl w-fit align-middle text-center appearance-none rounded-md bg-white active:bg-gray-100 py-1.5 px-3  text-gray-900 outline-1 -outline-offset-1 outline-gray-300"
              type="button"
              onClick={(e) => {
                e.stopPropagation();

                if (!predictionRequestRef.current) {
                  predictionRequestRef.current = fetch("/predict", {
                    method: "POST",
                    body: JSON.stringify({
                      SquareFeet: squareFeet,
                      Bedrooms: numOfBedrooms,
                      Bathrooms: numOfBathrooms,
                      Neighborhood: neighborhoodType,
                    }),
                  })
                    .then((res) => res.json())
                    .then((data) => {
                      setPrediction(data);
                    })
                    .catch((e: Error) => {
                      setError(e.message);
                    })
                    .finally(() => {
                      predictionRequestRef.current = null;
                      setPredictionIsPending(false);
                    });

                  setPredictionIsPending(true);
                }
              }}
            >
              {"Generate prediction"}
            </button>
          </div>
        </div>
      </div>

      <div className="mb-8">
        {/* {prediction && ( */}
        <>
          <Histogram
            width={700}
            height={450}
            xAxisLabel="Price Range Buckets"
            yAxisLabel="Number of Occurences"
            binInterval={1}
            data={[1, 1, 1, 4, 5, 5, 5, 7, 7, 8]}
            style={"" as React.CSSProperties}
          />
          <Histogram
            width={700}
            height={450}
            xAxisLabel="Price Range Buckets"
            yAxisLabel="Number of Occurences"
            binInterval={1}
            data={[1, 1, 1, 4, 5, 5, 5, 7, 7, 8]}
            style={"" as React.CSSProperties}
          />
        </>
      </div>
    </div>
  );
}

export default App;
