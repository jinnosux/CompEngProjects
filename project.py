import matplotlib.pyplot as plt
import numpy as np

def get_num_processes():
    while True:
        try:
            num_processes = int(input("Enter how many processes you would like to analyze: "))
            if num_processes > 0:
                return num_processes
            else:
                print("Number of processes must be greater than 0. Please try again.")
        except ValueError:
            print("Please enter a valid integer.")

def generate_random_data(num_processes):
    burst_durations = []
    priorities = np.random.permutation(np.arange(1, num_processes + 1)).tolist()

    for i in range(1, num_processes + 1):
        burst = np.random.choice(range(1, 51))
        priority = priorities[i-1]
        burst_durations.append(burst)
        
    return burst_durations, priorities

def generate_range_data(num_processes):
    burst_durations = []
    priorities = []
    
    burst_min = int(input("Enter the minimum burst duration: "))
    burst_max = int(input("Enter the maximum burst duration: "))
    
    available_priorities = list(range(1, num_processes + 1))
    
    for i in range(1, num_processes + 1):
        burst = np.random.choice(range(burst_min, burst_max + 1))
        priority = np.random.choice(available_priorities)
        available_priorities.remove(priority)
        
        burst_durations.append(burst)
        priorities.append(priority)

    return burst_durations, priorities

def manual_input_data(num_processes):
    burst_durations = []
    priorities = []
    for i in range(1, num_processes + 1):
        burst = int(input(f"Enter burst duration for P{i}: "))
        priority = int(input(f"Enter priority for P{i}: "))
        burst_durations.append(burst)
        priorities.append(priority)

    print(burst_durations, priorities)
    return burst_durations, priorities

def generate_table(num_processes, burst_durations, priorities):
    print("{:<10} {:<20} {:<10}".format("Process", "Burst Duration (ms)", "Priority"))
    for i in range(1, num_processes + 1):
        print("{:<10} {:<20} {:<10}".format(f"P{i}", burst_durations[i-1], priorities[i-1]))

def calculate_awt_with_priority(num_processes, burst_durations, priorities):
    sorted_processes = sorted(zip(burst_durations, priorities), key=lambda x: x[1])
    sorted_burst_durations, _ = zip(*sorted_processes)

    waiting_times = [0]
    for i in range(1, num_processes):
        waiting_time = waiting_times[i-1] + sorted_burst_durations[i-1]
        waiting_times.append(waiting_time)

    awt = np.sum(waiting_times) / num_processes
    return awt


def calculate_awt_without_priority(num_processes, burst_durations):
    waiting_times = [0] * num_processes
    for i in range(1, num_processes):
        waiting_time = waiting_times[i-1] + sum(burst_durations[:i])
        waiting_times.append(waiting_time)

    awt = sum(waiting_times) / num_processes
    return awt

def generate_awt_text(ax, awt_with_priority, awt_without_priority):
    ax.axis('off')
    ax.text(0.5, 0.5, f"AwT (no priority) = {awt_without_priority:.2f}ms\nAwT (priority) = {awt_with_priority:.2f}ms",
            va='center', ha='center', fontsize=14)
    
def generate_color_map(num_processes):
    return plt.cm.viridis(np.linspace(0, 1, num_processes))

def generate_bar_chart1(num_processes, burst_durations, priorities, ax, colors):
    for i in range(num_processes):
        ax.barh(1, burst_durations[i], color=colors[i], label=f'P{i + 1}', left=np.sum(burst_durations[:i]))

    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Process")
    ax.set_yticks([1])
    ax.set_title("Gantt Chart with Burst Durations")
    ax.legend()

    x_ticks = np.concatenate(([0], np.cumsum(burst_durations)))
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_ticks)

def generate_bar_chart2(num_processes, burst_durations, priorities, ax, colors):
    sorted_processes = sorted(zip(range(num_processes), burst_durations, priorities), key=lambda x: x[2])
    sorted_processes_indices, sorted_burst_durations, sorted_priorities = zip(*sorted_processes)

    for i in range(num_processes):
        ax.barh(1, sorted_burst_durations[i], color=colors[sorted_processes_indices[i]],
                label=f'P{sorted_processes_indices[i] + 1}', left=np.sum(sorted_burst_durations[:i]))

    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Process")
    ax.set_yticks([1])
    ax.set_title("Gantt Chart with Burst Durations (Sorted by Priority)")
    ax.legend()

    x_ticks = np.concatenate(([0], np.cumsum(sorted_burst_durations)))
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_ticks)

def main():
    num_processes = get_num_processes() 
    option = int(input("Would you like Burst Durations and Priorities to be:\n1. Randomly generated\n2. Range\n3. Manually\nEnter your choice (1/2/3): "))
    if option == 1:
        burst_durations, priorities = generate_random_data(num_processes)
    elif option == 2:
        burst_durations, priorities = generate_range_data(num_processes)
    elif option == 3:
        burst_durations, priorities = manual_input_data(num_processes)
    else:
        print("Invalid choice. Exiting.")
        return

    awt_with_priority = calculate_awt_with_priority(num_processes, burst_durations, priorities)
    awt_without_priority = calculate_awt_without_priority(num_processes, burst_durations)

    colors = generate_color_map(num_processes)

    fig = plt.figure(figsize=(20, 20))

    ax4 = fig.add_subplot(221, frame_on=False)
    ax4.xaxis.set_visible(False)
    ax4.yaxis.set_visible(False)

    table_data = [("Process", "Burst Duration (ms)", "Priority")] + \
                [(f"P{i}", burst_durations[i-1], priorities[i-1]) for i in range(1, num_processes + 1)]
    table = ax4.table(cellText=table_data, loc='center', cellLoc = 'center', rowLoc = 'center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 3.5)

    ax1 = fig.add_subplot(222)
    generate_awt_text(ax1, awt_with_priority, awt_without_priority)
    ax2 = fig.add_subplot(223)
    generate_bar_chart1(num_processes, burst_durations, priorities, ax2, colors)
    ax3 = fig.add_subplot(224)
    generate_bar_chart2(num_processes, burst_durations, priorities, ax3, colors)

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.4, hspace=0.4)

    plt.show()
    
if __name__ == "__main__":
    main()
