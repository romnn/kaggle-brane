## Kaggle package for brane


#### Prerequisites

In order to use the Kaggle’s public API, you must **authenticate using an API token**.
From the site header, click on your user profile picture, then on “My Account” from the dropdown menu.
This will take you to your account settings at https://www.kaggle.com/account.
Scroll down to the section of the page labelled API.
To create a new token, click on the **“Create New API Token”** button. This will download a fresh authentication token onto your machine.

Furthermore, if you attempt to interact with a specific competition (e.g. download it or submit), you **must enter the challenge and accept the rules via the kaggle website** with the same account you use with the API first!

#### Usage

First, import the brain package so that you can use it in the REPL:
```bash
brane import romnn/kaggle-brane
brane push kaggle 1.0.0
```

Subsequently, the `kaggle` can be imported in your brane scripts to interact with kaggle
```python
import kaggle;
```

#### Local development

```bash
# this will use the kaggle API with your local kaggle credentials at ~/.kaggle/kaggle.json if available 
COMPETITION=web-traffic-time-series-forecasting DESTINATION=. ./run.py competitions download
```

#### Build the brane package

```bash
brane remove kaggle && brane build container.yml
brane test kaggle
```
