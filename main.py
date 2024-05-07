import os
import base64
import html
import random

from flask import Flask, request, session
from model import Message 

app = Flask(__name__)
app.secret_key = '677631026d05fa8a60bd186803779dbbe3c7db0c017dd8b7'

@app.route('/', methods=['GET', 'POST'])
def home():

    # If the session does not include a CSRF token, then add one.
    if 'csrf_token' not in session:
        session['csrf_token'] = str(random.randint(10000000, 99999999))

    if request.method == 'POST':
        if request.form.get('csrf_token') == session['csrf_token']:
            m = Message(content=request.form['content'])
            m.save()

    body = """
<html>
<body>
<h1>Class Message Board</h1>
<h2>Contribute to the Knowledge of Others</h2>
<form method="POST">
    <textarea name="content"></textarea>
    <input type="hidden" name="csrf_token" value="{csrf_token}">
    <input type="submit" value="Submit">
</form>

<h2>Wisdom From Your Fellow Classmates</h2>
""".format(csrf_token=session['csrf_token'])
    
    for m in Message.select():
        escaped_content = html.escape(m.content)
        body += f"""
<div class="message">
{escaped_content}
</div>
"""

    return body 


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

