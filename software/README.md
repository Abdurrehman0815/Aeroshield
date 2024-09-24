# AI-Driven Drone Navigation for Air Pollution Collection

## Table of Contents
1. [Project Overview](#project-overview)
2. [How the Code Works](#how-the-code-works)
3. [AI Components](#ai-components)
4. [Air Pollution Collection](#air-pollution-collection)


---

## Project Overview
The **AI-driven drone system** autonomously navigates, avoids obstacles, predicts weather, and collects air pollution data on a **TiO2 plate**. AI helps optimize the flight path, adjust to real-time weather and environmental conditions, and avoid collisions while in flight.

---

## How the Code Works
This code includes:
- **Navigation**: AI algorithms like A* or Dijkstra for shortest-path planning using GPS waypoints.
- **Obstacle Detection & Avoidance**: Real-time object detection using a pre-trained YOLO model.
- **Weather Prediction**: Predict wind speed and rain using AI, adjusting flight accordingly.
- **Air Pollution Collection**: The drone hovers over a specified area and collects pollutants using a **TiO2 plate**.

---

## AI Components

### 1. Path Planning (Shortest Path)
The AI determines the shortest path using **A* or Dijkstra's algorithm** to navigate efficiently while avoiding obstacles.

### 2. Obstacle Detection and Avoidance
Real-time object detection is done via a **YOLO model**, helping the drone adjust its path dynamically to avoid obstacles.

### 3. Weather Prediction
AI-based models forecast **wind speed** and **rain** to adjust the drone’s altitude or return to base if weather conditions are unsafe.

---

## Air Pollution Collection

A TiO2 plate attached to the drone collects pollutants like NOx and particulate matter as the drone hovers at the specified location.
