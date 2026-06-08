# Smart Energy Monitor — IoT & AI System

## Overview

Smart Energy Monitor is a real-time IoT and Artificial Intelligence platform designed to monitor household energy consumption, visualize device usage, and detect abnormal consumption patterns using Machine Learning.

The project combines IoT simulation, MQTT communication, data processing, storage, visualization, and anomaly detection into a complete smart-home energy monitoring solution.

---

## Features

- Real-time energy monitoring
- Smart home simulation using ESP32 (Wokwi)
- MQTT communication through EMQX Broker
- Data processing with Node-RED
- MongoDB data storage
- Flask REST API
- Interactive dashboards
- Machine Learning anomaly detection using Isolation Forest
- Device consumption ranking
- Monthly energy cost estimation

---

## System Architecture

```text
ESP32 (Wokwi)
      │
      ▼
 MQTT / EMQX
      │
      ▼
   Node-RED
      │
      ▼
   MongoDB
      │
      ▼
   Flask API
      │
      ▼
 Machine Learning
 (Isolation Forest)
      │
      ▼
 Dashboards
```

---

## Technologies

### IoT
- ESP32
- Wokwi
- MQTT
- EMQX

### Data Processing
- Node-RED

### Backend
- Python
- Flask

### Database
- MongoDB

### Machine Learning
- Scikit-learn
- Isolation Forest

### Visualization
- ThingsBoard
- Node-RED Dashboard
- Custom AI Dashboard

---

## Screenshots

### AI Dashboard

![AI Dashboard](screenshots/dashboard-ai.png)

### Local Dashboard

![Local Dashboard](screenshots/dashboard-local.png)

### ESP32 Simulation

![ESP32](screenshots/esp32-wokwi.png)

### Node-RED Flow

![Node-RED](screenshots/node-red-flow.png)

### ThingsBoard Dashboard

![ThingsBoard](screenshots/thingsboard-dashboard.png)

---

## Machine Learning Module

The project integrates an Isolation Forest model to detect abnormal energy consumption patterns.

Main capabilities:

- Unsupervised anomaly detection
- Consumption behavior analysis
- Abnormal device usage identification
- Energy optimization recommendations

---

## Smart Home Devices Simulated

- Lamp
- Television
- Fan
- Computer
- Air Conditioner
- Washing Machine

---

## Key Functionalities

- Real-time power monitoring
- Consumption trend visualization
- Device ranking by energy usage
- Anomaly detection
- Monthly cost estimation
- Historical data analysis

---

## Repository Structure

```text
Smart-Energy-Monitor-IoT-AI-System/
│
├── flows/
├── ml-model/
├── smart-home-simulation/
├── screenshots/
│
├── README.md
└── .gitignore
```

---

## Author

Imad Elmiri

Master IASD — Artificial Intelligence & Data Science