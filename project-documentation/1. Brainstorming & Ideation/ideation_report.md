# Brainstorming & Ideation Report - Rising Waters

## 1. Problem Statement
Floods represent one of the most destructive natural disasters worldwide, leading to loss of lives, mass displacement, and immense economic damage. Conventional weather forecasts are often too broad and do not provide localized early-warning details. Disaster management teams and local authorities lack tools to classify real-time flood susceptibility based on local meteorological parameters.

**The Mission of Rising Waters:** To build an end-to-end Machine Learning warning system that consumes real-time local weather parameters (Annual Rainfall, Cloud Cover, and seasonal distribution) to classify flood risks instantly, allowing disaster relief coordinators to plan evacuations and allocate resources proactively.

---

## 2. Empathy Mapping

To understand the core users—such as **local meteorologists**, **disaster relief officers**, and **community leaders**—we analyzed their experiences:

### Says (User quotes):
* "We need a faster way to convert rainfall readings into actionable evacuation plans."
* "The warning bulletins are often too late; by the time the alert goes out, streets are already waterlogged."
* "Can we get a specific safety confidence score instead of just a generic alert?"

### Thinks (Beliefs & worries):
* *How do I prioritize resource allocation between three different sub-districts during monsoons?*
* *I worry that false alarms will make the community ignore actual evacuations.*
* *Is there a reliable model that generalizes weather trends without massive computational requirements?*

### Does (Observed behaviors):
* Regularly monitors stream gauges and manually cross-references them with radio weather alerts.
* Uses spreadsheets to log monthly rainfall but struggles to predict peak hazards.
* Mobilizes volunteer teams on stand-by during active monsoon season based on gut feeling.

### Feels (Emotions):
* **Anxious** about sudden cloudbursts during the night.
* **Helpless** due to the lack of specialized prediction tools for localized districts.
* **Responsible** for safeguarding lives and property under extreme conditions.

---

## 3. Problem-Solution Fit

| User Pain Point | System Feature | Strategic Value |
|---|---|---|
| Delayed warnings result in trapped populations. | Real-time classification with custom Bootstrap 5 alert panels. | Evacuation plans can be initiated hours in advance. |
| Inaccurate resource allocation. | Standardized parameter tables summarizing local meteorological metrics. | Relief coordinators deploy sandbags and boats to priority sectors. |
| Complex, heavy software configurations. | Zero-dependency Flask API compiled in pure Python. | Runs instantly in browser, compatible with mobile and Vercel. |
