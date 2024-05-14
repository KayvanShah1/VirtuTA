# AI Virtual Teaching Assistant
Welcome to AI Virtual Teaching Assistant! This project is designed to provide assistance in virtual teaching environments using AI technologies.
> DSCI 560 Spring 24 Final Project

<iframe width="560" height="315" src="https://www.youtube.com/embed/zmJYuHgZtFs?si=Iemyo5ZOKlyWo5b4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

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

Now you're ready to run the AI Virtual Teaching Assistant!!

## Authors
1. [Kayvan Shah](https://github.com/KayvanShah1) | `MS in Applied Data Science` | `USC`
1. [Soma Meghana Prathipati](https://www.linkedin.com/in/soma-meghana-p-/) | `MS in Applied Data Science` | `USC`
1. [Shreyansh Baredia](https://github.com/SHREYANSH-BARDIA) | `MS in Applied Data Science` | `USC`

#### LICENSE
This repository is licensed under the `BSD 5-Clause` License. See the [LICENSE](LICENSE) file for details.

#### Disclaimer

<sub>
The content and code provided in this repository are for educational and demonstrative purposes only. The project may contain experimental features, and the code might not be optimized for production environments. The authors and contributors are not liable for any misuse, damages, or risks associated with the direct or indirect use of this code. Users are strictly advised to review, test, and completely modify the code to suit their specific use cases and requirements. By using any part of this project, you agree to these terms.
</sub>