class Spring:
    springs = []
    def __init__(self, target=0, speed=10, damping=0.5, min_value=float('-inf'), max_value=float('inf')):
        self.target = target
        self.position = target
        self.velocity = 0
        # speed represents the angular frequency (ω) in this context
        self.angular_frequency = speed
        # Convert damping ratio (ζ) to damping coefficient (c)
        self.damping = damping * 2 * (speed ** 0.5)  # 2*ζω
        self.min_value = min_value
        self.max_value = max_value
        self.springs.append(self)

    def update(self, delta_time):
        # Calculate spring force (F = -kx)
        displacement = self.target - self.position
        spring_force = displacement * (self.angular_frequency ** 2)  # k = ω²
        
        # Apply force and damping
        self.velocity += spring_force * delta_time
        self.velocity *= (1 - self.damping * delta_time)
        
        # Update position
        new_position = self.position + self.velocity * delta_time
        
        # Check bounds and bounce if necessary
        if new_position < self.min_value:
            self.position = self.min_value
            self.velocity = -self.velocity * 0.8
        elif new_position > self.max_value:
            self.position = self.max_value
            self.velocity = -self.velocity * 0.8
        else:
            self.position = new_position
            
        return self.position