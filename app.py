from flask import Flask, render_template, request
from load_package import calculate_topsis
import os
from werkzeug.utils import secure_filename
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
#hi
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['RESULT_FOLDER'] = './results'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Handle file upload and process TOPSIS."""
    try:
        # Retrieve file and form data
        file = request.files['file']
        weights = request.form['weights']
        impacts = request.form['impacts']
        email = request.form['email']

        if not file:
            return "Please upload a valid file."

        # Save uploaded file
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        # Generate result file path
        result_filename = 'result.csv'
        result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)

        # Run the TOPSIS method
        calculate_topsis(input_path, weights, impacts, result_path)

        # Send the result via email
        send_email(email, result_path)

        return "File processed and result sent to your email!"
    except Exception as e:
        return f"An error occurred: {e}"

def send_email(to_email, file_path):
    """Send the result file via email."""
    from_email = 'pjain_be22@thapar.edu'  # Replace with your email
    password = ''     # Replace with your email password

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'TOPSIS Result File'

    body = 'Please find attached the result of your TOPSIS analysis.'
    msg.attach(MIMEText(body, 'plain'))

    # Attach the result file
    with open(file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={os.path.basename(file_path)}',
        )
        msg.attach(part)

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)

if __name__ == '__main__':
    app.run(debug=True)
