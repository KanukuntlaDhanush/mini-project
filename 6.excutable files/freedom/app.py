from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

model = joblib.load('model (3).pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/input')
def input_page():
    return render_template('input.html')

@app.route('/predict', methods=['POST'])
def predict():
    pr_rating = request.form['pr_rating']
    cl_rating = request.form['cl_rating']
    total_score = int(request.form['pr_score']) + int(request.form['cl_score'])

    if (pr_rating == '2' or cl_rating == '2') and (70 <= total_score <= 72):
        prediction = 'F'
    elif (pr_rating == '3' and cl_rating == '3') and (70 <= total_score <= 72):
        prediction = 'PF'
    elif (pr_rating == '5' and cl_rating == '5') and (29 <= total_score <= 36):
        prediction = 'PF'
    elif (pr_rating == '6' and cl_rating == '5') and (29 <= total_score <= 36):
        prediction = 'NF'
    elif (pr_rating == '5' and cl_rating == '6') and (29 <= total_score <= 36):
        prediction = 'NF'
    elif total_score > 72:
        prediction = 'F'
    elif total_score < 29:
        prediction = 'NF'
    elif 29 <= total_score <= 72:
        X = [[int(pr_rating), int(cl_rating), int(request.form['pr_score']), int(request.form['cl_score']), total_score]]
        prediction = model.predict(X)[0]
    else:
        prediction = 'Unknown'
    
    return render_template('predict.html', prediction=prediction, total_score=total_score)

if __name__ == "__main__":
    app.run(debug=False)
