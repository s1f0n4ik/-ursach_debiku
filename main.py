import numpy as np
import matplotlib.pyplot as plt


class Activity:
    def __init__(self, base_rate):
        self.base_rate = base_rate

    def update_activity(self, energy_level):
        return self.base_rate * (0.5 if energy_level < 0.3 else 1.0)


class PhysicalActivity(Activity):
    def __init__(self):
        super().__init__(0.2)


class MentalActivity(Activity):
    def __init__(self):
        super().__init__(0.1)


class Person:
    def __init__(self):
        self.energy = 1.0
        self.lactate = 0.0
        self.cognitive_fatigue = 0.0

    def update_energy(self, physical_activity, recovery_rate):
        energy_consumption_rate = 0.1
        self.energy = max(0, self.energy - energy_consumption_rate * physical_activity + recovery_rate)
        return self.energy

    def update_lactate(self, physical_activity, dt):
        lactate_accumulation_rate = 0.05
        lactate_recovery_rate = 0.03
        lactate_increase = lactate_accumulation_rate * physical_activity * dt
        lactate_recovery = lactate_recovery_rate * np.sqrt(self.lactate) * dt
        self.lactate = max(0, self.lactate + lactate_increase - lactate_recovery)
        return self.lactate

    def update_cognitive_fatigue(self, mental_activity, dt):
        cognitive_fatigue_rate = 0.02
        fatigue_increase = cognitive_fatigue_rate * mental_activity * (1 + np.log1p(self.cognitive_fatigue)) * dt
        cognitive_recovery = 0.03 * np.sqrt(self.cognitive_fatigue) * dt
        self.cognitive_fatigue = max(0, self.cognitive_fatigue + fatigue_increase - cognitive_recovery)
        return self.cognitive_fatigue


class Simulation:
    def __init__(self, time_end=120, dt=0.1):
        self.time_end = time_end
        self.dt = dt
        self.time = np.arange(0, self.time_end, self.dt)
        self.person = Person()
        self.physical_activity = PhysicalActivity()
        self.mental_activity = MentalActivity()

        # Initialize arrays to store simulation data
        self.energy = np.zeros_like(self.time, dtype=float)
        self.lactate = np.zeros_like(self.time, dtype=float)
        self.cognitive_fatigue = np.zeros_like(self.time, dtype=float)
        self.total_fatigue = np.zeros_like(self.time, dtype=float)
        self.recovery = np.zeros_like(self.time, dtype=float)
        self.physical_activity_levels = np.zeros_like(self.time, dtype=float)
        self.mental_activity_levels = np.zeros_like(self.time, dtype=float)

    @staticmethod
    def calculate_recovery_rate(t):
        recovery_rate_day = 0.03
        recovery_rate_night = 0.05
        # Check if t is an array or a single value
        if isinstance(t, np.ndarray):
            # Create a boolean array for nighttime and day time
            is_night = ((t % 24) >= 18) | ((t % 24) < 6)
            return np.where(is_night, recovery_rate_night, recovery_rate_day)
        else:
            # Single value handling
            return recovery_rate_night if (t % 24) >= 18 or (t % 24) < 6 else recovery_rate_day

    def run(self):
        self.energy[0] = self.person.energy
        self.lactate[0] = self.person.lactate
        self.cognitive_fatigue[0] = self.person.cognitive_fatigue

        for i, t in enumerate(self.time[1:], start=1):
            self.physical_activity_levels[i] = self.physical_activity.update_activity(self.energy[i - 1])
            self.mental_activity_levels[i] = self.mental_activity.update_activity(self.energy[i - 1])

            current_recovery_rate = self.calculate_recovery_rate(t)
            self.energy[i] = self.person.update_energy(self.physical_activity_levels[i], current_recovery_rate * self.dt)
            self.lactate[i] = self.person.update_lactate(self.physical_activity_levels[i], self.dt)
            self.cognitive_fatigue[i] = self.person.update_cognitive_fatigue(self.mental_activity_levels[i], self.dt)
            self.total_fatigue[i] = self.lactate[i] + self.cognitive_fatigue[i]

        self.recovery = np.where((self.time % 20) == 0, self.calculate_recovery_rate(self.time) * self.dt, 0)
        self.energy += self.recovery

    def plot_results(self):
        fig, axs = plt.subplots(3, 3, figsize=(15, 12))

        # Energy plot
        axs[0, 0].plot(self.time, self.energy, label='Energy', color='b')
        axs[0, 0].set_title('Energy Level')
        axs[0, 0].set_xlabel('Time (minutes)')
        axs[0, 0].set_ylabel('Energy')
        axs[0, 0].grid(True)
        axs[0, 0].legend()

        # Lactate plot
        axs[0, 1].plot(self.time, self.lactate, label='Lactate', color='r')
        axs[0, 1].set_title('Lactate Level')
        axs[0, 1].set_ylabel('Lactate')
        axs[0, 1].set_xlabel('Time (minutes)')
        axs[0, 1].grid(True)
        axs[0, 1].legend()

        # Cognitive fatigue plot
        axs[0, 2].plot(self.time, self.cognitive_fatigue, label='Cognitive Fatigue', color='g')
        axs[0, 2].set_title('Cognitive Fatigue')
        axs[0, 2].set_ylabel('Fatigue')
        axs[0, 2].set_xlabel('Time (minutes)')
        axs[0, 2].grid(True)
        axs[0, 2].legend()

        # Total fatigue plot
        axs[1, 0].plot(self.time, self.total_fatigue, label='Total Fatigue', color='m')
        axs[1, 0].set_title('Total Fatigue')
        axs[1, 0].set_ylabel('Fatigue')
        axs[1, 0].set_xlabel('Time (minutes)')
        axs[1, 0].grid(True)
        axs[1, 0].legend()

        # Recovery plot
        axs[1, 1].plot(self.time, self.recovery, label='Recovery', color='c')
        axs[1, 1].set_title('Recovery Level')
        axs[1, 1].set_ylabel('Recovery')
        axs[1, 1].set_xlabel('Time (minutes)')
        axs[1, 1].grid(True)
        axs[1, 1].legend()

        # Physical activity plot
        axs[1, 2].plot(self.time, self.physical_activity_levels, label='Physical Activity', color='orange')
        axs[1, 2].set_title('Physical Activity')
        axs[1, 2].set_ylabel('Activity')
        axs[1, 2].set_xlabel('Time (minutes)')
        axs[1, 2].grid(True)
        axs[1, 2].legend()

        # Mental activity plot
        axs[2, 0].plot(self.time, self.mental_activity_levels, label='Mental Activity', color='purple')
        axs[2, 0].set_title('Mental Activity')
        axs[2, 0].set_ylabel('Activity')
        axs[2, 0].set_xlabel('Time (minutes)')
        axs[2, 0].grid(True)
        axs[2, 0].legend()

        # Fatigue vs Energy plot
        axs[2, 1].plot(self.energy, self.total_fatigue, label='Fatigue vs Energy', color='brown')
        axs[2, 1].set_title('Fatigue vs Energy')
        axs[2, 1].set_ylabel('Fatigue')
        axs[2, 1].set_xlabel('Energy')
        axs[2, 1].grid(True)
        axs[2, 1].legend()

        # Empty plot for alignment
        axs[2, 2].axis('off')

        plt.tight_layout()
        plt.show()


# Example of running simulation
if __name__ == "__main__":
    simulation = Simulation()
    simulation.run()
    simulation.plot_results()
