import asyncio
import random

EVENTS = ["try", "penalty", "yellow"]

async def simulate_match(match_id, db_interface, broadcaster):
    minute = 0

    await db_interface.update_match(match_id, {
        "status": "live"
    })

    while minute < 80:
        await asyncio.sleep(1)
        minute += 1

        await db_interface.update_match(match_id, {
            "minute": minute
        })

        if random.random() < 0.2:
            await generate_event(match_id, minute, db_interface)

        match = await db_interface.get_match(match_id)
        await broadcaster(match)

    await db_interface.update_match(match_id, {
        "status": "finished"
    })

async def generate_event(match_id, minute, db):
    team = random.choice(["home", "away"])
    event_type = random.choice(EVENTS)

    points = 0
    if event_type == "try":
        points = 5
    elif event_type == "penalty":
        points = 3

    match = await db.get_match(match_id)
    match["score"][team] += points

    await db.update_match(match_id, {
        "score": match["score"]
    })

    await db.add_event(match_id, {
        "minute": minute,
        "type": event_type,
        "team": team,
        "description": f"{event_type.upper()} {team}"
    })
