# PCIMR_Tutorial_02

Run the task with the following command: </br>
`roslaunch rto_velocity velocity.launch`</br> 


Functioning of velocity_node:  
- Subscribers to /scan and /cmd_vel  
- Publisher to /pioneer/cmd_vel  

Functioning of `scan_callback`:  
Partitioning of the scan-range into 5 smaller ranges (left, diagonal-left, foward, diagonal-right, right).  
Speed reduces, if either range_forward, or range_diagonal_left/right have distances smaller than 3 (àttention_distance). Then, the minimum of the input speed or the allowed speed is taken. The robot comes to stop at a distance of 0.33 (stop_distance) to an object. However, the robot can always go backwards. 

Trying on the Robotino: </br>
xx



