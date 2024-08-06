import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import datetime

'''
THE FLOW OF THE OTP PROGRAM

1. The user writes the email during registration (done)
2. uses the "Send OTP" button and it sends a POST request to the backend (done)
3. then the backend will receive the request, which then it will generate a JS Object (done)
4. The JSON Object will indicate that the OTP is generated from this email (done)
5. The user gets the OTP and enters the OTP to the registration form (done)
6. Now when the user presses submit, it will see whether the OTP sent through the submission form
   is the same with the one in the backend that is generated
7. If it is the same, then the registration is successful

'''


class OTPVerification:
    def __init__(self):
        self.otp_store = {}

    def generate_otp(self, email_address):
        otp = random.randint(100000, 999999)
        timestamp = datetime.datetime.now()
        self.otp_store[email_address] = {'otp': otp, 'timestamp': timestamp}
        print(self.otp_store)
        return {'otp': otp, 'timestamp': timestamp, 'email_address': email_address}

    def send_otp_email(self, to_email, otp):

        '''
        if you are using gmail, make sure to use turn on your:
            - 2FA Authentication
            - make an "App Password" in settings so that you can login
        
        
        '''
        # from_email = "example@email.com"
        # from_password = "example"
        from_email = "stilllikelight@qq.com"
        from_password = "dowgmbuakxmhcaea"
        
        subject = "Your OTP Code"
        body = f"Your OTP code is {otp}"
        
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            server = smtplib.SMTP("smtp.qq.com", 587)  # this one depends on the smtp server and port from our mail provider
            server.starttls()
            server.login(from_email, from_password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
            server.quit()
        except Exception as e:
            print(f"Failed to send email: {e}")
            raise


    '''
    A Helper Function in OTPVerification Class to help verify the OTP that is
    submitted through the Svelte Forms
    '''
    def verify_otp(self, email, otp):
        to_email = email
        user_otp = otp
        
        if not to_email or not user_otp:
            return False

        if to_email in self.otp_store:
            stored_otp = self.otp_store[to_email]['otp']
            timestamp = self.otp_store[to_email]['timestamp']

            # Compare OTPs and check if the OTP is within the validity period
            if int(user_otp) == stored_otp and datetime.datetime.now() - timestamp < datetime.timedelta(minutes=5):
                # Remove the verified OTP
                del self.otp_store[to_email]
                return True
            else:

                return False
        else:
            return False
