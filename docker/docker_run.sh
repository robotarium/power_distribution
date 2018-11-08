docker run -d --restart=always \
	   --name power_distribution \
	   --net host \
	   --device /dev/gpiomem \
	   robotarium/power_distribution
