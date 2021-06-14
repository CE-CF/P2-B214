Drones:
    If no controller connected: Move the Drone with the arrow keys and move the second drone with ikjl
    If a controller is connected: Move one drone with wasd, one drone with left analog stick, and one with the controller d-pad arrows.
    If Tello mode on: Use the communication_tests to send commands to the drones.
Camera:
    No controller: Move the Camera with WSAD
    Controller: Move the Camera with the right analog stick

Exit with escape or the X on the top right

How to send commands:
  The commands are of format IP Address: Command
  Example: 0.0.0.0: takeoff

Start Menu:
    Drones' Speed: Linear speed of the drones in pixels per second
    Drone's Rotation: Rotational speed of the drones in degree per second
    No. of Drones: The number of drones in Tello mode. Up to 10
    Resolution: Resolution of the simulation window
    Frames Per Second: The max FPS cap of the simulation
    Tello Mode: Spawns Tello drones that take UDP commands instead of user input drones
    GPS Mode: Works with Tello Mode. Adds the position of the drones to their Tello state
    Full Screen: Starts the simulation in full screen
    Draw Drone's Path: Draws the path that the different drones take when moving. (Very resource heavy)
