# MB_1R2T_LIDAR_Demo
A quick Python Demo for the MB_1R2T LIDAR Module (available from [AliExpress](https://www.aliexpress.com/item/1005002600906162.html)) to visualise the output graphically.

## Usage
1. Connect the LIDAR Module via an USB-RS232 adapter. The 5V can be sourced directly from the USB port, the motor control signal is optional and can be left unconnected.
2. Change the port name in [line 19](mb_1r2t.py#L19) to the appropriate interface.
3. Run the python script

## Example
![Example Output](/example.png)

## Acknowledgement
The package structure was taken from https://github.com/Vidicon/mb_1r2t_ros
