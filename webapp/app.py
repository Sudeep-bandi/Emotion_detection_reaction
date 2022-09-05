#
#   Main driver code for the Flask based web app on a localhost
#   created by Ronja Rehm and Jan Kühlborn
#
###################################################################################

from flask import Flask, render_template, Response, make_response, send_file, send_from_directory
import audio_recognizer
import audio_recognizer8
import json
import video_recognizer
import os
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

app = Flask(__name__, static_folder='static')
global audio_emotion
global audio_emotion_8
global multi_emotion


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(video_recognizer.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/audio')
def audio():
    return render_template('audio.html', data='test')


@app.route('/audio8')
def audio8():
    return render_template('audio_8emotions.html', data='test')


@app.route('/Video')
def Video():
    return render_template('Video.html')


@app.route('/multimodal')
def multimodal():

    return render_template('multimodal.html', )


@app.route('/live-data')
def live_data():
    # echo audio predictions as JSON
    global audio_emotion
    data = audio_recognizer.analyze_audio()
    audio_emotion = data
    response = make_response(json.dumps(data.tolist()))
    response.content_type = 'application/json'
    return response

@app.route('/live-data8')
def live_data8():
    # echo audio predictions as JSON
    global audio_emotion_8
    data = audio_recognizer8.analyze_audio()
    audio_emotion_8 = data
    response = make_response(json.dumps(data.tolist()))
    response.content_type = 'application/json'
    return response


@app.route('/live-data_video')
def live_data_video():
    # Create a PHP array and echo it as JSON
    f = open('video_prediction.json')
    data = json.load(f)
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


@app.route('/live-data_multi')
def live_data_multi():
    # Create a PHP array and echo it as JSON
    global multi_emotion
    f = open('video_prediction.json')
    data = json.load(f)
    data2 = audio_recognizer.analyze_audio()


    newdict = [{"name": "Video",
                "data": [{"name": "Angry", "value": round(data[0] * 100, 2)},
                         {"name": "Fear", "value": round(data[1] * 100, 2)},
                         {"name": "Happy", "value": round(data[2] * 100, 2)},
                         {"name": "Sad", "value": round(data[3] * 100, 2)}]},
               {"name": "Audio",
                "data": [{"name": "Angry", "value": round(data2[0] * 100, 2)},
                         {"name": "Fear", "value": round(data2[1] * 100, 2)},
                         {"name": "Happy", "value": round(data2[2] * 100, 2)},
                         {"name": "Sad", "value": round(data2[3] * 100, 2)}]}]

    print(newdict)

    data3 = []
    data = np.array(data)
    for index in range(len(data2)):
        print(index)
        data3.append(0.7 * data[index] + 0.3 * data2[index])
    multi_emotion = data3

    response = make_response(json.dumps(newdict))
    response.content_type = 'application/json'
    return response


@app.route('/spectrogram')
def spectrogram():
    return send_file('diagrams\\MelSpec.png', mimetype='image/png')


@app.route('/waveplot')
def waveplot():
    return send_file('diagrams\\Waveplot.png', mimetype='image/png')


@app.route('/emotion')
def emotion():
    try:
        data = audio_emotion
    except NameError:
        data = [0.0, 0.0, 0.0, 0.0]
    print('audio array: ', data)
    if np.argmax(data) == 0:
        return send_file('static\\images\\angry.png', mimetype='image/jpg')
    elif np.argmax(data) == 1:
        return send_file('static\\images\\fear.jpg', mimetype='image/jpg')
    elif np.argmax(data) == 2:
        return send_file('static\\images\\happy.jpg', mimetype='image/jpg')
    elif np.argmax(data) == 3:
        return send_file('static\\images\\sad.png', mimetype='image/png')
    else:
        return send_file('static\\images\\blank.png', mimetype='image/jpg')


@app.route('/emotion8')
def emotion8():
    try:
        data = audio_emotion_8
    except NameError:
        data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    print('audio array: ', data)
    if np.argmax(data) == 0:
        return send_file('static\\images\\angry.png', mimetype='image/jpg')
    elif np.argmax(data) == 3:
        return send_file('static\\images\\fear.jpg', mimetype='image/jpg')
    elif np.argmax(data) == 4:
        return send_file('static\\images\\happy.jpg', mimetype='image/jpg')
    elif np.argmax(data) == 6:
        return send_file('static\\images\\sad.png', mimetype='image/png')
    elif np.argmax(data) == 1:
        return send_file('static\\images\\calm.jpg', mimetype='image/jpg')
    elif np.argmax(data) == 2:
        return send_file('static\\images\\disgust.jpg', mimetype='image/jpg')
    elif np.argmax(data) == 5:
        return send_file('static\\images\\neutral.png', mimetype='image/png')
    elif np.argmax(data) == 7:
        return send_file('static\\images\\surprise.png', mimetype='image/png')
    else:
        return send_file('static\\images\\blank.png', mimetype='image/jpg')


@app.route('/multi_emotion')
def multi_emotion():
    try:
        data = multi_emotion
    except NameError:
        data = [0.0, 0.0, 0.0, 0.0]
    print('multi array: ', data)
    if np.argmax(data) == 0:
        return send_file('static\\images\\angry.png', mimetype='image/jpg')
    elif np.argmax(data) == 1:
        return send_file('static\\images\\fear.jpg', mimetype='image/jpg')
    elif np.argmax(data) == 2:
        return send_file('static\\images\\happy.jpg', mimetype='image/jpg')
    elif np.argmax(data) == 3:
        return send_file('static\\images\\sad.png', mimetype='image/png')
    else:
        return send_file('static\\images\\blank.png', mimetype='image/jpg')


if __name__ == '__main__':
    app.run(debug=True)
