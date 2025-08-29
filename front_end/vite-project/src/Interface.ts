export interface Predictions {
  price_predictions: number[];
  gaussian_noisy_square_feet: number[];
}

export interface PredictionsInputs {
  squareFeet: number;
  numOfBedrooms: number;
  numOfBathrooms: number;
  neighborhoodType: string;
}
