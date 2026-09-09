Python 2D Physics Sandbox
A 2D physics simulator built with Python, Pygame, and Pymunk. This sandbox lets you spawn various dynamic objects—including fully jointed ragdolls—into an environment with ramps and walls, and manipulate the gravity in real-time.

Features
Dynamic Spawning: Click anywhere to drop bouncy balls, rigid squares, or articulated ragdolls.

Articulated Ragdolls: Uses Pymunk PivotJoints and ShapeFilters to create complex, connected bodies that tumble realistically without colliding with themselves.

Real-time Gravity Control: Shift gravity to any direction or turn it off completely (Zero-G) on the fly.

Friction & Elasticity: Objects roll, bounce, and grip surfaces accurately based on physics properties.

Smart Sleep/Wake System: Bodies automatically "wake up" when gravity shifts so they don't get stuck sleeping on surfaces.

Installation
Clone the repository:

Bash
git clone https://github.com/Ronak-uh/Physics-simulator-python.git
cd physics-sandbox
Install dependencies:
Make sure you have Python 3 installed, then run:

Bash
pip install pygame pymunk
Run the simulator:

Bash
python main.py
(Note: On macOS/Linux, you might need to use python3 and pip3)

Controls
Key	Action
Left Click	Spawn the currently selected object at the mouse cursor
1	Select Ball mode
2	Select Square mode
3	Select Ragdoll mode
C	Clear all spawned objects from the screen
Up Arrow	Reverse gravity (fall to the ceiling)
Down Arrow	Normal gravity (fall to the floor)
Left / Right	Sideways gravity (fall to the walls)
Z	Zero-Gravity (objects float and bounce with momentum)
Dependencies
pygame - Handles window creation, rendering (drawing lines, circles, polygons), and event loops.

pymunk - The physics engine doing the heavy lifting (mass, momentum, collisions, joints).

Future Implementations (To-Do)
Mouse-grabbing/throwing objects via temporary pivot joints.

Self-driving vehicles using pymunk.SimpleMotor.

Bouncy trampolines using pymunk.DampedSpring.

License
MIT - Free to use, modify, and distribute.