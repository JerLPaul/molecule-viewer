# Project Name
Molecule Viewer

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction
Molecule Viewer is a web-based application designed to visualize 2D representations of molecular structures.
The project uses a C backend for molecule data management and transformations, which is exposed to Python through SWIG (Simplified Wrapper and Interface Generator).
It enables users to upload molecules, view atoms and bonds, rotate molecules along x, y, or z axes, and store molecular data inside a SQLite database.
This efficient hybrid architecture provides the speed of C with the flexibility of Python.

## Features
- 🧪 Parse molecular .sdf files and store atoms/bonds.

- 🎨 Render molecules as scalable SVG images directly in the browser.

- 🔄 Rotate molecules dynamically on x, y, and z axes.

- 📦 Store and retrieve molecules and element properties from a SQLite database.

- 🖌️ Automatically generate radial gradients for atoms based on their properties (color, radius).

- 🌐 Host an HTTP server to handle file uploads, molecule display, and interaction.

- 🔗 Frontend integration through index.html with AJAX for dynamic interactions.

## Installation
Follow these steps to set up the project locally:

1. Clone the repository or download the files.

2. Ensure you have Python 3.x, SWIG, GCC, and SQLite3 installed.

3. Compile the C code and generate Python bindings using the provided Makefile:
```
make
```

4. Start the server:
```
python3 server.py
```

5. Open your browser and navigate to:
```
http://localhost:57455
```

## Usage
- 📄 Upload Molecules: Use the form to upload .sdf files and save molecules into the database.

- 🖥️ Display Molecules: Select molecules to render their structure as SVG.

- 🔄 Rotate Molecules: Apply rotations along x, y, or z axes to change molecule orientation.

- ➕ Add New Elements: Extend the database by adding new chemical elements with customized appearance.

- 🗑️ Remove Elements: Delete unwanted elements from the system dynamically.

## License
This project is licensed under the MIT License.
You are free to use, modify, and distribute this software with proper attribution.

## Acknowledgements
- SWIG for enabling seamless C-to-Python integration.

- SQLite3 for lightweight, embedded database storage.

- Python's http.server module for quick HTTP server setup.

- Open Chemistry File Formats for molecule structure (.sdf).

- Special thanks to various online resources on molecular visualization and SVG graphics generation.

