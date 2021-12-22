#!/bin/bash
while true
do
  #simulate 4 200 responses

  for i in {1..5}; do
    curl --output /dev/null --show-error --fail http://localhost:8080;
  done

	#simulate 1 404
	curl --silent --output /dev/null --show-error --fail http://localhost:8080/anything

	sleep 1
done
