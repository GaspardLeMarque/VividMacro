# Vivid Macro

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

- [Project Description](#project-description)
- [Starting the Application with Docker](#starting-the-application-with-docker)
- [Configuring FRED API Access](#configuring-fred-api-access)
- [License](#license)

## Project Description

Vivid Macro is an open-source project designed to simplify access 
to macroeconomic data from various sources. With support for fetching 
data directly from the FRED (Federal Reserve Economic Data) database 
and ASCII datasets from Tealbook (previously Greenbook), it serves as a 
comprehensive tool for macroeconomists and data analysts. 
The platform offers an intuitive interface for generating Vector 
Autoregression (VAR) visualizations, enabling users to easily explore 
and understand the dynamics among various economic indicators.
Developed with Flask and delivered as a Docker container, Vivid Macro
makes macroeconomic analysis accessible for personal and educational 
purposes.





## Starting the Application with Docker

VividMacro is a Docker-packaged Flask web application available
on Docker Hub. This guide shows how to start it with Docker.


### Prerequisites

Download and install Docker Desktop for your operating system to proceed, 
you can find it on [Docker's official website](https://www.docker.com/products/docker-desktop). 

### Pulling the Docker Image

To download the image, execute the following command 
in your terminal or command prompt:
```shell
docker pull gaspardlemarque/vivid-macro:dev
```

### Running the Application

With the Docker image downloaded, you can run the application by executing:
```shell
docker run -p 4000:5000 gaspardlemarque/vivid-macro:dev
```

This command initiates a Docker container from the `vivid-macro` image. 
Here, `-p 4000:5000` maps port 4000 on your local machine to port 5000 
inside the Docker container, which is the default port Flask listens on.
The application is now accessible in your local environment 
at `http://localhost:4000`. 

## Configuring FRED API Access

To retrieve macroeconomic data from the FRED (Federal Reserve Economic Data) database through Vivid Macro, you'll need to obtain and configure an API key.

### Obtaining a FRED API Key

1. Visit the FRED API documentation page at [https://fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html).
2. If you don't already have an account on the FRED website, you will need to create one. Click on "My Account" button and follow the instructions.
3. Once you have a FRED account, log in and generate a new API key. This key is unique to your account and will be used to authenticate your requests to the FRED API via Vivid Macro.

### Configuring Your Vivid Macro Project

After obtaining your API key, you'll need to configure Vivid Macro to use it:

1. In the root directory, create a file named `.env`. It will be used to store environment variables, including your FRED API key.

2. Open the `.env` file with your favorite text editor.

3. Add a line for the FRED API key in the following format:
    ```
    API_KEY='your_api_key_here'
    ```
    Replace `'your_api_key_here'` with the actual API key you obtained from FRED. Ensure there are no spaces before or after the equals sign.

4. Save your changes. Vivid Macro is now configured to authenticate with the FRED API using your API key.

## Preview
[preview.webm](https://github.com/GaspardLeMarque/VividMacro/assets/16758426/4a598fc3-6e8d-442e-a826-589d30649d82)

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the `LICENSE` file for more details.
