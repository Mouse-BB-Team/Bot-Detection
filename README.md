![release-date](https://img.shields.io/date/1601397036?label=release-date&style=flat-square)
![code-size](https://img.shields.io/github/languages/code-size/Mouse-BB-Team/Bot-Detection?style=flat-square)
![tag](https://img.shields.io/github/v/tag/Mouse-BB-Team/Bot-Detection?style=flat-square)
[![Website][web-shield]][web-url]
![Contributors](https://img.shields.io/github/contributors/Mouse-BB-Team/Bot-Detection?color=yellow&style=flat-square)
![Last-commit](https://img.shields.io/github/last-commit/Mouse-BB-Team/Bot-Detection?style=flat-square)
![Languages](https://img.shields.io/github/languages/count/Mouse-BB-Team/Bot-Detection?style=flat-square)
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://mouse-bb.pl">
    <img src="https://user-images.githubusercontent.com/50112357/83871505-761b7080-a730-11ea-8a93-c5429244d6db.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Mouse Behavioral Biometrics</h3>

  <p align="center">
Protection of Web applications with behavioral biometrics.
<br>
<i>Bot detection module</i>
    <br />
    <a href="https://mouse-bb.pl">Visit Site</a>
    ·
    <a href="https://github.com/Mouse-BB-Team/Bot-Detection/issues">Report Bug</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
  * [Project structure](#project-structure)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)
* [Authors](#authors)
* [Appendix](#appendix)



<!-- ABOUT THE PROJECT -->
## About The Project

This project was created in the manner of preparing the bachelor's degree thesis on AGH University of Science and Technology, Department of Computer Science, Electronics and Telecommunications.
The serialized data, collected from the [previous module](https://github.com/Mouse-BB-Team/Data-Collection) is used as the input dataset for [InceptionV3](https://tfhub.dev/google/imagenet/inception_v3/feature_vector/4) Machine Learning model, imported from [tensorflow hub](https://tfhub.dev/).
The idea is to perform transfer learning techniques to produce a model able to distinguish Web bots and humans on real commercial websites.


### Built With

* [Python](https://www.python.org/) – language used
* [Tensorflow](https://www.python.org/) – Machine Learning framework
* [Numpy](https://numpy.org/) – scientific calculation library
* [Pandas](https://pandas.pydata.org/) – data manipulation library
* [Pytest](https://docs.pytest.org/en/stable/) - framework for unit tests
* [Go](https://golang.org/) – language used to implement serializer
* [Protocol Buffers](https://developers.google.com/protocol-buffers) – used to serialize and store data

### Project structure
This section provides an information about project modules:

##### config
* *.env* – sample file with environmental variables that **MUST** be filled in order to run project locally
* *config.json* – contains path to .env file and public notifier variables
* *logger.config* – logger config
* *usersequence.proto* – protobuf schema for serialized data

##### ml_models
* *inceptionV3* – core machine learning model

##### utils
* *csv_writer* – module responsible for saving each model result to .csv file
* *deserializer* – module responsible for deserializing protobuf files that contains user mouse data
* *imgur_uploader* – module responsible for uploading plots to imgur in order to send it as url to slack webhook for live notifications
* *notification_jobs* – message informing about pending slurm job
* *preprocessing* – module for data preprocessing
* *prometheus_scripts* – shell scripts for operating on [Prometheus cluser](http://www.plgrid.pl/)
* *results_terminator* – terminates a global job result into the csv file
* *serializer* – go module to serialize data from database into the protofiles
* *slack_notifier* – custom notifier about pending, executing or finished/crashed job
* *statistics* – module to calculate statistics

##### root
* *main* – main script that runs the ML model
* *Makefile* – autoconfiguration for setting up the environment for the project

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Things you need to install before running:
```
python 3.8
pip3
go 1.14
```

### Installation
 
1. Clone the repo and change the directory to install requirements:
```sh
git clone https://github.com/Mouse-BB-Team/Bot-Detection.git
cd Bot-Detection/
pip3 install -r requirements.txt
```
> At this point you MUST set the variables in .env file


<!-- USAGE EXAMPLES -->
## Usage
Run script with:
```
python3 main.py -d <path_to_dataset> -t <count_of_ml_model_execution>
```


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Mail - <a href="mailto:mouse.bb.team@gmail.com">mouse.bb.team@gmail.com</a>

Project Link: [https://github.com/Mouse-BB-Team](https://github.com/Mouse-BB-Team)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

Our thesis supervisor:
* [Piotr Chołda - Website](http://home.agh.edu.pl/~cholda/)

Project made with PLGrid Infrastructure:
* [http://www.plgrid.pl/](http://www.plgrid.pl/)


## Authors

* **Kamil Kaliś** – [kamkali](https://github.com/kamkali)
* **Piotr Kuglin** – [lothar1998](https://github.com/lothar1998)

## Appendix
#### go serializer help for detailed usage
```
go run main.go -h
```

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[web-shield]: https://img.shields.io/website?style=flat-square&url=https%3A%2F%2Fwww.mouse-bb.pl
[web-url]: https://mouse-bb.pl


[license-shield]: https://img.shields.io/github/license/Mouse-BB-Team/Bot-Detection?style=flat-square
[license-url]: https://github.com/Mouse-BB-Team/Bot-Detection/blob/master/LICENSE
