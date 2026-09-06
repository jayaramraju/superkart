
import streamlit as st
import pandas as pd
import requests


# ============================================================
# Page configuration
# ============================================================

st.set_page_config(
    page_title="SuperKart Sales Predictor",
    page_icon="🛒",
    layout="centered"
)


# ============================================================
# Title
# ============================================================

st.title("SuperKart Sales Predictor")


# ============================================================
# Backend URL
# ============================================================

BACKEND_URL = "https://jrr070226-superkart-backend-jayaram.hf.space"


# ============================================================
# Online Prediction
# ============================================================

st.subheader("Online Prediction")


# ------------------------------------------------------------
# Collect business input
# ------------------------------------------------------------

product_weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    max_value=100.0,
    step=0.1
)

product_sugar_content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "No Sugar", "Regular"]
)

product_type = st.selectbox(
    "Product Type",
    ["Perishable", "Non Perishable"]
)

product_allocated_area = st.number_input(
    "Product Allocated Area",
    min_value=0.000,
    max_value=0.300,
    step=0.001
)

product_mrp = st.number_input(
    "Product MRP",
    min_value=0.00,
    max_value=1000.00,
    step=0.1
)

store_size = st.selectbox(
    "Store Size",
    ["Small", "Medium", "High"]
)

store_id = st.selectbox(
    "Store Id",
    ["OUT001", "OUT002", "OUT003", "OUT004"]
)

store_location_city_type = st.selectbox(
    "Store Location City Type",
    ["Tier 1", "Tier 2", "Tier 3"]
)

store_type = st.selectbox(
    "Store Type",
    [
        "Departmental Store",
        "Food Mart",
        "Supermarket Type1",
        "Supermarket Type2"
    ]
)

store_current_age = st.number_input(
    "Store Current Age",
    min_value=0,
    max_value=100,
    step=1
)


# ============================================================
# Create DataFrame
# ============================================================

business_df = pd.DataFrame({
    "product_weight": [product_weight],
    "product_sugar_content": [product_sugar_content],
    "product_type": [product_type],
    "product_allocated_area": [product_allocated_area],
    "product_mrp": [product_mrp],
    "store_size": [store_size],
    "store_id": [store_id],
    "store_location_city_type": [store_location_city_type],
    "store_type": [store_type],
    "store_current_age": [store_current_age]
})


# ============================================================
# Online Prediction Button
# ============================================================

if st.button("Predict"):

    backend_url = f"{BACKEND_URL}/v1/predict"

    try:

        response = requests.post(
            backend_url,
            json=business_df.to_dict(orient="records")[0],
            timeout=60
        )

        response.raise_for_status()

        data = response.json()


        if "prediction" in data:

            prediction = data["prediction"][0]

            st.success(
                f"Predicted Sales: {prediction:.2f}"
            )

        else:

            st.error(
                f"'prediction' key not found. Response: {data}"
            )


    except requests.exceptions.RequestException as e:

        st.error(
            f"Error making prediction: {e}"
        )


# ============================================================
# Show input data
# ============================================================

with st.expander("View Input Data"):

    st.dataframe(business_df)


# ============================================================
# Batch Prediction
# ============================================================

st.subheader("Batch Prediction")


uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)


# ============================================================
# Batch Prediction Button
# ============================================================

if uploaded_file is not None:

    if st.button("Predict Batch"):

        backend_url = f"{BACKEND_URL}/v1/batch_predict"

        try:

            response = requests.post(
                backend_url,
                files={
                    "file": uploaded_file
                },
                timeout=120
            )

            response.raise_for_status()

            predictions = response.json()


            st.success(
                "Batch predictions completed!"
            )

            st.write(predictions)


        except requests.exceptions.RequestException as e:

            st.error(
                f"Error making batch prediction: {e}"
            )
