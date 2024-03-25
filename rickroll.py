import subprocess

# Define the command to execute in each terminal window
command = "curl -s -L https://raw.githubusercontent.com/keroserene/rickrollrc/master/roll.sh | bash"

# AppleScript to open a new terminal window and execute the command
script = '''
tell application "Terminal"
    repeat 10 times
        do script "{0}"
    end repeat
end tell
'''.format(command)

# Save the AppleScript to a temporary file
script_file = "temp_script.scpt"
with open(script_file, "w") as file:
    file.write(script)

# Execute the AppleScript
subprocess.run(["osascript", script_file])

# Clean up the temporary script file
subprocess.run(["rm", script_file])
