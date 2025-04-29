Project Title: Cloud-Native Image Analysis API

Description: It is a simple web API using TensorFlow/MobileNetV2. It was deployed on GCP Cloud Run via Docker to classify select uploaded images. 

Features: A pretrained model "imageNET" was used to clasiffy these images. It will use the pretrained model and the endpoint /predict that accepts POST requests with an image file. From there, the model will return its top three predictions in a JSON format. 

List of technologies used: Python, Flask, TensorFlow/Keras (MobileNetV2), Docker, GCP (Cloud Run, Artifact Registry).

Local set up:
    
    Step 1: Make sure all libraries are properly installed. It is recomended to use Anaconda or create a virtual envorinment. For myself, I created a virtual environment. The libraries needed are tensorflow, Pillow, numpy, and requests.

    Step 2: Collect some simple images online. For myself, I collected some simple images of cats and dogs. 

    Step 3: We must load the pre-trained model. For this project, "imageNET" was used. Create a python file "predict_image.py" that loads the model needed. I also created two functions in the python file. One that preprocesses the image and one that predicts the image class. 
    Note: Do not worry if there are yellow squigly lines under the tensorflow.keras libraries if you are using vscode. The libraries will still run with no problem as long as you have installed the tensorflow library.

Web API Set up:
    
    Step 1: Install the library Flask.

    Step 2: Create a python file app.py. This will act as our simple web API. This file will also include setting up the /predict endpoint that will listen for POST requests, loads the model, creates a pipeline to preprocess the images, and handles the prediction. It should be set up so that the predictions are generated in a JSON file format.

Docker Container Set up:
    
    Step 1: Make sure that Docker Desktop is installed.

    Step 2: Create a Docker file in the project directory.

    Step 3: Run this bash command in the project directory: "docker build -t image-classifier-api ." This creates a docker image and tags it as image-classifier-api.

    Step 4: Now we can the Docker container with this bash command: "docker run -p 5001:5000 -d image-classifier-api". This maps the port 5001 on the host machine to the port 5000 on the container. The "-d image-classifier-api" allows for the container to run in the background.

Cloud Deployment:
    
    Step 1: For this project, I chose Google Cloud Platform as my cloud provider. This will allow me to host the docker container online. Create a Google Cloud Platform account. 

    Step 2: Install the Google Cloud SDK so that the gcloud tool is installed. 

    Step 3: Log in via the CLI with the command "gcloud auth login".

    Step 4: Create a project through the web interface so that we have a Project ID.

    Step 5: Use this bash command in the CLI to indicate which project should be used: "gcloud config set project ###########" 
            Note: Replace the ############ with the Project ID received in step 4.

    Step 6: Run this command to enable the Cloud Run API and Artifact Registry API: "gcloud services enable run.googleapis.com artifactregistry.googleapis.com"

    Step 7: Create a registry for the Docker image with this command: "gcloud artifacts repositories create image-repo --repository-format=docker --location=us-central1 --description="Docker repository for image classifier"".

    Step 8: Configure the Docker auth with this command: "gcloud auth configure-docker us-central1-docker.pkg.dev".

    Step 9: Tagging the Docker image: "docker tag image-classifier-api us-central1-docker.pkg.dev/#########/image-repo/image-classifier-api:latest"
            Note: Replace the ######### with the cloud project id.

    Step 10: Push the Docker image: "docker push us-central1-docker.pkg.dev/###########/image-repo/image-classifier-api:latest"
            Note: Replace the ######### with the cloud project id.

    Step 11: Deploy the registry from artificial registry to cloud run with this command: "gcloud run deploy image-classifier-service --image=us-central1-docker.pkg.dev/############/image-repo/image-classifier-api:latest --platform=managed --region=us-central1 --port=5000 --memory=1Gi --allow-unauthenticated".
            Note: Replace the ########## with the cloud project id.

Example:

Make sure that the image that you would like to post is in the project directory.

Run: "curl -X POST -F "file=@cat_2.jpg" Directory given by the cloud deployment/predict"

Note: This will post an example of a cat photo that I have in the project directory. The pretrained model will analyze the photo, and will return a list of what the image could be in a JSON format. 

Result:

{
  "predictions": [
    {
      "label": "tabby",
      "score": 0.8648473620414734
    },
    {
      "label": "Egyptian_cat",
      "score": 0.04398898035287857
    },
    {
      "label": "tiger_cat",
      "score": 0.018525511026382446
    }
  ]
}
