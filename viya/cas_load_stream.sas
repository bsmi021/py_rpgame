/* This script is used to create a live stream from SAS ESP to a SAS CAS Table (global), by doing the following:
    1. Create a CAS session
    2. Load the Streaming Data Action Set, note that you may need to change the the following:
        a. dataSource.server
        b. dataSource.port
        c. name
    3. Test to ensure the connection works by grabbing the ESP project's metadata and displaying it on screen, note
        you may need to change the casLib value to match the name from 2.c
    4. Removes the existing CAS table (rpg_game_demo), this is necessary when streaming data as the table is in the
       global scope and thus cannot be appended to with a new stream.
    5. Executes the loadStreams.loadStream CAS action which will create a connection to a window in the ESP model
       and will stream data into a new global table (rpg_game_demo)
*/

/* 1. create the cas session*/
CAS esp_session host="<cas controller IP>" SESSOPTS=( caslib=casuser TIMEOUT=99999 LOCALE="en_US");

/* 2. creates the cas lib and sets the connection to ESP */
proc cas;

	/* Load the Streaming Data Action Set */
	builtins.loadactionset actionSet="loadStreams";

	/* Create a caslib, specify the esp server (note srcType must be "esp") */
	table.addCaslib
		dataSource={port=5994,server="<esp server IP>",srcType="esp"}
		name="brwsmilib";
run;

/* 3. Pull the metadata */
proc cas;
	/* Query the metadata for the ESP caslib */
	loadStreams.mMetadata casLib="brwsmilib";
run;

/* 4. Assign all libraries and remove the CAS table */
caslib _all_ assign;

proc datasets library=casuser;
	delete rpg_combat_log;
quit;

/* 5. Stream the data into a new CAS table  */
proc cas;
	loadStreams.loadStream /
		casLib="brwsmilib"
		espUri="rpggame_demo_dataflow/cq1/attack_time_variables"
		casOut= {caslib="casuser",name="rpg_combat_log", promote=true};
run;

/** Terminate the CAS session **/
/* cas esp_session terminate; */