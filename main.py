import simpy
import random
import matplotlib.pyplot as plt
import pandas as pd

# Constants
RANDOM_SEED = 42
SIM_TIME = 10000  # Simulation time in minutes

# Machine and operation details with descriptive names
MACHINE_DETAILS = {
    'steel_cutting': {'count': 10, 'operation_time': 10, 'breakdown_prob': 0.05, 'repair_time': 30},
    'metal_pressing': {'count': 20, 'operation_time': 20, 'breakdown_prob': 0.1, 'repair_time': 45},
    'welding': {'count': 15, 'operation_time': 15, 'breakdown_prob': 0.07, 'repair_time': 40},
    'quality_inspection': {'count': 10, 'operation_time': 5, 'breakdown_prob': 0.03, 'repair_time': 20},
    'painting': {'count': 8, 'operation_time': 10, 'breakdown_prob': 0.04, 'repair_time': 25},
    'assembly_line': {'count': 12, 'operation_time': 18, 'breakdown_prob': 0.06, 'repair_time': 35},
    'packaging': {'count': 8, 'operation_time': 12, 'breakdown_prob': 0.05, 'repair_time': 30}
}

# Extended operation times for multiple product types with descriptive names
PRODUCT_OPERATION_TIMES = {
    'engine_parts': {
        'steel_cutting': 10,
        'metal_pressing': 20,
        'welding': 15,
        'quality_inspection': 5,
        'painting': 10,
        'assembly_line': 18,
        'packaging': 12
    },
    'chassis_components': {
        'steel_cutting': 12,
        'metal_pressing': 22,
        'welding': 17,
        'quality_inspection': 6,
        'painting': 11,
        'assembly_line': 20,
        'packaging': 14
    },
    'electrical_systems': {
        'steel_cutting': 8,
        'metal_pressing': 18,
        'welding': 13,
        'quality_inspection': 4,
        'painting': 9,
        'assembly_line': 16,
        'packaging': 10
    },
    'interior_fittings': {
        'steel_cutting': 9,
        'metal_pressing': 19,
        'welding': 14,
        'quality_inspection': 5,
        'painting': 10,
        'assembly_line': 17,
        'packaging': 11
    },
    'brake_systems': {
        'steel_cutting': 11,
        'metal_pressing': 21,
        'welding': 16,
        'quality_inspection': 6,
        'painting': 11,
        'assembly_line': 19,
        'packaging': 13
    },
    'suspension_units': {
        'steel_cutting': 10,
        'metal_pressing': 20,
        'welding': 15,
        'quality_inspection': 5,
        'painting': 10,
        'assembly_line': 18,
        'packaging': 12
    },
    'fuel_systems': {
        'steel_cutting': 8,
        'metal_pressing': 18,
        'welding': 13,
        'quality_inspection': 4,
        'painting': 9,
        'assembly_line': 16,
        'packaging': 10
    },
    'cooling_systems': {
        'steel_cutting': 12,
        'metal_pressing': 22,
        'welding': 17,
        'quality_inspection': 6,
        'painting': 11,
        'assembly_line': 20,
        'packaging': 14
    },
    'transmissions': {
        'steel_cutting': 9,
        'metal_pressing': 19,
        'welding': 14,
        'quality_inspection': 5,
        'painting': 10,
        'assembly_line': 17,
        'packaging': 11
    },
    'exhaust_systems': {
        'steel_cutting': 10,
        'metal_pressing': 20,
        'welding': 15,
        'quality_inspection': 5,
        'painting': 10,
        'assembly_line': 18,
        'packaging': 12
    },
    'lighting_components': {
        'steel_cutting': 11,
        'metal_pressing': 21,
        'welding': 16,
        'quality_inspection': 6,
        'painting': 11,
        'assembly_line': 19,
        'packaging': 13
    },
    'windshield_systems': {
        'steel_cutting': 12,
        'metal_pressing': 22,
        'welding': 17,
        'quality_inspection': 6,
        'painting': 11,
        'assembly_line': 20,
        'packaging': 14
    },
    'seat_frames': {
        'steel_cutting': 8,
        'metal_pressing': 18,
        'welding': 13,
        'quality_inspection': 4,
        'painting': 9,
        'assembly_line': 16,
        'packaging': 10
    },
    'door_handles': {
        'steel_cutting': 9,
        'metal_pressing': 19,
        'welding': 14,
        'quality_inspection': 5,
        'painting': 10,
        'assembly_line': 17,
        'packaging': 11
    },
    'mirror_units': {
        'steel_cutting': 10,
        'metal_pressing': 20,
        'welding': 15,
        'quality_inspection': 5,
        'painting': 10,
        'assembly_line': 18,
        'packaging': 12
    }
}

