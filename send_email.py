import streamlit as st
import smtplib
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import threading

# Email settings - use Streamlit input for these
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # SSL port

# Function to send the email
def send_email(SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL, SUBJECT, BODY):
    try:
        # Set up the server connection
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Create the email content
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = RECIPIENT_EMAIL
        message["Subject"] = SUBJECT

        # Add body text
        message.attach(MIMEText(BODY, "plain"))

        # Send the email
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, message.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        server.quit()

# Function to schedule the daily email
def schedule_daily_email(SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL, SUBJECT, BODY):
    # Send email every day at 9:00 AM
    schedule.every().day.at("09:00").do(send_email, SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL, SUBJECT, BODY)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Wait for 1 minute

# Streamlit UI
st.markdown("""
    <style>
        body {
            background-image: url('email.jpg');
            background-size: cover;
            background-position: center;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            cursor: pointer;
            border-radius: 8px;
            transition: background-color 0.3s;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .footer {
            text-align: center;
            padding: 10px;
            color: white;
            font-size: 18px;
            font-style: italic;
        }
    </style>
""", unsafe_allow_html=True)

st.title("✨ Daily Automated Email Scheduler ✨")

# Input fields with emojis for better visuals
SENDER_EMAIL = st.text_input("📧 Sender Email", "")
SENDER_PASSWORD = st.text_input("🔑 Sender Password", type="password")
RECIPIENT_EMAIL = st.text_input("📩 Recipient Email", "")
SUBJECT = st.text_input("📝 Email Subject", "Daily Report")
BODY = st.text_area("📄 Email Body", "This is your daily automated report.")

if st.button("⏰ Start Scheduling"):
    if SENDER_EMAIL and SENDER_PASSWORD and RECIPIENT_EMAIL:
        st.write("Scheduling email task... 🗓️")

        # Run the scheduling function in a separate thread
        email_thread = threading.Thread(target=schedule_daily_email, args=(SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL, SUBJECT, BODY))
        email_thread.start()

        st.write("✅ Email task is scheduled to run daily at 9:00 AM.")
    else:
        st.write("⚠️ Please provide all the required email details.")

# Footer message
st.markdown("<div class='footer'>Made with ❤️ by Farida Bano</div>", unsafe_allow_html=True)
