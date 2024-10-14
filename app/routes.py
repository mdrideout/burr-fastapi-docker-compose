from fastapi import APIRouter
from loguru import logger

from burr.core import ApplicationBuilder, expr
from burr.tracking import LocalTrackingClient

from app.actions import add_random_number, calculate_sum, end_flow, start_flow

router = APIRouter()


@router.get("/")
def root_example_flow(lucky_number: int):
    logger.info("Root route called")

    # Configure the tracking client
    tracker = LocalTrackingClient(
        project="fastapi_burr_example_project",
        storage_dir="/burr-data",  # The mounted volume path for burr data to be stored
    )

    # Create a burr application
    application = (
        ApplicationBuilder()
        # Define the actions we will be using
        .with_actions(
            # Bind the lucky_number parameter to the action due to the action's input requirement
            start_flow=start_flow.bind(lucky_number=lucky_number),
            add_random_number=add_random_number,
            calculate_sum=calculate_sum,
            end_flow=end_flow,
        )
        # Define the valid transitions between actions (edges in a graph of action nodes)
        # Cycle includes logic to evaluate the counter value
        .with_transitions(
            ("start_flow", "add_random_number"),
            ("add_random_number", "calculate_sum"),
            (
                "calculate_sum",
                "add_random_number",
                expr("counter<3"),  # evaluates to true if counter is less than 3
            ),
            ("calculate_sum", "end_flow"),
        )
        # Initial state - application has a cycle that continues until the counter reaches a threshold
        .with_state(counter=0)
        .with_entrypoint("start_flow")
        .with_tracker(tracker)
        .build()
    )

    action, result, state = application.run(halt_after=["end_flow"])

    # Log the result
    logger.info(f"Action: {action}")
    logger.info(f"Final Result: {result}")
    logger.info(f"Final State: {state}")

    return result
