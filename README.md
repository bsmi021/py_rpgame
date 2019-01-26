# RPG Game Demo

This project provides the various resources which are used to run a demonstration of Real-Time Open Architecture using SAS Event Stream Processing. Below you will find instructions on how to setup many of the components. *Note: it's expected that you have a SAS Viya and SAS ESP setup available and you understand how to use them.*

## Infrastructure:
  While the solution uses HDFS as a backing store, specific sections of the Apache NiFi resources can be disabled if you do not have access, or would like to change to a different storage platform.
* Docker Containers
  * Apache NiFi
  * Apache Kafka
