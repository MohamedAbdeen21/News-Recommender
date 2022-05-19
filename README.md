# Dockered-news-scraper

This is a project to scrape as many news articles as possible, made for CSE321 Project Based Learning course. The list of websites currently include: Vox, BBC, Washington Post, New York Times, Fox News, The Guardian.

Adding new English websites to the project is as simple as adding the RSS feeds link to the `rssfeeds.py` file. It only supports websites that write dates in English or Numeric formats.

The project uses:
- scrapy framework for scraping and pipelining to a postgres database, scrapy offers many features out-of-the-box that other webscraping libraries do not. Such features include: logging, concurrency, codes handling, .. etc.
- airflow for orchesteration. Airflow provides many useful tools like masking passwords, access control, and web UI for monitorization. 
- Docker to make both installation and development easier. The project uses many services like postgres, pgadmin, airflow UI, an api for the database (to do), starting all of them with a single line saves a lot of effort.
- Flask api to integrate the database easily with ML models and the web frontend (to do).

The project was challenging on so many levels. Reducing the scraping time of hundreds of articles to a few minutes was the major challenge that led me to choose scrapy for the project, and scrapy took me some time to learn. The ability to continue working across the different OS on my device led me to Docker and Docker-compose; it saved me alot of trouble that I figured that I would include it in the final version of the project.

Features-to-implement:
- [] Create a better data model: The current data model only cares about saving the articles. A better model would be needed if the project was to be implemented in an application.
- [] Create an API for the database: As I mentioned earlier, this will make integrating the project easier. 
- [] Create a web frontend: I had a very basic frontend made with HTML, CSS and Flask in the [un-dockerized version](https://github.com/MohamedAbdeen21/NewNews) of the repo, but I decided not to include it in here until it is more mature.

---

## Installation and running
Just download [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/) from the official docker website, clone the repo, move to the top-level directory and run ```sudo docker-compose up``` or ```sudo docker compose up``` depending on your installation of docker compose.

This will start pgAdmin on port 8081 with login credentials `admin@admin.com` and `root`, start a server and add the following connection credentials:
```
hostname/address: pgdatabase
username: root
passwrod: root
```
leave everything else as it is.

It will also start Airflow UI on port 8080, use login credentials `airflow` and `airflow`, from there you should see the DAG of the scrapy scraper, enable it and watch the data start flowing into the database from pgAdmin.

The scraped data will persist even after system reboot.

With some simple knowledge in docker, you can change these login credentials and port numbers easily.

## Credits

These are some of the people helped me through their content to create this project:
- Scrapy: John Watson Rooney [YouTube](https://www.youtube.com/c/JohnWatsonRooney)
- Docker and docker-compose: [Alexey Grigorev](https://www.linkedin.com/in/agrigorev/?originalSubdomain=de) from [DataTalksClub](https://www.youtube.com/channel/UCDvErgK0j5ur3aLgn6U-LqQ) 

## DISCLAIMER

The project scrapes the data once a day to avoid overwhelming the websites. I am not responsible for any malicious activity that this project is used in. This project was made as a learning experience for me and not intended to be used in an industrial environment. 