# Fundamentals of Algorithms

## Description
This project is a simple implementation of MS Paint using Python. It creates a dynamic canvas where users can draw freely, with each pixel updated in real-time. The core functionality involves direct pixel manipulation to render brush strokes. Extended features like **Undo** and **Redo** allow users to step forward or back through their drawing history, enhancing usability for more complex illustrations.

## Setup

Note: For all of these you may need to replace `python` with `py` or `python3` depending on your operating system and python version.

```bash
python -m pip install virtualenv
python -m venv venv
```

Next, activate your virtual environment (Must be done every time you open the terminal)

Windows Bash
```
source venv/Scripts/activate
```

Windows CMD
```
venv/Scripts/activate
```

Windows Powershell
```
venv/Scripts/activate.ps1
```

Mac / Linux bash
```
source venv/bin/activate
```

Then install the requirements!
```
python -m pip install -r requirements.txt
```

## Running the program

To run the interactive version:

```bash
python main.py
```

To run the visual tests:

```bash
python -m visuals.basic
python -m visuals.complex
python -m visuals.styles
```