# Function to model machine operation
def machine_operation(env, name, operation_time, breakdown_prob, repair_time, log, delays):
    while True:
        start_time = env.now
        yield env.timeout(operation_time)
        log.append((env.now, f'{name} finished an operation'))

        # Check for breakdown
        if random.random() < breakdown_prob:
            breakdown_time = env.now
            log.append((breakdown_time, f'{name} broke down'))
            yield env.timeout(repair_time)
            repair_time_end = env.now
            log.append((repair_time_end, f'{name} repaired'))
            delays.append((name, breakdown_time - start_time, repair_time_end - breakdown_time))

# Function to model the production line
def production_line(env, machine_details, log, delays):
    machines = {key: [simpy.Resource(env) for _ in range(value['count'])] for key, value in machine_details.items()}
    
    while True:
        for operation, details in machine_details.items():
            machine = random.choice(machines[operation])
            with machine.request() as request:
                yield request
                yield env.process(machine_operation(env, operation, details['operation_time'], details['breakdown_prob'], details['repair_time'], log, delays))

# Extended production line function for multiple product types
def multi_product_production_line(env, machine_details, product_operation_times, log, delays):
    machines = {key: [simpy.Resource(env) for _ in range(value['count'])] for key, value in machine_details.items()}
    
    while True:
        for product, operation_times in product_operation_times.items():
            for operation, time in operation_times.items():
                machine = random.choice(machines[operation])
                details = machine_details[operation]
                with machine.request() as request:
                    yield request
                    yield env.process(machine_operation(env, f'{product} - {operation}', time, details['breakdown_prob'], details['repair_time'], log, delays))

# Function to collect data for analysis
def data_collector(env, data):
    while True:
        data.append((env.now, len(data)))
        yield env.timeout(60)  # Collect data every hour

# Main simulation function for single product
def run_simulation():
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    data = []
    log = []
    delays = []

    # Start production line and data collector
    env.process(production_line(env, MACHINE_DETAILS, log, delays))
    env.process(data_collector(env, data))

    # Run simulation
    env.run(until=SIM_TIME)

    # Return data and log for further analysis
    return data, log, delays

# Main simulation function for multiple products
def run_extended_simulation():
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    data = []
    log = []
    delays = []

    # Start multi-product production line and data collector
    env.process(multi_product_production_line(env, MACHINE_DETAILS, PRODUCT_OPERATION_TIMES, log, delays))
    env.process(data_collector(env, data))

    # Run simulation
    env.run(until=SIM_TIME)

    # Return data and log for further analysis
    return data, log, delays

# Run the single product simulation
data, log, delays = run_simulation()

# Analyze the collected data for single product
df = pd.DataFrame(data, columns=['Time', 'Operations Completed'])
log_df = pd.DataFrame(log, columns=['Time', 'Event'])
delays_df = pd.DataFrame(delays, columns=['Machine', 'Operation Time', 'Repair Time'])
print("Single Product Line Simulation Data Summary:")
print(df.describe())

# Run the extended simulation for multiple products
extended_data, extended_log, extended_delays = run_extended_simulation()

