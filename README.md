<!-- logo -->
<a href="https://www.fantaso.de">
<img src="app/solarvibes/static/images/readme/fantaso.png" align="right" />
</a>

<!-- header -->
<h1 style="text-align: left; margin-top:0px;">
  IoT monitoring system
</h1>

> Monitor your plants, keep track of them environment and automate your water pump to irrigate them.

<!-- build -->
<!-- [![Build Status][travis-image]][travis-link] -->

<!-- banner -->
![banner][banner]

Project consists to allow users to manage irrigation system and monitor the growing plants/crop 24/7 with the help of an IoT system. The IoT system is composed by 3 main components:
* A **[Web application][app-repo-link]**: Allows users to register an account, view data collected from the sensors, `control water pump`, check `projected yields` and manage life-cycle of the growing plants/crop, `manage your sensors and pumps` and more...
* A **[Rest API][api-repo-link]**: Allows your wireless `pump controllers` & `sensors` (Raspberry Pi) to register and communicate with the web application to be able to send collected sensor data and receive instructions to control the water pump.
* A **[Raspberry Pi System Repository][raspberry-repo]**: Hardware that allow us to collect and control a remote wireless system. Which is composed, by a `weather sensor` (temperature, humidity & atmospheric pressure), `soil sensors` (moist, temperature & pH) and a `relay system` to control the water pump


## Installation:

### 1.Installing Web Application and Rest API

###### With ![docker][docker]:

1. Clone repository and go inside the repository folder "site-app-docker"
```sh
git clone https://github.com/Fantaso/site-app-docker
```

2. Build the docker images
```sh
docker-compose build
```

3. Initialize database used in the web app
```sh
docker-compose run --rm app python manage.py db init
```

4. Create the database mapping to migrate the database
```sh
docker-compose run --rm app python manage.py db migrate
```

5. Apply the migration changes detected to the database
```sh
docker-compose run --rm app python manage.py db upgrade
```

6. Add a test user to login into web app
```sh
docker-compose run --rm app python manage.py addusers
```

7. Add the crops data to the database
```sh
docker-compose run --rm app python manage.py addcrops
```

8. Add the licenses data to the database (licenses are string identifiers that allows to control which IoT sensors belongs to which user, and it is used for the IoT sensors to send the sensor data to the web app)
```sh
docker-compose run --rm app python manage.py addlicenses
```

9. Run the Docker containers
```sh
docker-compose up
```

### 2. Installing Raspberry Sensors
 [Visit Raspberry Pi Repository][raspberry-repo]
###### Visit  ![docker][docker]:


## Usage:
Once docker-compose is done downloading all images and none of the services failed after you have run the containers with `docker-compose up`


#### 1. Access Website
The web application should be running and you can access it in your web browser at _http://0.0.0.0:5000_, which will take you to the website and there in the navigation bar you can find the **login** link.


#### 2. Access App - Flask
Access the web app at _http://0.0.0.0:5000/app_
You will be prompt to enter **Username** and **Password**, which we have registered in `Step # 6` of the installation. Or you could register a new user following the link at the login page.

Login information:
- Username = fan@fantaso.de
- Password = **123456**


#### 3. Access Database Client - Adminer
Access the web app at _http://0.0.0.0:8080_
You will be prompt to enter **System**, **Server**, **Username**, **Password**, **Database** which has been pre-configured within the web app at `config.py` and the `docker-compose.yml` files.

Login information:
- System = **PostgreSQL**
- Server = **db**
- Username = **postgres**
- Password = **password**
- Database = **mydb**


#### 4. Communicate with your API - Flask
You can talk to the API if you have an API client like Postman in order to test and check how the process of registering a sensor or a pump controller into your web application.


1. Check if the API is working at:
  * GET
  * /agrimodule_api/


2. Check if IoT devices license is valid:
  * GET
  * /agrimodule_api/check/<identifier>


3. Register IoT devices and get credentials:
  * POST
  * /agrimodule_api/register
  * Payload:
    * `identifier` = str
    * `mac` = str
  * Response:
    * `username` = str
    * `password` = str


4. Send IoT devices data to web app database:
  * POST
  * /agrimodule_api/agrimodule/<agrimodule_id>/set-measurement
  * Payload:
    * `agrimodule_id` = int
    * `timestamp` = datetime
    * `soil_ph` = float
    * `soil_nutrient` = float
    * `soil_temp` = float
    * `soil_humi` = float
    * `air_temp` = float
    * `air_humi` = float
    * `air_pres` = float
    * `solar_radiation` = float
    * `batt_status` = int
    * `lat` = float
    * `lon` = float


5. Get an IoT specific measurement from the web app:
  * GET
  * /agrimodule_api/agrimodule/<agrimodule_id>/get-measurement/<measurement_id>


6. Get all data collected by an IoT device:
  * GET
  * /agrimodule_api/agrimodule/<agrimodule_id>/get-measurements


7. Unregister IoT devices:
  * GET
  * /agrimodule_api/unregister/<identifier>/<mac>



## Information:
| Technology Stack |  
| :- |:-:| :- |
| Python          | ![back-end][Python]                   | back-end |
| Flask           | ![web-framework][Flask]               | web-framework |
| SQLAlchemy      | ![orm][SQLAlchemy]                    | orm |
| PostgreSQL      | ![database][PostgreSQL]               | database |
| Docker          | ![container][Docker]                  | container |
| Docker-Compose  | ![container-manager][Docker-Compose]  | container-manager |
| Adminer         | ![database-client][Adminer]           | database-client |

## Maintainer
Carlos Rosas – [carlosmrosash][linkedin-profile] – fantaso.code@gmail.com



<!-- links -->
[github-profile]: https://github.com/fantaso/
[github-repo]: https://github.com/Fantaso/site-app-docker

[raspberry-repo]: https://github.com/Fantaso/agrimodule-smart-system/tree/master/AgrimoduleHardware/agrimodule_gw
[app-repo-link]: https://github.com/Fantaso/site-app-docker/tree/master/app
[api-repo-link]: https://github.com/Fantaso/site-app-docker/tree/master/app/solarvibes/agrimodule_api

[linkedin-profile]: https://www.linkedin.com/in/carlosmrosash/

[travis-link]: https://travis-ci.org/Fantaso/django-docker-travis.svg?branch=master
[travis-image]: https://travis-ci.org/Fantaso/django-docker-travis

<!-- images -->
[banner]: app/solarvibes/static/images/readme/mainUI.png
[Python]: app/solarvibes/static/images/readme/tech-python.png
[Flask]: app/solarvibes/static/images/readme/tech-flask.png
[SQLAlchemy]: app/solarvibes/static/images/readme/tech-sqlalchemy.jpg
[PostgreSQL]: app/solarvibes/static/images/readme/tech-postgresql.png
[Docker]: app/solarvibes/static/images/readme/tech-docker.png
[Docker-Compose]: app/solarvibes/static/images/readme/tech-dockercompose.png
[Adminer]: app/solarvibes/static/images/readme/tech-adminer.png
