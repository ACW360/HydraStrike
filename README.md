
# HydraStrike

**HydraStrike** is a graphical user interface (GUI) tool for automating brute-force attacks using Hydra. It is designed to be user-friendly and supports both single username and userlist-based attacks. HydraStrike works on Linux, macOS, and Windows (WSL or Cygwin environments).

## Features

- Support for both single usernames and userlists.
- HTTP POST form-based login brute-forcing.
- Light and Dark themes.
- Progress bar indicator.
- Stop button to terminate attacks at any time.
- Auto-detection of successful login and stops automatically.

## Requirements

- Python 3.6+
- [Hydra](https://github.com/vanhauser-thc/thc-hydra)
- Tkinter (comes with Python)
- Works best on Linux or WSL on Windows

## Installation

### Linux (Ubuntu/Debian-based)

```bash
sudo apt update
sudo apt install hydra python3 python3-pip -y
pip3 install -r requirements.txt
```

### macOS

```bash
brew install hydra python3
pip3 install -r requirements.txt
```

### Windows (via WSL)

1. Install [WSL](https://learn.microsoft.com/en-us/windows/wsl/install)
2. Use Ubuntu inside WSL:

```bash
sudo apt update
sudo apt install hydra python3 python3-pip -y
pip3 install -r requirements.txt
```

## Usage

```bash
python3 hydrastrike.py
```

1. Enter the target IP or hostname.
2. Provide path to password list.
3. Either enter a single username or provide path to a userlist.
4. Enter the HTTP POST form path (e.g., `/login.php`).
5. Enter the incorrect login verbiage (e.g., `Invalid username or password`).

HydraStrike will run Hydra and show real-time output in the GUI.

 watch a video tutorial on YouTube.
 👇👇👇
 https://youtu.be/un1EMxju4OI?si=O-ymdc1Nj94Lzi5n
 
## Legal Disclaimer

This tool is intended for **educational purposes** only and should not be used for unauthorized access to systems. The authors are **not responsible** for any damage caused by the misuse of this software.

## License

MIT License © 2025 ACW360, Arewa Cyber Warrior (HydraStrike)
