# Aeroshield (AQ-Drone) Project: Complete Overview

## 🚁 What is this project?

**Aeroshield**, also known as the **AQ-Drone Project**, is an innovative open-source air quality monitoring and prediction system that combines drone technology, artificial intelligence, and air purification techniques to address urban pollution challenges.

## 🎯 Project Purpose

The system addresses critical air quality issues in urban areas by:
- **Monitoring**: Real-time air quality assessment using drone-mounted sensors
- **Predicting**: AI-powered forecasting of air quality trends for the next 24 hours
- **Mitigating**: Active air purification using TiO2 (Titanium Dioxide) photocatalytic technology

## 🏗️ System Architecture

### 1. **Main Project Components**

#### `/` (Root Directory)
- **Purpose**: Overall project documentation and coordination
- **Key Features**:
  - TiO2 air purification technology integration
  - AI-guided navigation to high-pollution areas
  - Smart battery management for autonomous operations
  - Real-time data collection (CO, NOx, Ozone, VOCs, PM)

#### `/software/` - Drone Navigation & Control
- **Purpose**: AI-driven autonomous drone navigation system
- **Files**:
  - `on-drone.py` (99 lines): Main drone control script
  - `README.md`: Technical documentation
- **Key Features**:
  - **AI Path Planning**: A* and Dijkstra algorithms for optimal route planning
  - **Obstacle Avoidance**: YOLO-based real-time object detection
  - **Weather Prediction**: AI models for wind speed and rain forecasting
  - **DroneKit Integration**: Direct drone hardware control
  - **Autonomous Navigation**: GPS waypoint-based flight management

#### `/Intel-aeroshield-updated/` - Data Processing & ML Pipeline
- **Purpose**: Complete air quality data processing and prediction system
- **Files**:
  - `preprocess.py` (32 lines): Data cleaning and preparation
  - `bluetooth_data.py` (44 lines): Sensor data collection via Bluetooth
  - `airq-processing.py` (59 lines): AQI calculation and classification
  - `train-test.py` (156 lines): Machine learning models and predictions
  - `Readme.md`: Technical documentation
  - Data files: CSV datasets and training graphs
- **Key Features**:
  - **Data Pipeline**: Bluetooth → Processing → AQI Calculation → ML Prediction
  - **Intel OneDAL Integration**: Optimized machine learning performance
  - **Dual ML Models**: Both scikit-learn and Intel OneDAL implementations
  - **24-hour Forecasting**: Air quality predictions for next day
  - **Performance Visualization**: Training time comparisons and accuracy metrics

## 🔧 Technical Implementation

### Drone Navigation System (`/software/`)
```python
# Core functionality includes:
- Vehicle connection and control (DroneKit)
- AI-based path planning algorithms
- Real-time obstacle detection and avoidance
- Weather-adaptive flight adjustments
- Autonomous takeoff, navigation, and landing
```

### Data Processing Pipeline (`/Intel-aeroshield-updated/`)
```python
# Workflow:
1. preprocess.py: Clean raw air quality data
2. bluetooth_data.py: Collect real-time sensor data
3. airq-processing.py: Calculate AQI values
4. train-test.py: Train ML models and predict future AQI
```

### Air Quality Metrics Monitored
- **CO2**: Carbon Dioxide levels
- **NH3**: Ammonia concentration
- **VOC**: Volatile Organic Compounds (average of Benzene, Toluene, Xylene)
- **Particulate Matter**: PM2.5, PM10
- **Gases**: NO, NO2, SO2, O3, NOx

## 🚀 System Workflow

1. **Detection**: Air quality monitoring stations identify high-pollution areas
2. **Deployment**: Drone autonomously navigates to target location using AI pathfinding
3. **Collection**: TiO2 plates collect and purify polluted air while sensors gather data
4. **Analysis**: Real-time data processing and AQI calculation
5. **Prediction**: ML models forecast air quality for next 24 hours
6. **Return**: Drone returns to base for recharging and data upload

## 💡 Key Innovations

### AI-Powered Features
- **Smart Navigation**: A* algorithm for optimal flight paths
- **Predictive Analytics**: Random Forest models for AQI forecasting
- **Real-time Adaptation**: Dynamic route adjustment based on obstacles and weather
- **Performance Optimization**: Intel OneDAL for faster ML computations

### Environmental Technology
- **TiO2 Photocatalysis**: Active air purification during data collection
- **Multi-sensor Integration**: Comprehensive pollutant monitoring
- **Autonomous Operations**: Minimal human intervention required

## 📊 Performance Metrics

The system includes comprehensive performance tracking:
- **ML Model Accuracy**: Classification and regression model validation
- **Training Time Comparison**: Intel OneDAL vs. scikit-learn performance
- **Real-time Processing**: Bluetooth data streaming and processing
- **Flight Operations**: Battery management and navigation efficiency

## 👥 Project Team

- **Harikrishnan A**
- **Ashok Kumar S** 
- **Balaji M**
- **Abdur Rehman**

## 🛠️ Technology Stack

- **Programming**: Python
- **Drone Control**: DroneKit
- **Machine Learning**: scikit-learn, Intel OneDAL
- **Data Processing**: pandas, NumPy
- **Visualization**: matplotlib
- **Hardware Integration**: Bluetooth communication, sensor networks
- **AI Algorithms**: A*, Dijkstra, YOLO, Random Forest

## 🌍 Real-world Impact

This system addresses critical urban air quality challenges by providing:
- **Scalable Monitoring**: Deployable in cities with multiple monitoring stations
- **Active Mitigation**: Not just monitoring, but actively purifying air
- **Predictive Capabilities**: Helping communities prepare for air quality changes
- **Cost-effective Solution**: Open-source technology accessible to communities worldwide

---

*This project represents a comprehensive approach to urban air quality management, combining cutting-edge AI, robotics, and environmental technologies into a unified system for monitoring, predicting, and improving air quality in urban environments.*