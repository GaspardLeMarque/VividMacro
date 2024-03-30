# Vivid Macro

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

- [Project Description](#project-description)
- [Configuring FRED API Access](#configuring-fred-api-access)
- [License](#license)

## Project Description

Vivid Macro is an open-source project aimed at facilitating the access 
to macroeconomic data from various sources. It supports the retrieval 
of data from the FRED (Federal Reserve Economic Data) database 
and ASCII data sets from Tealbook (formerly known as Greenbook). 
Additionally, Vivid Macro offers a feature for creating 
Vector Autoregression (VAR) visualizations, facilitating the exploration
of relationships between monthly macroeconomic variables.

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
