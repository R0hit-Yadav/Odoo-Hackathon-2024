from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'limbachiyakrina157@gmail.com'
app.config['MAIL_PASSWORD'] = 'bahj nthc iidw vvxq'

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    recipient = request.form['recipient']
    subject = request.form['subject']
    body = request.form['body']

    msg = Message(subject=subject,
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[recipient])
    msg.body = body

    mail.send(msg)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
