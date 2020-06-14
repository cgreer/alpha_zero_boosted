import sys
from environment_registry import get_env_module
from agent_configuration import configure_agent

# script.py <environment> <p1 bot name> <p2 bot_name>
# script.py connect_four mcts_naive-6 human
environment, p1_bot_name, p2_bot_name, consideration_time = sys.argv[1:]
consideration_time = float(consideration_time)


def setup_agent(bot_name, consideration_time):
    species, generation = bot_name.split("-")
    generation = int(generation)

    agent_class, agent_settings = configure_agent(
        environment,
        species,
        generation,
        play_setting="tournament",
    )

    # Fix the amount of time per move for bots
    if "move_consideration_time" in agent_settings:
        agent_settings["move_consideration_time"] = consideration_time

    return agent_class, agent_settings


P1_agent_class, p1_agent_settings = setup_agent(p1_bot_name, consideration_time)
P2_agent_class, p2_agent_settings = setup_agent(p2_bot_name, consideration_time)

env_module = get_env_module(environment)

environment = env_module.Environment()

agent_1 = P1_agent_class(environment=environment, **p1_agent_settings)
agent_2 = P2_agent_class(environment=environment, ** p2_agent_settings)

environment.add_agent(agent_1)
environment.add_agent(agent_2)

environment.run()
