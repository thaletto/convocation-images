import os
import requests
import string

# ---- Get input from user ----
department = input("Enter department code (e.g., CSE, ECE, MEC): ").strip().upper()
year = input("Enter year of passing (e.g., 20 for 2020): ").strip()
section_letter = input("Enter section letter (e.g., A, B, C): ").strip().upper()

# Map section letter to numeric ID (A -> 0, B -> 1, C -> 2, ...)
section_map = {letter: str(idx) for idx, letter in enumerate(string.ascii_uppercase)}
if section_letter not in section_map:
    print("❌ Invalid section letter.")
    exit(1)
section_id = section_map[section_letter]

# ---- Range (2-digit roll numbers) ----
start_roll = int(input("Enter start roll number (e.g., 01): ").strip())
end_roll = int(input("Enter end roll number (e.g., 72): ").strip())

# ---- Folder structure: 2020/CSE/C/ ----
SAVE_DIR = os.path.join("images", f"20{year}", department, section_letter)
os.makedirs(SAVE_DIR, exist_ok=True)

# ---- Download loop ----
for roll in range(start_roll, end_roll + 1):
    roll_str = f"{roll:02d}"  # ensures 2-digit roll number
    file_code = f"{year}{section_id}{roll_str}"
    url = f"https://convocation.amrita.ac.in/files/CB.EN.U4{department}{file_code}.JPG"
    filename = os.path.join(SAVE_DIR, f"CB.EN.U4{department}{file_code}.jpg")

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"✅ Downloaded: {filename}")
        else:
            print(f"❌ Not Found: {url}")
    except requests.RequestException as e:
        print(f"⚠️ Error fetching {url}: {e}")
