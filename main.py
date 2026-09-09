import pygame
import pymunk
import math

# --- 1. Pygame Setup ---
pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

# --- 2. Pymunk Physics Space Setup ---
space = pymunk.Space()
space.gravity = (0, 900)

# --- 3. Create Static Environment ---
static_lines = [
    pymunk.Segment(space.static_body, (0, 750), (800, 750), 10),
    pymunk.Segment(space.static_body, (0, 0), (0, 800), 10),
    pymunk.Segment(space.static_body, (800, 0), (800, 800), 10),
    pymunk.Segment(space.static_body, (0, 200), (500, 400), 10),
    pymunk.Segment(space.static_body, (800, 450), (200, 650), 10)
]

for line in static_lines:
    line.elasticity = 0.4
    line.friction = 0.7
    space.add(line)

# --- 4. Entity Spawning Functions & Classes ---
def spawn_ball(space, position):
    mass = 1
    radius = 15
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.8
    shape.friction = 0.5 
    space.add(body, shape)
    return shape

def spawn_square(space, position):
    mass = 1
    size = (30, 30)
    moment = pymunk.moment_for_box(mass, size)
    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Poly.create_box(body, size)
    shape.elasticity = 0.5
    shape.friction = 0.6
    space.add(body, shape)
    return shape

class Ragdoll:
    def __init__(self, space, pos, group_id):
        self.space = space
        self.parts = []   
        self.joints = []  
        self.filter = pymunk.ShapeFilter(group=group_id)
        x, y = pos

        head_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 12))
        head_body.position = (x, y)
        head_shape = pymunk.Circle(head_body, 12)
        self._add_part(head_body, head_shape)

        torso_body = pymunk.Body(2, pymunk.moment_for_box(2, (16, 40)))
        torso_body.position = (x, y + 25)
        torso_shape = pymunk.Poly.create_box(torso_body, (16, 40))
        self._add_part(torso_body, torso_shape)

        l_arm_body = pymunk.Body(0.5, pymunk.moment_for_box(0.5, (8, 30)))
        l_arm_body.position = (x - 15, y + 25)
        l_arm_shape = pymunk.Poly.create_box(l_arm_body, (8, 30))
        self._add_part(l_arm_body, l_arm_shape)

        r_arm_body = pymunk.Body(0.5, pymunk.moment_for_box(0.5, (8, 30)))
        r_arm_body.position = (x + 15, y + 25)
        r_arm_shape = pymunk.Poly.create_box(r_arm_body, (8, 30))
        self._add_part(r_arm_body, r_arm_shape)

        l_leg_body = pymunk.Body(1, pymunk.moment_for_box(1, (10, 35)))
        l_leg_body.position = (x - 8, y + 60)
        l_leg_shape = pymunk.Poly.create_box(l_leg_body, (10, 35))
        self._add_part(l_leg_body, l_leg_shape)

        r_leg_body = pymunk.Body(1, pymunk.moment_for_box(1, (10, 35)))
        r_leg_body.position = (x + 8, y + 60)
        r_leg_shape = pymunk.Poly.create_box(r_leg_body, (10, 35))
        self._add_part(r_leg_body, r_leg_shape)

        self._add_joint(pymunk.PivotJoint(head_body, torso_body, (x, y + 10)))
        self._add_joint(pymunk.PivotJoint(torso_body, l_arm_body, (x - 8, y + 15)))
        self._add_joint(pymunk.PivotJoint(torso_body, r_arm_body, (x + 8, y + 15)))
        self._add_joint(pymunk.PivotJoint(torso_body, l_leg_body, (x - 6, y + 45)))
        self._add_joint(pymunk.PivotJoint(torso_body, r_leg_body, (x + 6, y + 45)))

    def _add_part(self, body, shape):
        shape.friction = 0.6
        shape.elasticity = 0.2
        shape.filter = self.filter
        self.space.add(body, shape)
        self.parts.append((body, shape))

    def _add_joint(self, joint):
        self.space.add(joint)
        self.joints.append(joint)

    def draw(self, screen):
        for body, shape in self.parts:
            if isinstance(shape, pymunk.Circle):
                px, py = int(body.position.x), int(body.position.y)
                pygame.draw.circle(screen, (255, 200, 150), (px, py), int(shape.radius))
            elif isinstance(shape, pymunk.Poly):
                vertices = [(v.rotated(body.angle).x + body.position.x, v.rotated(body.angle).y + body.position.y) for v in shape.get_vertices()]
                pygame.draw.polygon(screen, (100, 150, 200), vertices)

    def destroy(self):
        for joint in self.joints:
            self.space.remove(joint)
        for body, shape in self.parts:
            self.space.remove(body, shape)

