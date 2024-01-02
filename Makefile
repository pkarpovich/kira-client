SPOT_INVENTORY := ./inventory.yml
SSH_KEY := ~/.ssh/id_diskstation_rsa

deploy_%:
	spot -t $* -v -i ${SPOT_INVENTORY} -k ${SSH_KEY}