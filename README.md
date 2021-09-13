<!-- PROJECT LOGO -->
<p align="center">

  <h2 align="center">QR-code-attendance</h2>

  <p align="center">
    A Project for making attendance system easy and secure
    <br />
    <a href="http://miltonbhowmick.pythonanywhere.com/qrcodeattendance/">View Demo</a>
    ·
    <a href="https://github.com/Miltonbhowmick/QR-code-attendance/issues">Report Bug</a>
    ·
    <a href="https://github.com/Miltonbhowmick/QR-code-attendance/issues">Request Feature</a>
  </p>
</p>

<!-- ABOUT THE PROJECT -->
## About The Project

<strong>College & School (X)</strong>
<br>
<strong>This project is only for university students.</strong>
<br>
This is a project based on attendance system. I have tried to figure out a way to take attendance through android mobile. A QR code will be generated according to selected course code by teacher. Then he/she will show the generated QR code to projectile screen. Students will scan QR code and their names will be shown in the screen board with real time. 

Objectives:
* To convert the analog system to digital system.
* To save time to take class attendance. 
* To reduce cheating done by students.

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites
Be sure you have the following installed on your development machine:

* Python >= 3.7
* Django >=2.1
* Git
* pip
* Virtualenv (virtualenvwrapper is recommended)

### Installation

To setup a local development environment:

Create a virtual environment in which to install Python pip packages. With [virtualenv](https://pypi.python.org/pypi/virtualenv),
```bash
virtualenv venv            # create a virtualenv
source venv/bin/activate   # activate the Python virtualenv 
```

or with [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/),
```bash
mkvirtualenv -p python3 {{project_name}}   # create and activate environment
workon {{project_name}}   # reactivate existing environment
```

Clone GitHub Project,
```bash
git clone https://github.com/Miltonbhowmick/QR-code-attendance.git
cd  QR-code-attendance
```

Install development dependencies,
```bash
pip install -r requirements.txt
```

Migrate Database,
```bash
python manage.py migrate
```

Run the web application locally,
```bash
python manage.py runserver # 127.0.0.1:8000
```

Create Superuser,
```bash
python manage.py createsuperuser
```

<!-- CONTRIBUTING -->
## Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact
Linkedin - [@miltonbhowmick](https://www.linkedin.com/in/milton-chandro-bhowmick-52a288b6/)




