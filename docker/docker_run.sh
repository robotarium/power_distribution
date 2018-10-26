docker run -d --restart=always \
	   --net=host \
	   --device /dev/gpiomem \
	   robotarium:power_distribution