# --- Helper: Wake Up Sleeping Bodies ---
def wake_all_bodies(space):
    for body in space.bodies:
        if body.body_type == pymunk.Body.DYNAMIC:
            body.activate()

# --- 5. Main Game Loop Variables ---
balls = []
squares = []
ragdolls = []
ragdoll_group = 1 
spawn_mode = "ragdoll"
gravity_mode = "Down" # Tracks current gravity state

running = True
while running:
    # Update Window Title to include Gravity state
    pygame.display.set_caption(f"Mode: {spawn_mode.upper()} | Gravity: {gravity_mode} | Arrows: Gravity, Z: Zero-G")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # --- Handle Keyboard Input ---
        elif event.type == pygame.KEYDOWN:
            # Spawning and Clearing
            if event.key == pygame.K_1:
                spawn_mode = "ball"
            elif event.key == pygame.K_2:
                spawn_mode = "square"
            elif event.key == pygame.K_3:
                spawn_mode = "ragdoll"
            elif event.key == pygame.K_c:
                for b in balls: space.remove(b, b.body)
                balls.clear()
                for s in squares: space.remove(s, s.body)
                squares.clear()
                for r in ragdolls: r.destroy()
                ragdolls.clear()
                
            # --- Gravity Controls ---
            elif event.key == pygame.K_UP:
                space.gravity = (0, -900)
                gravity_mode = "Up"
                wake_all_bodies(space)
            elif event.key == pygame.K_DOWN:
                space.gravity = (0, 900)
                gravity_mode = "Down"
                wake_all_bodies(space)
            elif event.key == pygame.K_LEFT:
                space.gravity = (-900, 0)
                gravity_mode = "Left"
                wake_all_bodies(space)
            elif event.key == pygame.K_RIGHT:
                space.gravity = (900, 0)
                gravity_mode = "Right"
                wake_all_bodies(space)
            elif event.key == pygame.K_z:
                space.gravity = (0, 0)
                gravity_mode = "Zero-G"
                wake_all_bodies(space)

        # --- Handle Mouse Clicks ---
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if spawn_mode == "ball":
                balls.append(spawn_ball(space, event.pos))
            elif spawn_mode == "square":
                squares.append(spawn_square(space, event.pos))
            elif spawn_mode == "ragdoll":
                ragdolls.append(Ragdoll(space, event.pos, ragdoll_group))
                ragdoll_group += 1 

    # --- Draw Everything ---
    screen.fill((30, 30, 30))

    for line in static_lines:
        pygame.draw.line(screen, (150, 150, 150), line.a, line.b, int(line.radius * 2))

    for ball in balls:
        px, py = int(ball.body.position.x), int(ball.body.position.y)
        pygame.draw.circle(screen, (100, 200, 255), (px, py), int(ball.radius))
        end_x = px + ball.radius * math.cos(ball.body.angle)
        end_y = py + ball.radius * math.sin(ball.body.angle)
        pygame.draw.line(screen, (50, 100, 150), (px, py), (end_x, end_y), 2)

    for square in squares:
        vertices = [(v.rotated(square.body.angle).x + square.body.position.x, v.rotated(square.body.angle).y + square.body.position.y) for v in square.get_vertices()]
        pygame.draw.polygon(screen, (150, 255, 100), vertices)

    for ragdoll in ragdolls:
        ragdoll.draw(screen)

    space.step(1 / 60.0)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()