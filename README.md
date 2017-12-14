# Quarantine

Version: *2.0*

Master branch: [![Build Status](https://travis-ci.org/cloudpassage/quarantine.svg?branch=master)](https://travis-ci.org/cloudpassage/quarantine)

Develop branch: [![Build Status](https://travis-ci.org/cloudpassage/quarantine.svg?branch=develop)](https://travis-ci.org/cloudpassage/quarantine)

Author: *Apurv Singh* - *apurva@cloudpassage.com*

Updates (v2): *Ash Wilson* - *awilson@cloudpassage.com*

## Purpose
This containerized application monitors the /v1/events endpoint in the Halo API,
looking for specific events.  If a targeted event is matched, the tool will
move the workload into the configured quarantine group.

## How it works
Targeted events are listed, one per line, in `/conf/target-events`.  Feel free
to alter the file and rebuild the container, or mount in the config file from a
persistent volume.  Event types produced by Halo can be found here:
https://api-doc.cloudpassage.com/help#event-types

When the end of the events stream is reached, this tool continue to query
until more events arrive.  If you do not set the `HALO_EVENTS_START`
environment variable, the tool will start at the beginning of the current day.

The quarantine group is defined with the `$QUARANTINE_GROUP_NAME` environment
variable.  If you don't define this environment variable, it is assumed to be
"Quarantine". You should configure the group in your Halo account before you run
this tool.  We recommend applying a firewall policy to the group that restricts
all outbound traffic, and only allows inbound traffic from Ghostports users.

## Prerequisites

* You'll need an account with CloudPassage Halo.
* Make sure that your policies are configured to create events on failure.
* You'll need an administrative (read + write) API key for your Halo account.
* You'll need to have Docker installed.
* Create a quarantine group in your Halo account, with the appropriately
restrictive firewall rules.

## Using the tool (containerized)
Clone the code and build the container:

        git clone https://github.com/cloudpassage/quarantine
        cd quarantine
        docker build -t cloudpassage_quarantine .

Set these environment variables:

| Variable            | Purpose                                              |
|---------------------|------------------------------------------------------|
| HALO_API_KEY        | Halo API key ID (administrative privileges required) |
| HALO_API_SECRET_KEY | Halo API key secret                                  |
| HALO_QUARANTINE_GRP | Halo quarantine group name                           |


Optionally, define these as well:

| Variable            | Purpose                                   |
|---------------------|-------------------------------------------|
| HALO_EVENTS_START   | ISO8601 timestamp for starting event      |


To run the container interactively (foreground):

        docker run -it \
        -e HALO_API_KEY=$HALO_API_KEY \
        -e HALO_API_SECRET_KEY=$HALO_API_SECRET_KEY \
        -e HALO_QUARANTINE_GROUP=$HALO_QUARANTINE_GROUP \
        cloudpassage_quarantine


If you want to run quarantine in the background, you can start it like this:

        docker run -d \
        -e HALO_API_KEY=$HALO_API_KEY \
        -e HALO_API_SECRET_KEY=$HALO_API_SECRET_KEY \
        -e HALO_QUARANTINE_GROUP=$HALO_QUARANTINE_GROUP \
        cloudpassage_quarantine


Use `docker ps` to make sure it's running.  The container logs will be updated
with the last event's timestamp after every batch runs, so running
`docker logs -f CONTAINER_NAME` will allow you to watch the quarantine tool's
progress while consuming your events stream.


Optionally, you can add `-v PATH_TO/target-events:/conf/target-events`,
replacing `PATH_TO` with the path to the directory enclosing your customized
`target-events` file.

## Using the tool (run natively)
* Requirements: Python 2.7.10+
* Clone the repo: `git clone https://github.com/cloudpassage/quarantine`
* Enter the repo and install dependencies:
`cd quarantine && pip install -r requirements.txt`
* Set these environment variables:


| Variable            | Purpose                                              |
|---------------------|------------------------------------------------------|
| HALO_API_KEY        | Halo API key ID (administrative privileges required) |
| HALO_API_SECRET_KEY | Halo API key secret                                  |
| HALO_QUARANTINE_GRP | Halo quarantine group name                           |
| MATCH_FILE          | Path to file containing events to match (see "How it works", above)  |


* Optionally, define these as well:

| Variable            | Purpose                                   |
|---------------------|-------------------------------------------|
| HALO_EVENTS_START   | ISO8601 timestamp for starting event      |

* Run the tool: `python ./app/runner.py`



<!---
#CPTAGS:community-supported automation
#TBICON:images/python_icon.png
-->
