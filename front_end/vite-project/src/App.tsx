import { useRef, useState } from "react";

import { SelectMenu } from "./components/select/component";
import { InputField } from "./components/input/component";
import { Histogram } from "./components/visualization/histogram/component";

import type { Predictions, PredictionsInputs } from "./Interface";

import "./App.css";

function App() {
  const [error, setError] = useState<string | null>(null);

  // represent the actual state of the input fields. These are separate to prevent memory thrashing
  // due to constant changing properties. for instance, 'square feet' is typed, and each change would invoke the state setter.
  const [squareFeet, setSquareFeet] = useState<number>(1000);
  const [numOfBedrooms, setNumOfBedrooms] = useState<number>(2);
  const [numOfBathrooms, setNumOfBathrooms] = useState<number>(1);
  const [neighborhoodType, setNeighborhoodType] = useState<string>("Rural");

  // square feet input field constraint validation
  const [isEmpty, setIsEmpty] = useState<boolean>(true); // so that constraint validation doesn't flag in an empty field, while at the same time disabling the submit button
  const [isValid, setIsValid] = useState<boolean>(true); // starts out valid because of the default values

  const predictionRequestRef = useRef<Promise<void> | null>(null); // used to prevent rapid click race condition; sidesteps any split hairs of the react rendering lifecycle
  const [predictionIsPending, setPredictionIsPending] =
    useState<boolean>(false); // used as part of disabling the submit button
  const [prediction, setPrediction] = useState<Predictions | null>(null); // the actual prediction data as fetched on submission

  // the values supplied as part of the prediction above. This holistic rather than separate, because this value is not directly
  // invoked or changed by, say, the user actively typing in the input fields.
  const [predInputs, setPredInputs] = useState<PredictionsInputs | null>(null);

  return (
    <div className="flex flex-col items-center">
      <div className="w-[450px] mt-[128px] mb-[64px] col-start-1 row-start-1 appearance-none rounded-md bg-white py-1.5 px-3 text-gray-900 outline-1 -outline-offset-1 outline-gray-300">
        <h1 className="text-center align-middle text-[1.25rem] font-bold text-gray-900 my-4">
          Housing Price Predictor
        </h1>
        <div>
          {error && (
            <div className="bg-red-200">
              <p className="text-red-500 mb-10 p-2 text-sm">{error}</p>
              <button
                className="hover:cursor-pointer bg-white h-[24px] w-full py-4  flex justify-center items-center border-b-[1px] border-x-[1px] border-gray-300"
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
              disabled={!isValid || predictionIsPending}
              className="hover:cursor-pointer col-start-1 row-start-1 text-xl w-fit align-middle text-center appearance-none rounded-md bg-white active:bg-gray-100 py-1.5 px-3  text-gray-900 outline-1 -outline-offset-1 outline-gray-300"
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                console.log(
                  `Prediction attempted. Field values:squareFeet=${squareFeet}:numOfBedrooms=${numOfBedrooms}:numOfBathrooms=${numOfBathrooms}:neighborhoodType=${neighborhoodType}`
                );

                if (predictionRequestRef.current === null) {
                  predictionRequestRef.current = fetch("/predict", {
                    method: "POST",
                    headers: {
                      "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                      SquareFeet: squareFeet,
                      Bedrooms: numOfBedrooms,
                      Bathrooms: numOfBathrooms,
                      Neighborhood: neighborhoodType,
                    }),
                  })
                    .then((res) => {
                      if (res.ok) return res.json();
                    })
                    .then((data: Predictions) => {
                      console.log(`Received data: ${JSON.stringify(data)}`);

                      setPrediction(data);
                      setPredInputs({
                        squareFeet: squareFeet!,
                        numOfBedrooms: numOfBedrooms!,
                        numOfBathrooms: numOfBathrooms!,
                        neighborhoodType: neighborhoodType!,
                      });
                    })
                    .catch((e: Error) => {
                      setPrediction(null);
                      setPredInputs(null);
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

      <div className="mb-8 flex flex-col items-center justify-center w-[450px] mt-[128px] mb-[64px">
        {prediction && predInputs && (
          <>
            <div className="mb-10 flex flex-col items-center justify-center">
              <h1 className="text-center align-middle text-2xl mb-4">
                Inputs Of Predictions Below
              </h1>
              <ul className="text-sm">
                <li>
                  <span className="font-bold">SquareFeet:</span>{" "}
                  {predInputs.squareFeet} +-50 Gaussian Noise
                </li>
                <li>
                  <span className="font-bold">Number of Bedrooms:</span>{" "}
                  {predInputs!.numOfBedrooms}
                </li>
                <li>
                  <span className="font-bold">Number of Bathrooms:</span>{" "}
                  {predInputs.numOfBathrooms}
                </li>
                <li>
                  <span className="font-bold">Neighborhood Type:</span>{" "}
                  {predInputs.neighborhoodType}
                </li>
              </ul>
            </div>
            <div className="mb-8">
              <h1 className="text-center align-middle text-2xl mb-4">
                Predictions
              </h1>
              <div>
                <h2 className="text-sm font-bold mb-2">Axes Meanings</h2>
                <ul className="text-sm">
                  <li>
                    <span className="font-bold">{'x = "Price Ranges"'}</span>
                    {
                      ' = each space between a tick effectively represents "tick1 <= x < tick2" price range buckets ($)'
                    }
                  </li>
                  <li>
                    <span className="font-bold">
                      {'y = "Number of Examples"'}
                    </span>
                    {
                      " = the number of examples given the bin. The area formed by the bars effectively represents probability of occurence for the given bin."
                    }
                  </li>
                </ul>
              </div>
              <Histogram
                width={700}
                height={450}
                xAxisLabel="Price Ranges ($)"
                yAxisLabel="Number of Examples"
                yNumOfTicks={15}
                xTickLabelInterval={4}
                binInterval={1000}
                data={prediction.price_predictions}
                style={"" as React.CSSProperties}
              />
            </div>
            <div>
              <h1 className="text-center align-middle mb-4 text-2xl">
                Square Feet Uncertainty Range Used
              </h1>
              <p className="text-sm mb-4">
                The prediction uses gradient boosted regression. This method is
                robust, but unfortunately deterministic, as opposed to the
                stochastic nature related to this task. To produce a more
                reliabe prediction, Gaussian noise is applied to the features
                representing continuous data (in this case, square footage) to
                yield a spread of predictions rather than a single prediction.
                This also means submitting the same combination of inputs may
                not yield the same output.
              </p>
              <div>
                <h2 className="text-sm font-bold mb-2">Axes Meanings</h2>
                <ul className="text-sm">
                  <li>
                    <span className="font-bold">
                      {'x = "Square Feet Ranges"'}
                    </span>
                    {
                      ' = each space between a tick effectively represents "tick1 <= x < tick2" square footage buckets.'
                    }
                  </li>
                  <li>
                    <span className="font-bold">
                      {'y = "Number of Examples"'}
                    </span>
                    {
                      " = the number of examples given the bin. The area formed by the bars effectively represents probability of occurence for the given bin."
                    }
                  </li>
                </ul>
              </div>
              <Histogram
                width={700}
                height={550}
                xAxisLabel="Square Feet Ranges"
                yAxisLabel="Number of Examples"
                yNumOfTicks={15}
                xTickLabelInterval={1}
                binInterval={25}
                data={prediction.gaussian_noisy_square_feet}
                style={"" as React.CSSProperties}
              />
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
