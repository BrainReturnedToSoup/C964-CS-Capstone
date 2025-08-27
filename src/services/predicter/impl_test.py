import numpy as np
from .static import model_assets
from custom_logging.instance import logger
from .impl import Predicter
from .preprocessor import Preprocessor

def test_validate_input():
    pass

def test_predict():
    preprocessor=Preprocessor(logger=logger, prefit_scaler=model_assets.prefit_scaler, columns=model_assets.pretrained_gradient_boosted_regressor.feature_names_in_)
    predicter=Predicter(logger=logger, pretrained_model=model_assets.pretrained_gradient_boosted_regressor, preprocessor=preprocessor)
    
    testX_subset=model_assets.testX_raw_df.iloc[0:50]
    testY_subset=model_assets.testY_df.iloc[0:50]
    deltasY_subset=list(model_assets.deltasY)[0:50]

    # now, grab each sample, and make a mock input from such sample. The predictor then predicts on these mock inputs
    # and the predictions are consolidated back to then be compared to deltas already made in Google Collab.
    for i in range(0,50):
        sample=testX_subset.iloc[i]
        
        print(sample["Neighborhood"])
        
        input={
            "Bathrooms": sample["Bathrooms"],
            "SquareFeet": sample["SquareFeet"],
            "Bedrooms": sample["Bedrooms"],
            "Neighborhood": sample["Neighborhood"]
        }
        
        prediction=predicter.predict(input)
        delta=testY_subset.iloc[i].values[0]-prediction["price_prediction"]
        assert np.isclose(delta, deltasY_subset[i])
    
    