# Analyze the collected data for multiple products
extended_df = pd.DataFrame(extended_data, columns=['Time', 'Operations Completed'])
extended_log_df = pd.DataFrame(extended_log, columns=['Time', 'Event'])
extended_delays_df = pd.DataFrame(extended_delays, columns=['Machine', 'Operation Time', 'Repair Time'])
print("\nMulti-product Line Simulation Data Summary:")
print(extended_df.describe())

# Detailed Report
def generate_report(log_df, delays_df, title):
    report = f"### {title} ###\n\n"
    report += "Event Counts:\n"
    report += log_df.groupby('Event').size().to_string() + '\n\n'
    report += "Delay Statistics:\n"
    report += delays_df.describe().to_string() + '\n\n'
    return report

# Generate and print detailed reports
single_product_report = generate_report(log_df, delays_df, "Single Product Line Simulation Report")
multi_product_report = generate_report(extended_log_df, extended_delays_df, "Multi-product Line Simulation Report")

print(single_product_report)
print(multi_product_report)

# Plot all graphs on a single screen
fig, axs = plt.subplots(3, 3, figsize=(18, 20))

# Plot 1: Single product operations over time
axs[0, 0].plot(df['Time'], df['Operations Completed'], label='Operations completed over time')
axs[0, 0].set_title('Single Product Line Operations Over Time')
axs[0, 0].set_xlabel('Simulation Time (minutes)')
axs[0, 0].set_ylabel('Operations Completed')
axs[0, 0].legend()

# Plot 2: Single product event count
axs[0, 1].plot(log_df['Time'], log_df.index, drawstyle='steps-post', label='Operations and Events')
axs[0, 1].set_title('Single Product Line Events')
axs[0, 1].set_xlabel('Simulation Time (minutes)')
axs[0, 1].set_ylabel('Event Count')
axs[0, 1].legend()

# Plot 3: Multi-product operations over time
axs[0, 2].plot(extended_df['Time'], extended_df['Operations Completed'], label='Operations completed over time')
axs[0, 2].set_title('Multi-product Line Operations Over Time')
axs[0, 2].set_xlabel('Simulation Time (minutes)')
axs[0, 2].set_ylabel('Operations Completed')
axs[0, 2].legend()

# Plot 4: Multi-product event count
axs[1, 0].plot(extended_log_df['Time'], extended_log_df.index, drawstyle='steps-post', label='Operations and Events')
axs[1, 0].set_title('Multi-product Line Events')
axs[1, 0].set_xlabel('Simulation Time (minutes)')
axs[1, 0].set_ylabel('Event Count')
axs[1, 0].legend()

# Plot 5: Single product delay statistics
delays_df.boxplot(column=['Operation Time', 'Repair Time'], ax=axs[1, 1])
axs[1, 1].set_title('Single Product Line Delay Statistics')
axs[1, 1].set_ylabel('Time (minutes)')

# Plot 6: Multi-product delay statistics
extended_delays_df.boxplot(column=['Operation Time', 'Repair Time'], ax=axs[1, 2])
axs[1, 2].set_title('Multi-product Line Delay Statistics')
axs[1, 2].set_ylabel('Time (minutes)')

# Plot 7: Single product delay distribution
delays_df.hist(column='Operation Time', bins=20, ax=axs[2, 0])
axs[2, 0].set_title('Single Product Line Operation Time Distribution')
axs[2, 0].set_xlabel('Operation Time (minutes)')
axs[2, 0].set_ylabel('Frequency')

# Plot 8: Single product repair time distribution
delays_df.hist(column='Repair Time', bins=20, ax=axs[2, 1])
axs[2, 1].set_title('Single Product Line Repair Time Distribution')
axs[2, 1].set_xlabel('Repair Time (minutes)')
axs[2, 1].set_ylabel('Frequency')

# Plot 9: Multi-product delay distribution
extended_delays_df.hist(column='Operation Time', bins=20, ax=axs[2, 2])
axs[2, 2].set_title('Multi-product Line Operation Time Distribution')
axs[2, 2].set_xlabel('Operation Time (minutes)')
axs[2, 2].set_ylabel('Frequency')

plt.tight_layout()
plt.show()
