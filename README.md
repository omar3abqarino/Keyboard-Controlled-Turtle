# Keyboard-Controlled-Turtle
Use Your Keyboard To Drive The Turtle Anywhere You Want.
You can control it Using (A, W, S, D).

## External Dependencies:
- `sshkeyboard` used for key capture.
- `twist_stamper` used for the bonus task.
- `xterm` used for the external window to input from launch file.

### Minimum Python Version To Use is Python3.6  

### You copy these lines of code to clone the repository  
<code> cd ~/ros2_ws/src </code>  
<code> git clone https://github.com/omar3abqarino/Keyboard-Controlled-Turtle.git </code>  
<code> cd ~/ros2_ws </code>

> [!CAUTION]
> You Have To Paste These lines for the code to run smoothly.  
> <code> rosdep update </code>  
> <code> rosdep install --from-paths src -y --ignore-src </code>  
> <code> pip install --user sshkeyboard --break-system-packages </code>

## To Build The App
<code> colcon build </code>  
<code> source install/setup.bash </code>

## Usage
<code> ros2 launch my_pkg robot_launch.launch.py </code>  

### Additional Parameters
- You Can Change The Data Type Between `Twist` & `TwistStamped` by adding this parameter to the launch line code `use_stamped:=true` or `use_stamped:=false`.  
- You Can Change The Dominant Color Topic Name from the XTerm window that pops off at launch.
