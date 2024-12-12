Random (RAND):
- Simplest algorithm - when a page fault occurs, it randomly selects any page in physical memory to replace
- Uses Python's random.randrange() to select a victim frame from 0 to 31 (since we have 32 physical pages)

First In First Out (FIFO):
- Maintains pages in order of arrival
- Always replaces the oldest page (the one that's been in memory the longest)
- In our implementation, we:
    - Always select frame 0 as the victim
    - After replacement, rotate the physical memory list to maintain FIFO order

Least Recently Used (LRU):
- Replaces the page that hasn't been used for the longest time
In our implementation:
    - Each page tracks its last access time
    - When choosing a victim, selects the page with the oldest last_access_time
    - For tiebreakers (same last access time):
        - Prefers to replace clean pages over dirty pages
        - If both pages are clean or both dirty, replaces the lower-numbered page

Page Replacement with Aging (PER):
- Uses reference bits and dirty bits with periodic reset
- Every 200 memory references, all reference bits are set to 0
- When selecting a victim, follows this priority order:
    - Unreferenced and clean pages (ref=0, dirty=0)
    - Unreferenced and dirty pages (ref=0, dirty=1)
    - Referenced and clean pages (ref=1, dirty=0)
    - Referenced and dirty pages (ref=1, dirty=1)
    - Within each category, selects the lowest-numbered page
- Implementation details:
    - Tracks references_since_reset counter
    - When counter hits 200, calls reset_reference_bits()
    - For each memory access:
        - Sets reference bit to 1
        - For writes, sets dirty bit to 1
