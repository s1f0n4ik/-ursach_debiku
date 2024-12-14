import numpy as np
import matplotlib.pyplot as plt

# Constants: consider adding circadian factors, stress impact multipliers, etc.
energy_consumption_rate = 0.1
lactate_accumulation_rate = 0.05
recovery_rate_day = 0.03
recovery_rate_night = 0.05  # More recovery during night
cognitive_fatigue_rate = 0.02
mental_activity_rate_base = 0.1
physical_activity_rate_base = 0.2

# Initial conditions
initial_energy = 1.0
initial_lactate = 0.0
initial_cognitive_fatigue = 0.0

time_end = 120
time_step = 1

# Time vector
time = np.arange(0, time_end, time_step)

# Initialize variables
energy = np.zeros_like(time, dtype=float)
lactate = np.zeros_like(time, dtype=float)
cognitive_fatigue = np.zeros_like(time, dtype=float)
total_fatigue = np.zeros_like(time, dtype=float)
recovery = np.zeros_like(time, dtype=float)
physical_activity = np.zeros_like(time, dtype=float)
mental_activity = np.zeros_like(time, dtype=float)

# Initial values
energy[0] = initial_energy
lactate[0] = initial_lactate
cognitive_fatigue[0] = initial_cognitive_fatigue


def update_activity(activity_base, energy_level):
    """Adjust activity based on available energy."""
    return activity_base * (0.5 if energy_level < 0.3 else 1.0)


def calculate_recovery_rate(t):
    """Determine recovery rate based on time of day."""
    return recovery_rate_night if (t % 24) >= 18 or (t % 24) < 6 else recovery_rate_day


def simulate_lactate(current_lactate, physical_activity_rate):
    """Simulate lactate buildup and recovery."""
    lactate_increase = lactate_accumulation_rate * physical_activity_rate
    lactate_recovery = recovery_rate_day * np.sqrt(current_lactate)
    return max(0, current_lactate + lactate_increase - lactate_recovery)


def simulate_cognitive_fatigue(current_cognitive_fatigue, mental_activity_rate):
    """Simulate cognitive fatigue and recovery."""
    fatigue_increase = cognitive_fatigue_rate * mental_activity_rate * (1 + np.log1p(current_cognitive_fatigue))
    cognitive_recovery = recovery_rate_day * np.sqrt(current_cognitive_fatigue)
    return max(0, current_cognitive_fatigue + fatigue_increase - cognitive_recovery)


# Simulation loop
for t in range(1, len(time)):
    physical_activity[t] = update_activity(physical_activity_rate_base, energy[t - 1])
    mental_activity[t] = update_activity(mental_activity_rate_base, energy[t - 1])

    current_recovery_rate = calculate_recovery_rate(t)
    energy[t] = max(0, energy[t - 1] - energy_consumption_rate * physical_activity[t] + current_recovery_rate)

    lactate[t] = simulate_lactate(lactate[t - 1], physical_activity[t])
    cognitive_fatigue[t] = simulate_cognitive_fatigue(cognitive_fatigue[t - 1], mental_activity[t])

    total_fatigue[t] = lactate[t] + cognitive_fatigue[t]

    if t % 20 == 0:  # Recovery session
        recovery[t] = current_recovery_rate
        energy[t] = min(1.0, energy[t] + recovery[t])

# Plotting results
fig, axs = plt.subplots(3, 3, figsize=(15, 12))

# Energy plot
axs[0, 0].plot(time, energy, label='Энергия', color='b')
axs[0, 0].set_title('Уровень энергии')
axs[0, 0].set_xlabel('Время (мин)')
axs[0, 0].set_ylabel('Энергия')
axs[0, 0].grid(True)
axs[0, 0].legend()

# Lactate plot
axs[0, 1].plot(time, lactate, label='Лактат', color='r')
axs[0, 1].set_title('Уровень лактата')
axs[0, 1].set_ylabel('Лактат')
axs[0, 1].set_xlabel('Время (мин)')
axs[0, 1].grid(True)
axs[0, 1].legend()

# Cognitive fatigue plot
axs[0, 2].plot(time, cognitive_fatigue, label='Когнитивная усталость', color='g')
axs[0, 2].set_title('Когнитивная усталость')
axs[0, 2].set_ylabel('Усталость')
axs[0, 2].set_xlabel('Время (мин)')
axs[0, 2].grid(True)
axs[0, 2].legend()

# Total fatigue plot
axs[1, 0].plot(time, total_fatigue, label='Общая усталость', color='m')
axs[1, 0].set_title('Общая усталость')
axs[1, 0].set_ylabel('Усталость')
axs[1, 0].set_xlabel('Время (мин)')
axs[1, 0].grid(True)
axs[1, 0].legend()

# Recovery plot
axs[1, 1].plot(time, recovery, label='Восстановление', color='c')
axs[1, 1].set_title('Уровень восстановления')
axs[1, 1].set_ylabel('Восстановление')
axs[1, 1].set_xlabel('Время (мин)')
axs[1, 1].grid(True)
axs[1, 1].legend()

# Physical activity plot
axs[1, 2].plot(time, physical_activity, label='Физическая активность', color='orange')
axs[1, 2].set_title('Физическая активность')
axs[1, 2].set_ylabel('Активность')
axs[1, 2].set_xlabel('Время (мин)')
axs[1, 2].grid(True)
axs[1, 2].legend()

# Mental activity plot
axs[2, 0].plot(time, mental_activity, label='Умственная активность', color='purple')
axs[2, 0].set_title('Умственная активность')
axs[2, 0].set_ylabel('Активность')
axs[2, 0].set_xlabel('Время (мин)')
axs[2, 0].grid(True)
axs[2, 0].legend()

# Fatigue vs Energy plot
axs[2, 1].plot(energy, total_fatigue, label='Утомление vs Энергия', color='brown')
axs[2, 1].set_title('Утомление vs Энергия')
axs[2, 1].set_ylabel('Утомление')
axs[2, 1].set_xlabel('Энергия')
axs[2, 1].grid(True)
axs[2, 1].legend()

# Empty plot for alignment
axs[2, 2].axis('off')

plt.tight_layout()
plt.show()