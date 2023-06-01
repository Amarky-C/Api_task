import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

firstUrl = input('Input Stack Overflow API link: ')
secondUrl = "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow"

user_name = input("enter user name: ")
smtp_username = "amarkychinelle@gmail.com"
smtp_password = "roqdsjxcrbhmvnxb"
sender_email = input("enter sender email: ")
receiver_email =input("enter recipient email: ")
subject = "Stack Overflow Results"

# Set the proper header to be sent
try:
    response = requests.get(firstUrl).json()
except:
    response = requests.get(secondUrl).json()

responseLength = len(response['items'])
header = f"DATA FETCHED FROM STACK-OVERFLOW API CONTAINING: {responseLength} RESULTS."

def format_results():
    results = []
    count = 1

    # Add header
    results.append(header)
    results.append('\n')

    while count <= responseLength:
        # Format the results
        result = f"Number {count}\n"
        result += f"This question was asked by: {response['items'][count-1]['owner']['display_name']} with user ID: {response['items'][0]['owner']['user_id']}\n"
        result += f"The title of the question is: {response['items'][count-1]['title']}\n"
        result += f"The number of views on the question is: {response['items'][count-1]['view_count']}\n"
        result += f"The link to the question is: {response['items'][count-1]['link']}\n"
        result += f"The link to {response['items'][count-1]['owner']['display_name']}'s profile image is: {response['items'][count-1]['owner']['profile_image']}\n"
        result += '\n'
        results.append(result)
        count += 1

        # Return only 50 results
        if count == 51:
            break

    return '\n'.join(results)

# Format the results
formatted_results = format_results()

# Email configuration

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Create a plain text version of the email
plain_text = MIMEText(formatted_results, "plain")

# Attach the plain text version to the email
message.attach(plain_text)

# Send the email
smtp_server = "smtp.gmail.com"
smtp_port = 587


try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    print(user_name, "Questions downloaded and sent via email successfully.")
except Exception as e:
    print(user_name, "An error occurred while sending the email:", str(e))