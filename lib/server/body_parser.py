from typing import List

import server.data as data
import log

def is_ready() -> bool:
    return data.action_count != None

def parse(action_count: int | None, state: List[int] | None, score: int | None, lost: bool | None) -> None:
    if data.action_count == None and action_count != None:
        data.action_count = action_count
        log.verbose(f"Spēles darbību skaits iestatīts: {data.action_count}")
    
    if data.action_count == None:
        return
    
    # Updated fields
    if state != None:
        data.curr_state = state
    
    if score != None:
        data.curr_score = score
    
    if lost != None:
        data.has_lost = lost