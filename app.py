from flask import Flask,render_template,request
import pickle

app=Flask(__name__)

# step 2:loading the saved model
with open("stroke-svc-model.pkl","rb")as file:
    stroke_model=pickle.load(file)
    
with open("lb-smoking.pkl","rb")as file:
    lb_smoke=pickle.load(file)
    
       
# step 3:define a user function
def predict_stroke(gender="Male", age=67.0, hypertension="Yes", heart_disease="Yes", avg_glucose_level=234.46, bmi=75.0, smoking_status="formerly smoked", Residence_type="Urban"):
    lst = []

    # Encode gender
    if gender == 'Male':
        lst.append(1)
    elif gender == 'Female':
        lst.append(0)
    else:  # 'Other'
        lst.append(2)

    lst.append(float(age))

    # Encode hypertension
    lst.append(1 if hypertension == "Yes" else 0)

    # Encode heart disease
    lst.append(1 if heart_disease == "Yes" else 0)

    lst.append(float(avg_glucose_level))
    lst.append(float(bmi))

    # Encode smoking status
    try:
        smoking_encoded = lb_smoke.transform([smoking_status])[0]
    except ValueError as e:
        print(f"Invalid smoking_status: {smoking_status}")
        print("Allowed values are:", lb_smoke.classes_)
        return

    lst.append(smoking_encoded)

    # One-hot encode residence type
    if Residence_type == "Urban":
        lst.extend([0, 1])
    else:  # Rural
        lst.extend([1, 0])

    # Now lst has 9 features
    if len(lst) != 9:
        print("Error: feature list does not have 9 elements.")
        print("Current lst:", lst)
        return

    result = stroke_model.predict([lst])
    print("Raw model output:", result)
    
    if result[0] == 1:
        return "Person is having a stroke"
    else:
        return "Person is not having a stroke"


@app.route("/",methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/contact",methods=["GET"])
def contact():
    return render_template("contact.html")

@app.route("/predict",methods=["GET","POST"])
def predict():
    if request.method=="POST":
        gender=request.form.get("gender")
        age=float(request.form.get("age"))
        hyper=request.form.get("hyper")
        heart=request.form.get("heart")
        glucose=float(request.form.get("glucose"))
        bmi=float(request.form.get("bmi"))
        smoke=request.form.get("smoke")
        residence=request.form.get("residence")
        result=predict_stroke(gender=gender,age=age,hypertension=hyper,heart_disease=heart,avg_glucose_level=glucose,bmi=bmi,smoking_status=smoke,Residence_type=residence)
        return render_template("predict.html",prediction=result)
    return render_template("predict.html")

@app.route("/about",methods=["GET"])
def about():
    return render_template("about.html")


if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0', port=8000)
