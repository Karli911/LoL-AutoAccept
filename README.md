 __Auto Accept League of Legends__

This Python application automatically finds and clicks the "Accept" button in League of Legends, helping you quickly enter matches. It can be configured to run automatically on system startup across different operating systems.


## **Features**
- **Automatically detects and clicks** the "Accept" button in League of Legends.
- **Configurable** to run on startup for Windows, macOS, and Linux.
- **Logs activity** for troubleshooting and monitoring.

## **Troubleshooting**
- **1.** Ensure that the *accept_button.png* is located in the same directory as *auto-accept.py*.
- **2.** Be sure to launch "League of Legends" and not move the window around. Take a screenshot of the "Accept" button and crop it. Cut everything else except the button itself.
- **3.** Do **NOT** change the resolution of your screen too much. The script will detect the button only from the screenshot taken. If you want this to work in another resolution, make sure to take another screenshot, and replace the *accept_button.png* with the new screenshot.

## **Installation**

### **1. Windows**

#### **Convert Python Script to Executable**
To convert the Python script into an executable:

```bash
pip install pyinstaller
pyinstaller --onefile accept-button.py
```

This will generate an executable in the dist directory.
Set Up on Startup

Press **Win + R**, type shell:startup, and press Enter to open the Startup folder.
Copy the executable file from the dist directory into the Startup folder.

### 2. macOS
Convert Python Script to Executable

To create a macOS application:

```bash
pip install py2app
python accept-button py2app
```

This creates a .app package.
Add to Login Items

  Open System Preferences -> Users & Groups.
  Select your user account and click on the Login Items tab.
  Drag the .app file into the Login Items list.

### 3. Linux (Systemd)
Create a Systemd Service

    Create a .service file:

```bash
sudo nano /etc/systemd/system/auto_accept.service
```

Add the following content:
```bash
ini

    [Unit]
    Description=Auto Accept League of Legends

    [Service]
    ExecStart=/usr/bin/python3 /path/to/accept-button.py
    WorkingDirectory=/path/to/your/script/
    Restart=always
    User=your_username

    [Install]
    WantedBy=multi-user.target
    Replace /path/to/accept-button.py with the actual path to your script, and your_username with your Linux username
```
Enable and Start the Service
Enable the service to run on boot:

```bash

sudo systemctl enable auto_accept.service
```
Start the service immediately:

```bash

sudo systemctl start auto_accept.service
```
### Usage

Once set up, the application will automatically run in the background. It will monitor your screen for the "Accept" button in League of Legends and click it when found.
## Logging

The application generates logs to help troubleshoot any issues. Check the app.log file in the application directory to see the log entries.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

### License

This project is licensed under the MIT License. See the LICENSE file for details.

## Notes

  Ensure the ***accept_button.png*** image is correctly placed in the same directory as the executable.
  Adjust the template matching threshold and screen resolution if the button is not being detected correctly.
