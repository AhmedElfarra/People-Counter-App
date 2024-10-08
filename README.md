<p align="center"></p> <h1 align="center">Retail Store Customer Traffic Analysis System</h1> <p align="center"> <strong>Advanced real-time insights for retail store optimization</strong> </p> <p align="center"> <a href="#retail-store-customer-traffic-analysis-system">About</a> • <a href="#key-features">Key Features</a> • <a href="#tech-stack">Tech Stack</a> • <a href="#getting-started">Getting Started</a> • <a href="#troubleshooting">Troubleshooting</a> • <a href="#contributors">Contributors</a> </p>

# Retail Store Customer Traffic Analysis System

- This project leverages a Raspberry Pi with a camera module to develop an advanced system for tracking and analyzing customer traffic in retail environments. Using computer vision and deep learning technologies, the system provides real-time insights into store performance, helping store owners optimize both operations and customer experience.

## Project Motivation

- In the competitive retail market, understanding customer behavior is key to success. Traditional methods of customer tracking often fail to provide the depth of data needed to make informed decisions. This project addresses this gap by employing sophisticated technologies to enhance data accuracy and provide actionable insights, ultimately aiming to improve store profitability and customer satisfaction.

## System Overview

The system integrates several technologies and components:
- **Raspberry Pi with Camera Module**: Captures video footage for real-time people detection and counting.
- **Python with OpenCV and PyTorch**: Processes the video to detect and track people.
- **WebSocket (FastAPI)**: Facilitates real-time data transmission between the Raspberry Pi and the analytics dashboard.
- **Streamlit**: Provides a user-friendly dashboard for real-time and historical data visualization.
- **Packet Sniffer**: Enhances people counting accuracy by analyzing WiFi probe requests to estimate the number of nearby devices.

### Key Features

- **Real-Time Analytics**: Monitors customer entry and exit in real time, with data refreshed instantaneously on the dashboard.
- **Data Visualization**: Provides graphs and statistics through an interactive dashboard, aiding in quick decision-making.
- **Scalable Architecture**: Designed to be easily scalable, supporting increased load and additional cameras without significant changes to the core system.
- **Security and Privacy**: Ensures data is processed and stored securely, with measures to protect against unauthorized access.

Tech Stack
<p align="center"> <img src="https://img.shields.io/badge/Raspberry%20Pi-FF0000?style=for-the-badge&logo=raspberry-pi&logoColor=white" alt="Raspberry Pi"> <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV"> <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch"> <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"> <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"> </p>

## Prerequisites
Before running the system, ensure you have the following installed:
- Python 3.8+
- Raspberry Pi OS or compatible Unix/Linux OS
- Docker (for Docker-based setup)

## How to Run

- This application can be run either directly on your local machine using Python or using Docker for containerization, which simplifies setup and deployment. Follow the steps below based on your preferred method.

### Running Without Docker

- Ensure you have Python 3.8+ installed before you begin.

1. **Clone the repository:**
- cd into project repo and then cd into src 

#### Set up and activate the Python virtual environment:

```bash 
python3 -m venv myenv
source myenv/bin/activate
```

#### Install required dependencies:

```bash
pip3 install -r requirements.txt
```

#### Start the WebSocket server to handle real-time data:

```bash
uvicorn websocket_server:app --reload --host 0.0.0.0 --port 8000
```

#### Run the main application script:

```bash
python3 main.py
```

#### Launch the Streamlit dashboard to view the analytics:

```bash
streamlit run app.py
```

- Navigate to http://localhost:8501 on your web browser to access the dashboard.


### Running With Docker
- Ensure you have Docker and Docker Compose installed.
- Navigate to the project's root directory where the docker-compose.yml file is located.
Build and run the containers:

```bash
docker-compose build
docker-compose up
```

- The application will be accessible through the Streamlit dashboard at http://localhost:8501.

### Application Layout

#### System Dashboard

- Here is a look at the system dashboard which provides real-time analytics:

![Dashboard](/images/dashboard.png "System Dashboard")

#### Graphical User Interface

- This is the graphical user interface of the application, showing the main control elements:

![GUI](/images/gui.png "Graphical User Interface")

#### Navigation Panel

- Below is the navigation panel used in our system:

![Navigation Panel](/images/nav.png "Navigation Panel")


#### Data Download Example

Below is an example of how the data looks when downloaded as a CSV file from the system:

![Data CSV Example](/images/data-csv.png "Downloaded Data CSV")

### Additional Notes
- Ensure that the Raspberry Pi and camera are correctly set up and that the Raspberry Pi's IP address is correctly configured in the application settings if running remotely.
- Check the firewall settings on your network to ensure that the required ports are open (especially port 8501 for Streamlit and port 8000 for the WebSocket server).

### Troubleshooting
- WebSocket Connection Issues: Ensure the WebSocket server address in the client configuration matches the server's IP and port.
- Camera Not Detected: Verify that the Raspberry Pi's camera is properly connected and enabled.
- Dependency Errors: Check that all Python dependencies are correctly installed in the virtual environment.

### Contributors
- Ahmed Elfarra
- Ammar Alzureiqi
