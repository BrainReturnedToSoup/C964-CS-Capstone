from back_end.static.model_assets.loader.instance import MODEL_ASSETS

# declaring a local reference 'model_assets' so that the
# predictor depends on 'model_assets' rather than 'MODEL_ASSETS' directly.
# By doing this, 'model_assets' can be tested on an expected API within the 'predictor'
# module, while the real structure of 'MODEL_ASSETS' can change.

model_assets=MODEL_ASSETS