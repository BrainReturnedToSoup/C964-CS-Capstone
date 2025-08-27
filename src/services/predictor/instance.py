from custom_logging.instance import logger
from .static import model_assets
from .preprocessor import Preprocessor
from .impl import Predictor

preprocessor=Preprocessor(logger=logger, prefit_scaler=model_assets.prefit_scaler, columns=model_assets.pretrained_gradient_boosted_regressor.feature_names_in_)
predictor=Predictor(logger=logger, pretrained_model=model_assets.pretrained_gradient_boosted_regressor, preprocessor=preprocessor)