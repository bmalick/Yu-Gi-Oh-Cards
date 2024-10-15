# Image in order to create .exe file for windows using ubuntu base image


# Use the base Ubuntu image
FROM ubuntu

# Add i386 architecture and update the package list
RUN dpkg --add-architecture i386 && apt-get update

# Install necessary packages: Wine, dependencies, and Python 3
RUN apt-get install -y \
    software-properties-common \
    wget \
    wine64 \
    wine32:i386 \
    winbind \
    xvfb \
    python3-pip

# Download the Python installer for Windows (change version if needed)
RUN wget https://www.python.org/ftp/python/3.9.1/python-3.9.1-amd64.exe

# Run the Python installer using Wine (simulating Windows installation)
RUN xvfb-run wine python-3.9.1-amd64.exe /quiet InstallAllUsers=1 PrependPath=1

# Install PyInstaller using Wine's Python
RUN wine python -m pip install pyinstaller

# Copy your Python script to the container
COPY your_script.py /root/your_script.py

# Run PyInstaller to create the Windows executable
RUN xvfb-run wine pyinstaller --onefile /root/your_script.py

# Command to keep the container running for debugging or manual execution
CMD ["/bin/bash"]

# Run PyInstaller to Build an Executable
# wine pyinstaller --onefile your_script.py

# Run your script
# wine your_script.exe
