export interface Prediction {
  price_predictions: number[];
  gaussian_noisy_square_feet: number[];
}

export interface PredictionInputs {
  squareFeet: number;
  numOfBedrooms: number;
  numOfBathrooms: number;
  neighborhoodType: string;
}
