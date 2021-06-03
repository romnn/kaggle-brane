## Kaggle for brane

This [brane](https://github.com/onnovalkering/brane) package provides wrappers for the [Kaggle](https://www.kaggle.com/) API for easy interaction when working with data pipelines and machine learning models in `brane`.

#### Prerequisites

In order to use the Kaggle’s public API, you must **authenticate using an API token**.
From the site header, click on your user profile picture, then on “My Account” from the dropdown menu.
This will take you to your account settings at https://www.kaggle.com/account.
Scroll down to the section of the page labelled API.
To create a new token, click on the **“Create New API Token”** button. This will download a fresh authentication token onto your machine.

Furthermore, if you attempt to interact with a specific competition (e.g. download it or submit), you **must enter the challenge and accept the rules via the kaggle website** with the same account you use with the API first!

#### Usage

First, import the brain package from this repository:
```bash
brane import romnn/kaggle-brane
```

You also need to push the package to be able to import it in your remote session or jupyterlab notebook:
```bash
brane push kaggle 1.0.0
```

Subsequently, the `kaggle` package can be imported in your `brane` scripts to interact with kaggle.
You can try it out with the `brane --debug repl` as well:
```python
import kaggle;
let test := download_competition("comp-name", "./data", "kaggle_username", "kaggle_key", false, true);
```

#### Documentation

At the moment, only `download_competition` is considered production ready, but more API calls have been implemented to cover the full Kaggle API for an easy integration with your `brane` projects.

The easiest way to learn about the available functions, parameters and return types, is to explore the package with
```bash
brane --debug test kaggle
```
after you imported it.

This will give you a list of all the available functions and show you the parameters in the order they are expected. When you supply valid credentials and the desired parameters  you will be able so see the output of the function.

#### Local development

It is recommended to develop locally by using environment variables and the `run.py` python script. This will use the Kaggle API with your local kaggle credentials at `~/.kaggle/kaggle.json` if available 

```bash
COMPETITION=web-traffic-time-series-forecasting DESTINATION=. ./run.py competitions download
```

#### Build the brane package

After local development, you can build and push the `brane` package with the included `Makefile` command:
```bash
make build

# check that the package was updated and test it
brane list
brane --debug test kaggle
```
