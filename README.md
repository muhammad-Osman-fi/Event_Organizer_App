#                                            EVENT ORGANIZER
#                                      Copyright 2024 Usman Aslam
#                              Licensed under the Apache License, Version 2.0


Welcome to the Event Organizer project! This application is designed to help you manage and track guests at events. It provides functionality for adding guests, updating and filtering guest lists, scanning QR codes, and sending invitations via email. Here's a comprehensive guide on how to set up, use, and understand this project.

# Table of Contents

Project Overview
Dependencies
Setup Instructions
Using the Application
Troubleshooting
Contributing
License

# Project Overview

Event Organizer is a desktop application built using the Tkinter library in Python. It allows you to:

Add and manage guests for an event.
Generate QR codes for guests and scan them at the event entrance.
Send email invitations with QR codes.
Keep track of payments and other guest details.
Filter and search guests based on various criteria.

# Dependencies

To run this project, you'll need Python 3.x installed along with the following packages:

Tkinter (usually comes with Python)
re (regular expressions)
sqlite3 (SQLite database library)
qrcode (QR code generation library)
tempfile (temporary file handling)
smtplib (SMTP client for sending emails)
email (email handling and MIME parsing)
threading (multithreading support)
datetime (date and time handling)
cv2 (OpenCV for QR code scanning)
pyzbar (for decoding QR codes)

To install missing packages, use the following command:

"pip install qrcode opencv-python pyzbar"

# Setup Instructions

Clone the repository to your local environment:

"git clone <repository-url>"
"cd Event_Organizer_App"

Ensure you have all dependencies installed (see Dependencies).
Run the application:

"python event_organizer.py"

# Troubleshooting

If you encounter issues with the QR code scanner, ensure you have a functioning webcam and the opencv-python package installed.
If you cannot send emails, check your email server settings and credentials.
If the application doesn't start, verify that all dependencies are installed correctly.

# Contributing

Contributions are welcome! To contribute to this project, please follow these steps:

Fork the repository.
Create a new branch for your feature or bugfix.
Make your changes and commit them.
Push your branch to your fork.
Create a Pull Request with a detailed description of your changes.
# License

This project is licensed under the Apache License 2.0. See the LICENSE file for more information.

Thank you for using the Event Organizer! We hope this guide helps you get started with the project. If you have any questions or need further assistance, please feel free to reach out or open an issue in the repository.
