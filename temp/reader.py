import os

# Define the file path
documents_path = os.path.expanduser("~/Documents")
file_path = os.path.join(documents_path, "savefile.bulletheaven")

# Initialize variables
upgrades = 0
kills = 0
player_hp = 0
exp = 0
player_level = 0

# Read data from the file and assign to variables
with open(file_path, "r") as file:
    for line in file:
        if line.startswith("Upgrades:"):
            upgrades = int(line.split(":")[1].strip())
        elif line.startswith("Kills:"):
            kills = int(line.split(":")[1].strip())
        elif line.startswith("Player HP:"):
            player_hp = int(line.split(":")[1].strip())
        elif line.startswith("EXP:"):
            exp = int(line.split(":")[1].strip())
        elif line.startswith("Player Level:"):
            player_level = int(line.split(":")[1].strip())

# Print the variables
print(f"Upgrades: {upgrades}")
print(f"Kills: {kills}")
print(f"Player HP: {player_hp}")
print(f"EXP: {exp}")
print(f"Player Level: {player_level}")
