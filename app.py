from flask import Flask, request, render_template
import pickle
import numpy as np


app = Flask(__name__)


# ==========================
# Load Model and Scaler
# ==========================

model = pickle.load(
    open("models/svm_model.pkl", "rb")
)


scaler = pickle.load(
    open("models/scaler.pkl", "rb")
)



# ==========================
# Home Route
# ==========================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )




# ==========================
# Prediction Route
# ==========================

@app.route("/predict", methods=["POST"])
def predict():

    try:


        feature_names = [

            "mean_radius",
            "mean_texture",
            "mean_perimeter",
            "mean_area",
            "mean_smoothness",
            "mean_compactness",
            "mean_concavity",
            "mean_concave_points",
            "mean_symmetry",
            "mean_fractal_dimension",

            "radius_error",
            "texture_error",
            "perimeter_error",
            "area_error",
            "smoothness_error",
            "compactness_error",
            "concavity_error",
            "concave_points_error",
            "symmetry_error",
            "fractal_dimension_error",

            "worst_radius",
            "worst_texture",
            "worst_perimeter",
            "worst_area",
            "worst_smoothness",
            "worst_compactness",
            "worst_concavity",
            "worst_concave_points",
            "worst_symmetry",
            "worst_fractal_dimension"

        ]



        values = []


        for feature in feature_names:

            value = request.form.get(feature)

            if value == "" or value is None:

                return render_template(
                    "index.html",
                    error="Please fill all fields"
                )


            values.append(
                float(value)
            )




        input_data = np.array(values).reshape(1,-1)



        # Scaling

        scaled_input = scaler.transform(
            input_data
        )



        # Prediction

        prediction = model.predict(
            scaled_input
        )



        if prediction[0] == 1:

            result = "Benign"

            message = (
                "The model predicts the tumor "
                "as Benign."
            )


        else:

            result = "Malignant"

            message = (
                "The model predicts the tumor "
                "as Malignant."
            )




        return render_template(

            "index.html",

            prediction=result,

            message=message

        )




    except ValueError:


        return render_template(

            "index.html",

            error="Only numerical values are allowed"

        )



    except Exception as e:


        return render_template(

            "index.html",

            error=f"Error: {e}"

        )





if __name__ == "__main__":

    app.run(debug=True)