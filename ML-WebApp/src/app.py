import numpy as np
from joblib import load
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

import uuid

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    request_type_str = request.method
    if request_type_str == 'GET':
        return render_template('index.html', href='static/base.svg')
    else:
        text = request.form['text']
        random_str = uuid.uuid4().hex
        path = f'static/{random_str}.svg'
        make_picture('AgesAndHeights.pkl', load('model.joblib'), floats_string_to_np_arr(text), path)
        return render_template('index.html', href=path)

def make_picture(training_data_filename, model, new_input_arr, output_file):
    # assert training_data_filename[-1:-5] == '.pkl'
    data = pd.read_pickle(training_data_filename)
    ages = data['Age']
    data = data[ages > 0]
    ages = data['Age']
    heights = data['Height']

    x_new = np.array([range(19)]).reshape(19, 1)
    preds = model.predict(x_new)

    fig = px.scatter(x=ages, y=heights, title='Heights vs Age of people', labels={'x':'Age (years)', 'y':'Height (inches)'})
    fig.add_trace(go.Scatter(x=x_new.reshape(x_new.shape[0]), y=preds, mode='lines', name='Model'))

    new_preds = model.predict(new_input_arr)
    fig.add_trace(go.Scatter(x=new_input_arr.reshape(len(new_input_arr)), y=new_preds, mode='markers', name='New Outputs', marker=dict(color='purple', size=20, line=dict(color='purple', width=2))))
    fig.write_image(output_file, width=800, engine='kaleido')
    fig.show()

def floats_string_to_np_arr(floats_str):
    def is_float(s):
        try:
            float(s)
            return True
        except:
            return False
    floats = [float(x) for x in floats_str.split(',') if is_float(x)]
    return np.array(floats).reshape(len(floats), 1)

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=2022,
        debug=False
    )