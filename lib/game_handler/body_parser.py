from typing import List

import game_handler.data as data
import log

def is_ready() -> bool:
    if data.state_size == None or data.action_count == None:
        return False
    else:
        return True

def parse(state_size: int | None, action_count: int | None, state: List[int] | None, score: int | None, lost: bool | None) -> None:
    if data.state_size == None and state_size != None:
        data.state_size = state_size
        log.verbose(f"Spēles stāvokļa izmērs iestatīts: {data.state_size}")

    if data.action_count == None and action_count != None:
        data.action_count = action_count
        log.verbose(f"Spēles darbību skaits iestatīts: {data.action_count}")
    
    if data.state_size == None or data.action_count == None:
        return
    
    # Updated fields
    if state != None:
        data.curr_state = state
    
    if score != None:
        data.curr_score = score
    
    if lost != None:
        data.has_lost = lost