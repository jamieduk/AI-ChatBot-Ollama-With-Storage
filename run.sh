#!/bin/bash
echo "Starting Chatbot"
#python chatbot.py
#!/bin/bash

# Function to check if in venv
check_venv() {
    # Check if there is a "bin/activate" file, which indicates we are in a venv
    if [ -f "bin/activate" ]; then
        echo "Already in a virtual environment."
        return 0
    else
        echo "Not in a virtual environment."
        return 1
    fi
}

# Main function to start venv
start_venv() {
    # Check if already in venv
    if check_venv; then
        return
    fi

    # Check if "myenv" directory exists
    if [ -d "myenv" ]; then
        echo "Activating existing virtual environment 'myenv'..."
        source myenv/bin/activate
    else
        echo "Creating and activating new virtual environment 'myenv'..."
        python -m venv myenv
        source myenv/bin/activate
    fi
}

# Call main function
start_venv

#!/bin/bash

# Infinite loop
while true
do
  # Run the Python script
  python chatbot-ollamaV4.py
  
  # Optional: add a small sleep to prevent a tight loop in case the script exits quickly
  sleep 1
done



