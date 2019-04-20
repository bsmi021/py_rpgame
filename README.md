# RPG Game Demo
---
This project provides the various resources which are used to run a demonstration of Real-Time Open Architecture using SAS Event Stream Processing. Below you will find instructions on how to setup many of the components. 

![Image](https://github.com/bsmi021/rpgame2/blob/master/images/001_sas_rpgdemo_integration_architecture.png)

*The intention of this project is not to teach you how to use any of the technologies below, it's strongly advised that you review information from the following links to gain clarity.*

  * [SAS Event Stream Processing 5.2](https://documentation.sas.com/?cdcId=espcdc&cdcVersion=5.2&docsetId=espov&docsetTarget=home.htm&locale=en)
  * [SAS Viya (various)](https://documentation.sas.com/?docsetId=helpcenterdefault&docsetTarget=surfedin.htm&docsetVersion=1.0)
  * [Apache Kafka](https://kafka.apache.org/)
  * [Apache NiFi](https://nifi.apache.org/)
  * [Apache Flume](https://flume.apache.org/)

## Project Structure

* [avro_schemas](https://github.com/bsmi021/rpgame2/tree/master/avro_schemas) - contains the various AVRO schemas which are used by NiFi for publishing events to SAS ESP<br><br>
* [data](https://github.com/bsmi021/rpgame2/tree/master/data) - contains the data files used by the Python client for both players as well as inventory items. Take time to understand these files prior to modifying them as they can cause the demo to run unexpectingly<br><br>
* [flume_config](https://github.com/bsmi021/rpgame2/tree/master/flume_config) - contains the Apache Flume configuration file for consuming Kafka and publishing raw data to HDFS *If you use this configuration please ensure you change the source bootstrap servers host address (5-total sources)*<br><br>

* [nifi_scripts](https://github.com/bsmi021/rpgame2/tree/master/nifi_scripts) - this directory provides the embedded Python code used in the ExecuteScript NiFi processors
  * [nifi_rpg_game_demo_flow.xml](https://github.com/bsmi021/rpgame2/tree/master/nifi_scripts/nifi_rpg_game_demo_flow.xml) - this file contains the NiFi processing group for the demonstration. All of the IP addresses have been set to a generic IP, you must edit the Kafka and ESP processors (orange and blue repectively) to the IP addresses which match your environment. This file can be imported into your NiFi environment using the "Import Template" action.
  
* [rpggame](https://github.com/bsmi021/rpgame2/tree/master/rpggame) - directory contains the source code for the RPG Game Simulator, 
  * [utils.py](https://github.com/bsmi021/rpgame2/blob/master/rpgame/utils.py) - You must set the *kafka_bootstrap_server* variable on Line 47 to the IP address of your Apache Kafka bootstrap server prior to running the main Python program

* [sas_esp](https://github.com/bsmi021/rpgame2/tree/master/sas_esp) - directory contains the ESP project files for the demo and includes the scripts for the embedded MAS modules. 
  * [rpggame_demo_dataflow.xml](https://github.com/bsmi021/rpgame2/blob/master/sas_esp/rpggame_demo_dataflow.xml) - this file provides the main SAS ESP project for the demo environment. This project requires Python be installed and configured on your SAS ESP server. See [SAS® Help Center: Configuring Python for SAS Event Stream Processing](https://go.documentation.sas.com/?docsetId=masag&docsetTarget=n1fn07cwjn2w65n16njwlbpgo5fk.htm&docsetVersion=5.2&locale=en#n18c6khet91vznn1hgpnj9b1h13x) for more information on setting up Python for SAS ESP.
Additionall the *data/models* folder contains the Python ML model file for the *rpggame_demo_ml* ESP project.
  * [rpggame_demo_ml.xml](https://github.com/bsmi021/rpgame2/blob/master/sas_esp/rpggame_demo_ml.xml) - this file contains a SAS ESP project which executes a Python ML model as well as SAS ESP online ML model. This requires that you deploy the [data/models/p_attack_lr_v1.sav](https://github.com/bsmi021/rpgame2/blob/master/sas_esp/data/models/p_attack_lr_v1.sav) file to the SAS ESP server and ensure the path is set correctly in the project's MAS module.

* [viya](https://github.com/bsmi021/rpgame2/tree/master/viya) - contains two assets for SAS Viya
  * [cas_load_stream.sas](https://github.com/bsmi021/rpgame2/blob/master/viya/cas_load_stream.sas) - this file will create a new CAS session, then load the *loadStreams* actionset followed by subscribing to the ESP model. *Note you will need to set the values for the CAS controller and ESP server*
  * [rpggame_combat_dashboard.json](https://github.com/bsmi021/rpgame2/blob/master/viya/rpggame_combat_dashboard.json) - this file needs to be imported into the SAS Viya Content server (you will need admin permissions), *Note ensure that the cas_load_stream.sas code is executed first to ensure that the CAS Table exists before importing*

* [main.py](https://github.com/bsmi021/rpgame2/tree/master/main.py) - this is the main entry point into the Python program which runs the RPG Game Simulator. You can tweek the following variables (lines 21-23):
  * fight_count - this is set to 50 and will spawn 50 fights simultaneously, tweak this number as needed but note raising this number could cause lock-ups on the host running the simulator
  * send_to_kafka - this is set to *true* by default, setting this to false will output all messages to the console and will not send them to your Kafka server
 

## Infrastructure:
  The infrastructure for this demo environment uses a combination of a standing Hadoop Distribution (which is not required, you may omit it from your deployment and stop NiFi processes), a few generally available Docker images, as well as a SAS Event Stream Processing (v5.2) setup and SAS Viya 3.4 setup. Instructions for setting up SAS Viya and SAS ESP are outside the scope of this project; however, the demonstration assets have been included to deploy to your own demo environment.
    
* Docker Containers
  * [Apache NiFi](https://hub.docker.com/r/apache/nifi/) - The general Docker image for Apache NiFi works perfectly fine; however, you'll need to mount a local directory (easiest method) to the running container in order to move assets into it. 
  
    *Note: change the local directory value, as well you may need to change the host port depending on your existing host port usage*<br>
    `docker run --name rpg_nifi -d -it -v (local directory):/usr/share -p 8080:8080 apache/nifi:1.6.0`
    
    Follow the instructions at [Setting Up Apache NiFi to Run with SAS Event Stream Processing](https://go.documentation.sas.com/?cdcId=espcdc&cdcVersion=5.2&docsetId=espcases&docsetTarget=p1pyldv5uiyl2wn15ofigbx6qbd1.htm&locale=en) for instructions on installing the SAS ESP processors to Apache NiFi.
    
  * [Apache Kafka](https://hub.docker.com/r/landoop/fast-data-dev/) - I like to use the **landoop/fast-data-dev** image for Apache Kafka as it has a full-fledged Kafak installation that starts up very quickly, it also includes a lot of extras which make it worth running.
  
    *Note: you will replace the ADV_HOST parameter with the IP address of the host you're running the containter from, additionally modify the exposed ports per your host port availability.<br>
    `docker run --name rpg_kafka -it -p 2181:2181 -p 8081:8081 -p 8082:8082 -p 8083:8083 -p 9092:9092 -e ADV_HOST=(your host IP) landoop/fast-data-dev` 


## ESP Model Design
![Image](https://github.com/bsmi021/rpgame2/blob/master/images/001_sas_rpgdemo_stream_process.png)

