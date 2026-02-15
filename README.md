# Gesture-Based Copy/Paste Prototype (Work in Progress)

An innovative Human-Computer Interaction (HCI) tool that allows users to perform clipboard operations (Copy & Paste) using real-time hand gesture recognition.

 Overview
This project explores the intersection of Computer Vision and desktop automation. By leveraging hand-tracking algorithms, it translates specific physical gestures into system-level keyboard shortcuts, providing a touchless way to interact with digital content.

Tech Stack
- Language: Python
- Computer Vision: OpenCV / Mediapipe (Hand tracking logic)
- Automation: PyAutoGUI (for system-level shortcut triggering)
- Logic: Custom gesture-detection algorithms to minimize false positives.

 Key Features
- Real-time Tracking: High-speed hand landmark detection.
- Gesture Mapping: - `Gesture A`: Triggers `Ctrl + C` (Copy)
  - `Gesture B`: Triggers `Ctrl + V` (Paste)
 
    Future Roadmap:
  -Cross-Platform Potential:** Designed to work as a background utility for desktop environments.
- Integration with **Machine Learning** models to recognize more complex, personalized gestures.
- Reducing "Technical Debt" by optimizing frame processing for lower CPU usage (Green Computing).
