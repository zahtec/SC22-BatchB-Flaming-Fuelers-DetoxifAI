# ☠️ DetoxifAI

_Detecting venemous or posionous species in the wild_

## 👀 What is it?

DetoxifAI's main goal is protect people who arent knowledgable about the species they may encounter. For exmaple if you were walking in the woods and you wanted to check if a mushroom was edible or not, you could easily use DetoxifAI to find information and said species. Currently it focuses on commonly found California snake and mushrooms species.

## ⚙️ How does it work?

DetoxifAI uses the [YoloV5](https://github.com/ultralytics/yolov5) computer vision model to classify certain species using images uploaded by the user. Our AI was created like so:

-   Web scraping images of specific species of mushroom and snake we wanted to classify using [serp](https://serpapi.com)
-   Label and filter through data found so we can get the images we will use for **training our model**
-   Export our data and **augment it** so that it creates a stronger final model
-   Train the model using [Google Colab](https://colab.research.google.com) and [Kaggle](https://www.kaggle.com) for superior speed GPUs. Adjusting hyperparameters and input data accordingly
-   Create and frontend and also a backed using [flask](https://flask.palletsprojects.com) for serving it to users, while also linking up our backend to [YoloV5](https://github.com/ultralytics/yolov5) and classifying each image uploaded by a user

## 🚀 Usage

To use DetoxifAI first clone this repo by running

```sh
git clone https://github.com/zahtec/SC22-BatchB-Flaming-Fuelers-DetoxifAI.git
```

Then change your terminal directory to the `SC22-BatchB-Flaming-Fuelers-DetoxifAI` folder and run (assuming you already have [Python](https://www.python.org/) installed)

```sh
python ./app/main.py
```

Or, if you have multiple versions of python installed

```sh
python3 ./app/main.py
```

This will intiate a flask server that will bind the URL to `localhost:1234`. Open your browser, go to this URL, and proceed to upload your images & get your results!

This project is also able to run on [CoCalc](https://cocalc.com/) and has been tested on there

## 📈 Stats

More information can be found on this projects about page on the frontend, if you would like to view it, please follow the instructions above ([🚀 Usage](#-usage))

### Final precision and recall

**Precision:** `~0.97`

**Recall:** `~0.98`

### Confusion Matrix and other images

[![Deploy a Web Project with Flask](https://img.youtube.com/vi/JUb-PpejA7w/0.jpg)](https://youtu.be/JUb-PpejA7w 'Deploy a Web Project with Flask')
