# PDF Downloader Application

## Overview
The PDF Downloader is a GUI application built using Python and Eel, designed to download PDF files from google search using a prompt. This application provides a user-friendly interface to input topic name/prompt and download PDF files directly to the provided directory.

## Features
- Simple and intuitive GUI.
- Download PDF files frome google search by only a prompt.
- Error handling for invalid URLs or failed downloads.
- Progress indication for ongoing downloads.

## Prerequisites
- Python 3.12.4
- Internet connection for downloading PDFs

## Installation

Clone the repository:

```bash
git clone https://github.com/gurjarms/PDF-Downloader.git
cd PDF-Downloader
cd app
```
## create a virtual environment
```bash
python -m venv env
```
## Run virtual environment
```bash
env\scripts\activate
```

## Install the required packages:
install dependencies
```bash
pip install -r requirements.txt
```

## Run the application:

```bash
python main.py
```

The GUI will launch. Enter the pdf topic name you wish to download and location for download pdf , and click the "Download" button.

## Project Structure
- main.py: The main Python script to run the application.
- requirements.txt: Lists all the dependencies required to run the application.
- web/: Contains HTML, css and js files for the GUI.

## Dependencies
### The application requires the following packages, listed in requirements.txt:
```
Eel
Requests
bs4
func_timeout
selenium
```
## Contributing
### Contributions are welcome! If you have suggestions for improvements or find bugs, feel free to create an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
Thanks to the creators of Eel for providing a simple way to create Python GUIs with web technologies.
