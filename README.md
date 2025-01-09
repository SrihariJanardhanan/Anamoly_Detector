# Anomaly Detection in CCTV Footage

## Overview

This Deep learning based web application is designed to detect anomalies and violent behavior in real-time CCTV footage using advanced image processing algorithms. The system leverages 3D Convolutional Neural Networks (3D-CNN) and FlowNet models to process video data and identify suspicious activities. Upon detecting an anomaly, the application instantly sends an alert via SMS using Twilio's API, ensuring prompt response to potential threats.

## Features

- **Real-Time Video Processing**: Analyze live CCTV footage to detect anomalies or violent behavior in real time.
  
- **Advanced Deep Learning Models**:
  - **3D-CNN**: Used for spatial-temporal analysis of video frames to detect abnormal patterns.
  - **FlowNet**: Utilized for optical flow analysis, aiding in detecting motion-based anomalies.
  
- **Alert System**:
  - **SMS Notifications**: When an anomaly is detected, the system sends an immediate alert to pre-configured mobile numbers using Twilio's SMS API
  
- **User-Friendly Interface**: A web-based dashboard for monitoring live footage, reviewing detected anomalies, and managing alerts.

- **Region-Based Anomaly Statistics**:
  - **Crime Stats Dashboard**: Displays the number of anomalies detected across various local streets, helping authorities track and respond to incidents more effectively.

## Installation

1. **Clone the Repository**
   ```
   git clone https://github.com/Mohamed-Javeed/Anomaly-Detector-SIH-23.git
   ```

2. **Navigate to the Project Directory**
   ```
   cd Anomaly-Detector-SIH-23
   ```

3. **Install Dependencies**
   Ensure you have `pip` and `virtualenv` installed. Then, create a virtual environment and install the required packages:
   ```
   virtualenv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Set Up Twilio API**
   - Sign up for a [Twilio](https://www.twilio.com/) account.
   - Get your account SID, authentication token, and a Twilio phone number.
   - Set these credentials in your environment variables or (suggested) within the keys.py file .

5. **Apply Migrations**
   Set up the database by running the migrations:
   ```
   python manage.py migrate
   ```

6. **Run the Server**
   Start the development server:
   ```
   python manage.py runserver
   ```

7. **Access the Application**
   Open your web browser and go to `http://127.0.0.1:8000/` to access the application.

## Project Structure

- **anomaly_detector/**: Core app handling video processing, anomaly detection, and alert generation.
  
- **models/**: Directory containing the pre-trained 3D-CNN and FlowNet models used for video analysis.
  
- **alerts/**: Handles the integration with Twilio's API for sending SMS alerts.
  
- **dashboard/**: Manages the web interface, displaying live footage, detection logs, and alert history.
  
- **templates/**: HTML templates for rendering the web pages.

- **static/**: Static files including CSS, JavaScript, and images used in the web interface.

## Usage

1. **Anomaly Detection**:
   - The system processes video frames in real-time using 3D-CNN and FlowNet models to detect any suspicious activity.
  
2. **Alerts and Notifications**:
   - When an anomaly is detected, it is flagged on the dashboard, and an SMS alert is sent to the configured mobile numbers.

3. **Review Detected Anomalies**:
   - Users can view a log of detected anomalies along with relevant details like timestamp and type of anomaly.

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## Contact

For any queries or issues, please reach out via [GitHub Issues](https://github.com/Mohamed-Javeed/Anomaly-Detector-SIH-23/issues).
