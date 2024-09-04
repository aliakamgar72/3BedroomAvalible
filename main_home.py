import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

# Configuration
url = "https://www.homestead.ca/apartments/1751-1761-sheppard-avenue-east-toronto"
check_interval = 300  # Check every hour (3600 seconds)
recipient_email = "fawadaryan@gmail.com"
sender_email = "aliakamgar0@gmail.com"
sender_password = "gwna lqpf lnbn syrg"

try:
    response = requests.get(url, proxies={"http": None, "https": None})
        
    if response.status_code == 200:
            print("The request was successful!")
            # Process the response here if needed
            
    else:
            print(f"Request failed with status code: {response.status_code}")
            
            
except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        

def check_availability():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Adjust this logic to match the HTML structure of the webpage
    # Find the section where apartment availability is listed
    available_units = soup.find_all('div', class_='suite-row')  # You may need to inspect the site to get the correct class name

    for unit in available_units:
        if 'Inquire Now' in unit.text:  # Adjust this condition based on the actual text content of the availability
            return True
    
    return False

def send_email_notification():
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "3-Bedroom Apartment Availability Alert!"

    body = f"A 3-bedroom apartment is now available at {url}. Check the website for more details."
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

def main():
    while True:
        if check_availability():
            print("3-bedroom apartment is available!")
            send_email_notification()
            break
        else:
            print("No availability yet. Checking again in one hour...")
        time.sleep(check_interval)

if __name__ == "__main__":
    main()