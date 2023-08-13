
import smtplib
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE
import os

from flask import url_for
 
import datetime
import base64
 
 
class emailSender():
    smtp_server = 'cpanel140.dnscpanel.com'
    smtp_port = 587
    email_address = 'info@codebyateko.com'
    email_password = 'video_GAMER0109#'
    
    currentYear = datetime.datetime.now()
    
    def CompleteRegister(self, email, username, firstName):

        subject = 'TeamBridge | Welcome to TeamGroup!'
        body = ('''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Email Template</title>
                    <style>
                        /* Reset CSS */
                        body, p, h1, h2, h3, h4, h5, h6 \{
                            margin: 0;
                            padding: 0;
                        }
                        body {
                            font-family: Arial, sans-serif;
                            font-size: 14px;
                            line-height: 1.5;
                            color: #333;
                        }
                        /* Container */
                        .container {
                            width: 100%;
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                        }
                        /* Heading */
                        .heading {
                            text-align: center;
                            margin-bottom: 20px;
                        }
                        .heading h1 {
                            font-size: 24px;
                            margin-bottom: 10px;
                        }
                        /* Content */
                        .content {
                            margin-bottom: 20px;
                        }
                        /* Button */
                        .button {
                            display: inline-block;
                            background-color: #007bff;
                            color: #fff;
                            text-decoration: none;
                            padding: 10px 20px;
                            border-radius: 5px;
                        }
                        /* Footer */
                        .footer {
                            text-align: center;
                            color: #777;
                        }
                    </style>
                    <!-- Bootstrap CSS -->
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
                </head>
                <body>''' + f'''
                    <div class="container">
                        <div class="heading">
                            <img src="https://i.imgur.com/XYJG7vg.png" width="150" height="150">
                            <h1>Welcome to TeamGroup!</h1>
                        </div>
                        <div class="content">
                            <p>Hi {firstName},</p>
                            <p>Hope you love our platform.</p>
                            <p>You should now login using your username @{username}</p>
                            <p>Don't forget to join your company or just create one!.</p>
                        </div>
                        <div class="footer">
                            <p>&copy; {emailSender.currentYear.year} TeamGroup. All rights reserved.</p>
                        </div>
                    </div>
                </body>
                </html>

                ''')
        
        msg = MIMEMultipart()
        msg['From'] = emailSender.email_address
        msg['To'] = email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))


        with smtplib.SMTP(emailSender.smtp_server, emailSender.smtp_port) as server:
            server.starttls()
            server.login(emailSender.email_address, emailSender.email_password)
            server.send_message(msg)
        
        print(f'Email sent successfully to {email}!')
        
        
    def sendRecoveryPassword(self, user):

        subject = 'TeamBridge | Password Recovery'
        body = ('''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Email Template</title>
                    <style>
                        /* Reset CSS */
                        body, p, h1, h2, h3, h4, h5, h6 \{
                            margin: 0;
                            padding: 0;
                        }
                        body {
                            font-family: Arial, sans-serif;
                            font-size: 14px;
                            line-height: 1.5;
                            color: #333;
                        }
                        /* Container */
                        .container {
                            width: 100%;
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                        }
                        /* Heading */
                        .heading {
                            text-align: center;
                            margin-bottom: 20px;
                        }
                        .heading h1 {
                            font-size: 24px;
                            margin-bottom: 10px;
                        }
                        /* Content */
                        .content {
                            margin-bottom: 20px;
                        }
                        /* Button */
                        .button {
                            display: inline-block;
                            background-color: #007bff;
                            color: #fff;
                            text-decoration: none;
                            padding: 10px 20px;
                            border-radius: 5px;
                        }
                        /* Footer */
                        .footer {
                            text-align: center;
                            color: #777;
                        }
                    </style>
                    <!-- Bootstrap CSS -->
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
                </head>
                <body>''' + f'''
                    <div class="container">
                        <div class="heading">
                            <h1>Forgot your password?</h1>
                        </div>
                        <div class="content">
                            <p>Hey {user.first_name},</p>
                            <p>You asked for a password recovery?</p>
                            <p><b>Here it is!</b></p>
                            <a href="http://127.0.0.1:5000/resetPassword/{user.resetPassword}"><input type="button" class="btn btn-success" value="Recover Password"></a>
                        </div>
                        <div class="footer">
                            <p>&copy; {emailSender.currentYear.year} TeamGroup. All rights reserved.</p>
                        </div>
                    </div>
                </body>
                </html>

                ''')
        
        msg = MIMEMultipart()
        msg['From'] = emailSender.email_address
        msg['To'] = user.email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))


        with smtplib.SMTP(emailSender.smtp_server, emailSender.smtp_port) as server:
            server.starttls()
            server.login(emailSender.email_address, emailSender.email_password)
            server.send_message(msg)
        
        print(f'Email sent successfully to {user.email}!')
        


    def PasswordChanged(self, user):

        subject = 'TeamBridge | Password Changed!'
        body = ('''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Email Template</title>
                    <style>
                        /* Reset CSS */
                        body, p, h1, h2, h3, h4, h5, h6 \{
                            margin: 0;
                            padding: 0;
                        }
                        body {
                            font-family: Arial, sans-serif;
                            font-size: 14px;
                            line-height: 1.5;
                            color: #333;
                        }
                        /* Container */
                        .container {
                            width: 100%;
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                        }
                        /* Heading */
                        .heading {
                            text-align: center;
                            margin-bottom: 20px;
                        }
                        .heading h1 {
                            font-size: 24px;
                            margin-bottom: 10px;
                        }
                        /* Content */
                        .content {
                            margin-bottom: 20px;
                        }
                        /* Button */
                        .button {
                            display: inline-block;
                            background-color: #007bff;
                            color: #fff;
                            text-decoration: none;
                            padding: 10px 20px;
                            border-radius: 5px;
                        }
                        /* Footer */
                        .footer {
                            text-align: center;
                            color: #777;
                        }
                    </style>
                    <!-- Bootstrap CSS -->
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
                </head>
                <body>''' + f'''
                    <div class="container">
                        <div class="heading">
                            <h1>Your password has been changed</h1>
                        </div>
                        <div class="content">
                            <p>Hey {user.first_name},</p>
                            <p>Your password has been changed, if it was you, ignore this email.</p>
                            <p>If this wasn't you please contact us to take actions</p>
                            <input type="button" class="btn btn-info" value="Contact us">
                        </div>
                        <div class="footer">
                            <p>&copy; {emailSender.currentYear.year} TeamGroup. All rights reserved.</p>
                        </div>
                    </div>
                </body>
                </html>

                ''')
        
        msg = MIMEMultipart()
        msg['From'] = emailSender.email_address
        msg['To'] = user.email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))


        with smtplib.SMTP(emailSender.smtp_server, emailSender.smtp_port) as server:
            server.starttls()
            server.login(emailSender.email_address, emailSender.email_password)
            server.send_message(msg)
        
        print(f'Email sent successfully to {user.email}!')

if __name__ == '__main__':
    emailSender()