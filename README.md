
# ImageProcessingAPI




## Introduction

This Image Processing API allows users to perform various operations on images, such as rotation, resizing, conversion to grayscale, flipping, and thumbnail creation. It is designed to be both powerful and flexible, providing users with the ability to easily manipulate images according to their needs.
## API Endpoint

- URL: http://localhost:5000/process_image_sequence
- Method: POST
- Payload: Includes the image file and the operations to be performed, formatted in a specific structure.


## Code Structure

The API's backend is structured into three main components:

- main.py: Handles routing and initial request processing, including error checks.
- ProcessingService.py: Acts as an intermediary, managing the sequence of operations on images.
- ImageProcessor.py: Defines the core operations, with each class dedicated to a specific image manipulation task.
## Prerequisites

Python: Ensure you have Python installed on your system. This API requires Python 3.x. You can download Python from the official website: python.org.
## Setting Up the Environment

1. Install Python:

- Download and install Python from python.org. During the installation, make sure to select the option to add Python to your system's PATH.
2. Create a Virtual Environment:

- Open a command line interface (CLI) and navigate to the project's root directory.
- Run the following command to create a virtual environment named venv:
**python -m venv venv**

- This creates a new directory venv in your project folder, containing the virtual environment.

3. Activate the Virtual Environment:

- Activate the virtual environment by running:
On Windows:

**.\venv\Scripts\activate**

On macOS and Linux:

**source venv/bin/activate**

- Once activated, your command line will usually show the name of the virtual environment, indicating that all Python and pip commands will now operate within this isolated environment.


4. Install Dependencies:

- Ensure the requirements.txt file is present in the project's root directory. This file contains a list of all packages needed to run the API. (It should already be in the API folder)
- Install the required packages by running:
**pip install -r requirements.txt**

- This command reads the requirements.txt file and installs all the listed packages along with their dependencies.
## Starting the API Server

1. Run the Server:

1. Run the Server:

With the virtual environment activated and dependencies installed, you can start the API server by running:

**python main.py**


This command executes the main.py script, which should start the Flask application and listen for incoming requests.
Verify:

Once the server starts, it will typically print a message indicating it is running and listening on a specific port (usually http://127.0.0.1:5000 for Flask applications).
You can now send requests to the API endpoint http://localhost:5000/process_image_sequence as specified in the documentation.
## Using Test Files

There a couple of ways to interact with the API server. It is listed in the main documentation. The first is to use the command line and the curl command. The second way is to write a Python file or any file that can send requests to the API endpoint.

In this API there are tests files that can be used to interact with the API directly. 

### CommandLineClient.py

The easiest way is to use CommandLineClient.py included in the ClientSide folder of the repo. Run the Python file in another terminal and interact with the prompts there. The program will run on the command line with guided instructions on how to process the image.


### PythonTestFiles

There are a set of Python files and a folder called differentformatting. The Python files represent the different scenarios you can test out. 

- **generic.py** : A generic request.
- **missingparameter.py**: Sends request with a missing parameter
- **morethan5.py**: Sends a request where the image is greater than 5 MB
- **morethan20op.py**: Sends a request where there are more than 20 operations.
- **noimage.py**: Sends a request where there are no images.
- **nooperations.py**: Sends a request where there are no operations. 

Of course it could simply be one file and the user edit the files, but for the purposes of easier time these are the scenarios you can choose to test. Run the respective Python file to test out the different scenarios.

As for the differentformatting folder, this contains a variety of images in different formats to test out. The only one that stands out is the morethan5MP.png which is used to test whether an image of 5 MB will be accepted by the API (it will not).


AGAIN: You do not need to run these Python test files. The API has to be running, but the way to send a request is up to you. Send it to the correct endpoint with the correct payload and the API should be able handle it correctly.
