import numpy as np
from services.predicter.interface import BEDROOMS, BATHROOMS, NEIGHBORHOOD, SQUARE_FEET_RANGE
from services.predicter.static import model_assets

def test_expected_columns():
    expected_columns_x=frozenset(["SquareFeet", "Bedrooms", "Bathrooms", "Neighborhood"])
    expected_columns_y=frozenset(["Price"])
    
    assert frozenset(model_assets.trainX_raw_df.columns) == expected_columns_x
    assert frozenset(model_assets.trainX_transformed_df) == expected_columns_x
    assert frozenset(model_assets.trainY_df) == expected_columns_y
    assert frozenset(model_assets.testX_raw_df.columns) == expected_columns_x
    assert frozenset(model_assets.testX_transformed_df) == expected_columns_x
    assert frozenset(model_assets.testY_df) == expected_columns_y

def test_bedrooms_unique():
    unique_bedrooms_dataset=model_assets.dataset_df["Bedrooms"].unique()
    unique_bedrooms_trainX_raw=model_assets.trainX_raw_df["Bedrooms"].unique()
    unique_bedrooms_trainX_transformed=model_assets.trainX_transformed_df["Bedrooms"].unique()
    unique_bedrooms_testX_raw=model_assets.testX_raw_df["Bedrooms"].unique()
    unique_bedrooms_testX_transformed=model_assets.testX_transformed_df["Bedrooms"].unique()
    
    assert frozenset(unique_bedrooms_dataset) == BEDROOMS
    assert frozenset(unique_bedrooms_trainX_raw) == BEDROOMS
    assert frozenset(unique_bedrooms_trainX_transformed) == BEDROOMS
    assert frozenset(unique_bedrooms_testX_raw) == BEDROOMS
    assert frozenset(unique_bedrooms_testX_transformed) == BEDROOMS
    
def test_bathrooms_unique():
    unique_bathrooms_dataset=model_assets.dataset_df["Bathrooms"].unique()
    unique_bathrooms_trainX_raw=model_assets.trainX_raw_df["Bathrooms"].unique()
    unique_bathrooms_trainX_transformed=model_assets.trainX_transformed_df["Bathrooms"].unique()
    unique_bathrooms_testX_raw=model_assets.testX_raw_df["Bathrooms"].unique()
    unique_bathrooms_testX_transformed=model_assets.testX_transformed_df["Bathrooms"].unique()

    assert frozenset(unique_bathrooms_dataset) == BATHROOMS
    assert frozenset(unique_bathrooms_trainX_raw) == BATHROOMS
    assert frozenset(unique_bathrooms_trainX_transformed) == BATHROOMS
    assert frozenset(unique_bathrooms_testX_raw) == BATHROOMS
    assert frozenset(unique_bathrooms_testX_transformed) == BATHROOMS
    
def test_neighborhoods_unique():
    unique_neighborhoods_dataset=model_assets.dataset_df["Neighborhood"].unique()
    unique_neighborhoods_trainX_raw=model_assets.trainX_raw_df["Neighborhood"].unique()
    unique_neighborhoods_trainX_transformed=model_assets.trainX_transformed_df["Neighborhood"].unique()
    unique_neighborhoods_testX_raw=model_assets.testX_raw_df["Neighborhood"].unique()
    unique_neighborhoods_testX_transformed=model_assets.testX_transformed_df["Neighborhood"].unique()
    
    assert frozenset(unique_neighborhoods_dataset) == frozenset(NEIGHBORHOOD.keys())
    assert frozenset(unique_neighborhoods_trainX_raw) == frozenset(NEIGHBORHOOD.keys())
    assert frozenset(unique_neighborhoods_trainX_transformed) == frozenset(NEIGHBORHOOD.values())
    assert frozenset(unique_neighborhoods_testX_raw) == frozenset(NEIGHBORHOOD.keys())
    assert frozenset(unique_neighborhoods_testX_transformed) == frozenset(NEIGHBORHOOD.values())

def test_neighborhoods_mapping():
    premapped_neighborhoods_train=model_assets.trainX_transformed_df["Neighborhood"]
    mapped_neighborhoods_train=model_assets.trainX_raw_df["Neighborhood"].map(NEIGHBORHOOD)
    
    assert list(premapped_neighborhoods_train) == list(mapped_neighborhoods_train)
    
    premapped_neighborhoods_test=model_assets.testX_transformed_df["Neighborhood"]
    mapped_neighborhoods_test=model_assets.testX_raw_df["Neighborhood"].map(NEIGHBORHOOD)
    
    assert list(premapped_neighborhoods_test) == list(mapped_neighborhoods_test)
    
def test_square_feet_range():
    min=model_assets.dataset_df["SquareFeet"].min()
    max=model_assets.dataset_df["SquareFeet"].max()
    
    assert min == SQUARE_FEET_RANGE[0]
    assert max == SQUARE_FEET_RANGE[1]
    
def test_scaler():
    scaler=model_assets.prefit_scaler

    first_sample_unscaled=[[model_assets.trainX_raw_df["SquareFeet"].iloc[0]]]
    first_sample_prescaled=[[model_assets.trainX_transformed_df["SquareFeet"].iloc[0]]]
    first_sample_scaled=scaler.transform(first_sample_unscaled)
        
    assert np.isclose(first_sample_scaled, first_sample_prescaled)
        
    second_sample_unscaled=[[model_assets.trainX_raw_df["SquareFeet"].iloc[1]]]
    second_sample_prescaled=[[model_assets.trainX_transformed_df["SquareFeet"].iloc[1]]]
    second_sample_scaled=scaler.transform(second_sample_unscaled)
    
    assert np.isclose(second_sample_scaled, second_sample_prescaled)
    
    
    