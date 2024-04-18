# AI Virtual Teaching Assistant
Welcome to AI Virtual Teaching Assistant! This project is designed to provide assistance in virtual teaching environments using AI technologies.
> DSCI 560 Spring 24 Final Project

## Setup Instructions

### Python Development Environement
#### Conda Environment Setup

1. **Clone the Repository**: Clone this repository to your local machine.

2. **Navigate to Project Directory**: Open your terminal or command prompt and navigate to the root directory of the project.

3. **Create Conda Environment**: Run the following command to create a Conda environment using the provided `env.yml` file:

   ```bash
   conda env create -f env.yml
   ```

4. **Activate the Environment**: Activate the Conda environment using:

   ```bash
   conda config --set auto_activate_base false # To not activate "base" env by default
   conda activate gemini
   ```

5. **Update the environment**: If you already have a Conda environment cretaed updated it using the command below have the new dependencies installed
   ```bash
   conda env update --file env.yml --prune
   ```

__OR__

#### Virtual Environment (venv) Setup

1. **Navigate to Project Directory**: Open your terminal or command prompt and navigate to the root directory of the project.

2. **Create Virtual Environment**: Run the following command to create a virtual environment using `requirements.txt`:

   ```bash
   python -m venv gemini
   ```

3. **Activate the Virtual Environment**:
   - On Windows:
     ```bash
     gemini\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source gemini/bin/activate
     ```

### Setting Up Environment Variables

1. **Create Secrets Directory**: While in the root directory of the project, create a directory named `secrets`.

2. **Place GCP Service Account File**: Move your Google Cloud Platform (GCP) service account file into the `secrets` directory. Ensure it is named appropriately.

3. **Copy and Populate Environment Variables**:
   - Copy the `example.env` file provided in the project and rename it to `.env`.
   - Open the `.env` file and set the following variables:
     - `GCLOUD_SERVICE_ACCOUNT_KEY_PATH`: Path to your GCP service account file relative to the `secrets` directory.
     - `PROJECT_ID`: Your GCP project ID.
     - `PROJECT_LOCATION`: Location of your GCP project.
     - `MONGODB_URI`: URI for your MongoDB instance or database.

Now you're ready to run the AI Virtual Teaching Assistant!