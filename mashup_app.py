from flask import Flask, render_template, request
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    try:
        singer_name = request.form['singer_name']
        num_videos = int(request.form['num_videos'])
        audio_duration = int(request.form['audio_duration'])
        output_file_name = request.form['output_file_name']
        recipient_email = request.form['recipient_email']  # Add this line to get recipient email

        # Run the script with subprocess
        result = subprocess.run(
            ['python', '102103385.py', singer_name, str(num_videos), str(audio_duration), output_file_name, recipient_email],
            capture_output=True,
            text=True
        )

        # Display the output in the console
        print(result.stdout)

        # Email the result file
        send_email(output_file_name, recipient_email)  # Pass recipient email to send_email

        return 'Script executed successfully! Check your email for the result.'
    except Exception as e:
        return f'An error occurred: {str(e)}'

def send_email(output_file_name, recipient_email):
    # Email configuration
    sender_email = "senderemail@email.com"
    sender_password = "senderpassword"

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email  # Use recipient_email instead of a fixed to_email
    msg['Subject'] = 'Mashup Result'

    # Attach the result file
    attachment = open(f"{output_file_name}.mp3", "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % f"{output_file_name}.mp3")
    msg.attach(part)

    # Connect to Gmail's SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Login to the Gmail account
    server.login(sender_email, sender_password)

    # Send the email
    server.sendmail(sender_email, recipient_email, msg.as_string())  # Use recipient_email instead of a fixed to_email

    # Close the connection
    server.quit()

if __name__ == '__main__':
    app.run(debug=True)
    app.run(debug=True, host='127.0.0.1', port=5001)
