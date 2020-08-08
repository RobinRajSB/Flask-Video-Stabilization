from flask import Flask
from flask import Flask, request, jsonify, Response,redirect,url_for,render_template, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from vidstab import VidStab
import matplotlib.pyplot as plt
import os

config = {
    "DEBUG": True
}



app = Flask(__name__, static_folder='static')
# app.register_blueprint(routes)


# tell Flask to use the above defined config
app.config.from_mapping(config)


UPLOAD_FOLDER = './static/Uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 





@app.route('/')
def home():
	return render_template('home.html')



@app.route("/demo")
def demo():
	return render_template('demoo.html')



@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.filename = "file.mp4"
     
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
      
      return redirect(url_for('stabilize'))
      
	


@app.route('/background_process_test')
def background_process_test():
    print ("Hello")
    return ("nothing")


@app.route('/stabilize')
def stabilize():
    stabilize_video()
    return render_template('page.html')


@app.route('/return-files', methods=['GET'])
def return_file():
    return send_from_directory(directory='static/Output', filename='stable_video.avi', as_attachment=True)



def stabilize_video():
    stabilizer = VidStab()
    stabilizer.stabilize(input_path='static/Uploads/file.mp4', output_path='static/Output/stable_video.avi')

    stabilizer.plot_trajectory()
    plt.savefig('static/img/plot_trajectory.png')

    stabilizer.plot_transforms()
    plt.savefig('static/img/plot_transforms.png')
    return ('________________Completed convertion_____________')



if __name__ == '__main__':
    app.run( host='0.0.0.0',port=8080)


