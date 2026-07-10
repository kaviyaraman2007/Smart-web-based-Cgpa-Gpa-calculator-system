
# ===========================================
# SMART LOAN APPROVAL SYSTEM
# ===========================================

import pandas as pd
import numpy as np
import joblib


# ===========================================
# DATA MANAGEMENT
# ===========================================

class DataManagement:

    def receive_input(self):

        print(
"\n===== Applicant Details ====="
)

        applicant = {

    "ApplicantName": input("Applicant Name: "),
    "Age": int(input("Age: ")),
    "Mobile": input("Mobile Number: "),
    "Email": input("Email: "),

    "Gender": input("Gender (Male/Female): "),
    "Married": input("Married (Yes/No): "),
    "Dependents": int(input("Dependents: ")),
    "Education": input("Education (Graduate/Not Graduate): "),
    "Self_Employed": input("Self Employed (Yes/No): "),
    "ApplicantIncome": float(input("Applicant Income: ")),
    "CoapplicantIncome": float(input("Coapplicant Income: ")),
    "LoanAmount": float(input("Loan Amount: ")),
    "Loan_Amount_Term": float(input("Loan Term: ")),
    "Credit_History": int(input("Credit History (1/0): ")),
    "Property_Area": input("Property Area (Urban/Semiurban/Rural) : ")




        }

        return applicant


    def _get_int_input(self, prompt, field_name):
        while True:
            try:
                value = int(input(prompt))
                return value
            except ValueError:
                print(f"Invalid input for {field_name}. Please enter an integer.")


    def _get_float_input(self, prompt, field_name):
        while True:
            try:
                value = float(input(prompt))
                return value
            except ValueError:
                print(f"Invalid input for {field_name}. Please enter a number.")


    def validate_data(self, applicant):
      if applicant["ApplicantIncome"] <= 0:
          print("Invalid Applicant Income")
          return False

      if applicant["LoanAmount"] <= 0:
          print("Invalid Loan Amount")
          return False

      if applicant["Age"] < 18:
          print("Applicant must be at least 18 years old.")
          return False

      if len(applicant["Mobile"]) != 10:
          print("Invalid Mobile Number")
          return False

      if "@" not in applicant["Email"]:
          print("Invalid Email Address")
          return False

      if applicant["Loan_Amount_Term"] <= 0:
          print("Invalid Loan Term")
          return False

      if applicant["Credit_History"] not in [0, 1]:
          print("Invalid Credit History")
          return False

      return True


    def preprocess_data(self, applicant):

        print("\nPreprocessing Data...")

        # Encoding Example
        gender = 1 if applicant["Gender"] == "Male" else 0
        married = 1 if applicant["Married"] == "Yes" else 0
        education = 1 if applicant["Education"] == "Graduate" else 0
        employed = 1 if applicant["Self_Employed"] == "Yes" else 0
        credit = applicant["Credit_History"]

        property_area = {

            "Urban":2,
            "Semiurban":1,
            "Rural":0

        }.get(applicant["Property_Area"],0)

        features = np.array([[

            gender,
            married,
            applicant["Dependents"],
            education,
            employed,
            applicant["ApplicantIncome"],
            applicant["CoapplicantIncome"],
            applicant["LoanAmount"],
            applicant["Loan_Amount_Term"],
            credit,
            property_area

        ]])

        return features


# ===========================================
# MACHINE LEARNING (Dummy Model)
# ===========================================


class MachineLearning:

    def load_model(self):

        print("\nLoading Dummy Model...")

        # No trained model, using rule-based dummy model
        model = "Dummy Loan Model"

        return model


    def predict_loan(self, model, data):

        print("\nRunning Loan Prediction...")

        applicant_income = data[0][5]
        loan_amount = data[0][7]
        credit_history = data[0][9]

        # Dummy ML decision rules

        if (
            credit_history == 1
            and applicant_income >= 30000
            and loan_amount <= 500000
        ):

            return [1]       # Approved

        else:

            return [0]       # Rejected



    def confidence(self, model, data):

        applicant_income = data[0][5]
        credit_history = data[0][9]

        # Dummy confidence calculation

        if credit_history == 1 and applicant_income >= 30000:

            return 94.75     # High confidence

        else:

            return 68.50     # Low confidence

# ===========================================
# RESULT MANAGEMENT
# ===========================================

class ResultManagement:


    def display_result(self, applicant, prediction, confidence):

        print("\n==============================")
        print("       LOAN APPROVAL RESULT")
        print("==============================")


        print("Applicant Name :", applicant["ApplicantName"])
        print("Mobile Number  :", applicant["Mobile"])
        print("Email          :", applicant["Email"])


        if prediction[0] == 1:

            print("\nLoan Status : APPROVED")
            print("Message     : Congratulations! Your loan is approved.")

        else:

            print("\nLoan Status : REJECTED")
            print("Message     : Sorry! Your loan application is rejected.")


        print("Confidence    :", round(confidence,2), "%")

        print("==============================")



    def save_prediction(self, applicant, prediction, confidence):

        result = {

            "ApplicantName": applicant["ApplicantName"],

            "Mobile": applicant["Mobile"],

            "Email": applicant["Email"],

            "Prediction":
                "APPROVED" if prediction[0] == 1 else "REJECTED",

            "Confidence":
                round(confidence,2)

        }


        df = pd.DataFrame([result])


        df.to_csv(
            "prediction_history.csv",
            mode="a",
            index=False,
            header=False
        )


        print("\nPrediction Saved Successfully!")


# ===========================================
# MAIN
# ===========================================

class SmartLoanSystem:

    def __init__(self):

        self.data = DataManagement()

        self.ml = MachineLearning()

        self.result = ResultManagement()


    def run(self):

        applicant = self.data.receive_input()

        if self.data.validate_data(applicant):

            processed = self.data.preprocess_data(applicant)

            model = self.ml.load_model()

            prediction = self.ml.predict_loan(model,
                                              processed)

            confidence = self.ml.confidence(model,
                                            processed)

            self.result.display_result(applicant,prediction,
                                       confidence)

            self.result.save_prediction(applicant,prediction,
                                        confidence)

        else:

            print("Application Cancelled")



# ===========================================
# START PROGRAM
# ===========================================

if __name__ == "__main__":

    system = SmartLoanSystem()

    system.run()
