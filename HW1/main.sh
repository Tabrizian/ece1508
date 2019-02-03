sudo ovs-ofctl del-flows s1
sudo ovs-ofctl del-flows s2
sudo ovs-ofctl del-flows s3
sudo ovs-ofctl del-flows s4
sudo ovs-ofctl add-flow s2 idle_timeout=0,in_port=4,dl_type=0x0800,nw_dst=10.0.0.3,actions=output:3
sudo ovs-ofctl add-flow s2 idle_timeout=0,in_port=4,dl_type=0x0800,nw_dst=10.0.0.1,actions=output:1
sudo ovs-ofctl add-flow s2 idle_timeout=0,in_port=1,dl_type=0x0800,nw_dst=10.0.0.9,actions=output:4
sudo ovs-ofctl add-flow s2 idle_timeout=0,in_port=3,dl_type=0x0800,nw_dst=10.0.0.7,actions=output:4

sudo ovs-ofctl add-flow s4 idle_timeout=0,in_port=4,dl_type=0x0800,nw_src=10.0.0.3,nw_dst=10.0.0.7,actions=output:1
sudo ovs-ofctl add-flow s4 idle_timeout=0,in_port=4,dl_type=0x0800,nw_src=10.0.0.1,nw_dst=10.0.0.9,actions=output:3
sudo ovs-ofctl add-flow s4 idle_timeout=0,in_port=1,actions=output:4
sudo ovs-ofctl add-flow s4 idle_timeout=0,in_port=3,actions=output:4

sudo ovs-ofctl add-flow s1 idle_timeout=0,in_port=1,actions=output:3
sudo ovs-ofctl add-flow s1 idle_timeout=0,in_port=3,actions=output:1





