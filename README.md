# Picture Tracing App for Kids

## Overview
This project is a Python-based application designed to help kids trace pictures using AI-generated outlines. The app includes both a web-based user interface and a command-line interface (CLI), providing flexible ways to interact with the tool.

## Project Structure

- **app.py**: Main web application file.
- **cli_app.py**: Command-line interface application for running the app without a UI.
- **template/**: Directory for HTML templates and other assets for the web app.
- **requirements.txt**: List of Python dependencies required for the project.
- **sample_prompts.md**: File containing sample prompts for generating image outlines.

## Demo

<video width="600" controls>
  <source src="./demo/demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Setup

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Copy the example environment file and configure it**:
    ```sh
    cp .env.example .env
    ```

## Usage

### Running the Web Application
To run the web application, execute:
```sh
python app.py
```

### Running the CLI Application

To use the CLI version, execute:

```sh
python cli_app.py
```

## License
This project is licensed under the MIT License.
