import os

# Define the data
upgrades = 5
kills = 224
player_hp = 60
exp = 300
player_level = 6

# Define the file path
documents_path = os.path.expanduser("~/Documents")
file_path = os.path.join(documents_path, "savefile.bulletheaven")

# Write data to the file
with open(file_path, "w") as file:
    file.write(f"Upgrades: {upgrades}\n")
    file.write(f"Kills: {kills}\n")
    file.write(f"Player HP: {player_hp}\n")
    file.write(f"EXP: {exp}\n")
    file.write(f"Player Level: {player_level}\n")

print(f"Data saved to {file_path}")
