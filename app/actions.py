from typing import Tuple
import random
from loguru import logger
from burr.core import action, State


@action(reads=[], writes=["lucky_number"])
def start_flow(state: State, lucky_number: int) -> State:
    logger.info(f"Saving lucky number to state: {lucky_number}")
    return state.update(lucky_number=lucky_number)


@action(reads=[], writes=["random_number"])
def add_random_number(state: State) -> State:
    # Generate a random_number between 1 and 100
    random_number = random.randint(1, 100)

    # Write the random_number to state
    return state.update(random_number=random_number)


@action(reads=["lucky_number", "random_number", "counter"], writes=["sum"])
def calculate_sum(state: State) -> Tuple[dict, State]:
    logger.info(f"Calculating sum. Counter: {state['counter']}")

    # Read the lucky_number and random_number from state
    lucky_number = state["lucky_number"]
    random_number = state["random_number"]

    # Calculate the sum
    sum = lucky_number + random_number

    # Write the sum to state, and increment the counter
    # Also returns the result dict purely for example purposes
    return {"sum": sum}, state.update(sum=sum, counter=state["counter"] + 1)


@action(reads=[""], writes=[])
def end_flow(state: State) -> Tuple[dict, State]:
    logger.info("End of flow")
    return {}, state
