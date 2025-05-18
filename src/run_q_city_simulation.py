import random
import matplotlib.pyplot as plt
from collections import Counter

class Agent:
    def __init__(self, unique_id, group, stance):
        self.unique_id = unique_id
        self.group = group  # "StatusQuo" or "Opposition"
        self.stance = stance  # -1 = Hardline, 0 = Moderate, 1 = Conciliatory

    def interact(self, other_agent):
        # Only interact with agents from other groups
        if self.group != other_agent.group:
            influence = other_agent.stance
            # Adjust stance slightly toward the other agent's stance
            self.stance += 0.5 * influence
            # Keep stance in range [-1, 1]
            self.stance = max(-1, min(1, self.stance))


class Simulation:
    def __init__(self, num_agents=100, steps=20):
        self.num_agents = num_agents
        self.steps = steps
        self.agents = []
        self.history = []

        # Initialize agents
        for i in range(num_agents):
            group = "StatusQuo" if i < num_agents // 2 else "Opposition"
            stance = random.choice([-1, 0, 1])
            self.agents.append(Agent(i, group, stance))

    def step(self):
        random.shuffle(self.agents)
        for i in range(0, self.num_agents, 2):
            a1 = self.agents[i]
            a2 = self.agents[i + 1] if i + 1 < self.num_agents else self.agents[0]
            a1.interact(a2)
            a2.interact(a1)

        # Record stance distribution
        self.record_history()

    def record_history(self):
        stance_counts = Counter()
        for agent in self.agents:
            rounded_stance = round(agent.stance)
            stance_counts[rounded_stance] += 1
        self.history.append(stance_counts)

    def run(self):
        self.record_history()
        for _ in range(self.steps):
            self.step()
        self.plot_results()

    def plot_results(self):
        time_series = { -1: [], 0: [], 1: [] }
        for t in self.history:
            for s in [-1, 0, 1]:
                time_series[s].append(t.get(s, 0))

        plt.plot(time_series[-1], label="Hardline (-1)")
        plt.plot(time_series[0], label="Moderate (0)")
        plt.plot(time_series[1], label="Conciliatory (+1)")
        plt.xlabel("Time Step")
        plt.ylabel("Number of Agents")
        plt.title("Agent Stance Evolution in Q City")
        plt.legend()
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    sim = Simulation(num_agents=100, steps=30)
    sim.run()
