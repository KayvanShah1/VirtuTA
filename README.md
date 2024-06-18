# VirtuTA: AI-enabled Virtual Teaching Assistant
Welcome to VirtuTA, an innovative project designed to build a fully functional electronic/virtual teaching assistant for university courses. VirtuTA is designed to enhance the educational experience by providing immediate, accurate, and context-aware responses to student queries. This project leverages the latest advancements in machine learning, natural language processing, and AI to support both students and instructors in an academic setting.

## Introduction
In the ever-evolving landscape of education, the demand for effective and efficient teaching tools has never been greater. `VirtuTA` aims to meet this demand by providing a virtual teaching assistant capable of handling a variety of tasks, from answering student queries to providing detailed feedback and support. This project is a culmination of the skills we've honed through numerous laboratory assignments and the additional expertise we've gained in domain-specific functions.

Our platform integrates with various educational tools and data sources to provide a seamless user experience. This project is part of a larger initiative to explore and implement cutting-edge technology in educational environments.

### Demo Video
**Click on the image below to view the video**

[![PRESENTATION VIDEO](https://img.youtube.com/vi/zmJYuHgZtFs/maxresdefault.jpg)](https://www.youtube.com/watch?v=zmJYuHgZtFs)

## Project Overview
The goal of this semester's final project is to develop a complete working solution for electronic/virtual teaching assistants, dubbed VirtuTA. Our approach is rooted in a structured and incremental development process, ensuring that we build a platform that is not only functional but also scalable and adaptable to different educational needs.
> DSCI 560: Data Science Professional Practicum Final Project

### Key Features
- **Automated Login and Real-time Data Collection**: VirtuTA supports automated login to platforms like Piazza and web-based forums, ensuring real-time data collection and interaction.

- **Context-Aware Responses**: Our system utilizes advanced embedding algorithms to match user queries with the most relevant answers, incorporating both static and dynamic content.

- **Multimodal Responses**: VirtuTA can include images and videos in its responses, enhancing the explanatory power and engagement of the assistant.

- **Integration with External Tools**: The assistant can integrate with tools like OpenAI and HuggingFace for enhanced language processing capabilities.

- **Logistical Support**: Provides timely updates and responses related to course logistics, helping students stay informed and organized.

- **Automated Communication:** VirtuTA streamlines interactions between students and instructors by providing automated responses to common queries, facilitating discussion forums, and offering personalized assistance.

- **Assignment Management:** Manage assignments seamlessly, including creation, distribution, grading, and feedback provision.

- **Content Delivery:** Easily upload and organize course materials such as lecture slides, readings, and multimedia content for accessible anytime, anywhere learning.

- **Student Support:** Personalized support through Q&A sessions, study guides, tutoring, and additional resource recommendations.

- **Analytics and Insights:** Analyze student interactions and performance data to generate valuable insights for improving teaching strategies and tracking student progress.

## Agentic Workflow Integration

In addition to the core features, VirtuTA incorporates an agentic workflow, inspired by _Relevance-Augmented Generation_ (RAG) principles. This workflow enhances VirtuTA's capabilities by integrating powerful data retrieval and generation techniques, ensuring that the assistant provides accurate and contextually relevant responses.

We have created a `multimodal RAG` using `Langchain`, powered by `Google Gemini`. For __context awareness__, we utilize two vector stores with `Mongo Atlas Vector Search` for _content-based_ and _logistics-based_ queries. VirtuTA generates detailed and comprehensive answers with snapshots from slides, timestamps, links to videos, and original sources. Additionally, it queries the YouTube API for content-based queries to provide the best videos explaining the concepts students are seeking.

This agentic workflow is directly integrated into `Piazza`, a popular forum used by students and teachers at many universities. It leverages the Piazza API to query unanswered and unresolved questions, providing answers directly within the thread.

We invite you to explore VirtuTA and join us on this exciting journey towards revolutionizing the educational experience. Your feedback and contributions are invaluable as we strive to make VirtuTA a state-of-the-art virtual teaching assistant.

> [!INFO]
> Piazza Classroom Invitation: [Click here](https://piazza.com/usc/summer2024/dsci560)
> Classroom may or may not be active as project is currently not being maintained

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

## Conclusion

VirtuTA is poised to revolutionize the way students interact with educational content and support systems. By integrating advanced AI techniques with robust educational frameworks, we aim to provide a highly effective, engaging, and supportive learning environment. Stay tuned for our weekly progress updates and final project demonstration!

Thank you for your interest in **VirtuTA**!

## Authors
1. [Kayvan Shah](https://github.com/KayvanShah1) | `MS in Applied Data Science` | `USC`
1. [Soma Meghana Prathipati](https://www.linkedin.com/in/soma-meghana-p-/) | `MS in Applied Data Science` | `USC`
1. [Shreyansh Baredia](https://github.com/SHREYANSH-BARDIA) | `MS in Applied Data Science` | `USC`

#### Team and Credits
This project is a collaborative effort by a team of dedicated students from the __University of Southern California's__ **MS** in **Applied Data Science** program. Special thanks to _Mihika Gaonkar_, _Prathamesh Lonkar_, _Mithesh Ramachandran_, _Hritik Bansal_, and _Suma Sree Gottipati_ for their contributions to demo video.

#### LICENSE
This repository is licensed under the `BSD 5-Clause` License. See the [LICENSE](LICENSE) file for details.

#### Disclaimer

<sub>
The content and code provided in this repository are for educational and demonstrative purposes only. The project may contain experimental features, and the code might not be optimized for production environments. The authors and contributors are not liable for any misuse, damages, or risks associated with the direct or indirect use of this code. Users are strictly advised to review, test, and completely modify the code to suit their specific use cases and requirements. By using any part of this project, you agree to these terms.
</sub>