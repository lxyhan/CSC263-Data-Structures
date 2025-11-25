#!/usr/bin/env python3
from a3_submission import Queue, Tower

print("=== COMPLEX QUEUE STRESS TEST ===")
q = Queue(20)

# Insert many items in weird order
operations = [
    ( "add", (99, 2) ),
    ( "add", (42, 7) ),
    ( "add", (13, 5) ),
    ( "add", (13, 5) ),      # duplicate priority + obj
    ( "add", (17, 9) ),
    ( "add", (1, 10) ),      # highest priority so far
    ( "add", (555, 1) ),     # very low priority
    ( "add", (777, 11) ),    # new top
    ( "pop", None ),
    ( "add", (888, 3) ),
    ( "add", (4, 8) ),
    ( "pop", None ),
    ( "add", (5000, 10) ),   # ties with existing
    ( "pop", None ),
    ( "add", (123, 12) ),    # biggest so far
    ( "add", (321, 12) ),    # duplicate max priority
    ( "add", (222, 11) ),
    ( "pop", None ),
    ( "pop", None ),
    ( "add", (7777, 15) ),   # new giant
    ( "pop", None ),
    ( "pop", None ),
    ( "pop", None ),
]

step = 1
for op, arg in operations:
    print(f"\n--- Step {step}: {op} {arg if arg else ''} ---")
    if op == "add":
        obj, pri = arg
        q.add(obj, pri)
    else:
        removed = q.pop()
        print(f"Removed: ({removed.obj}, {removed.pri})" if removed else "Removed: None")

    print(f"Heap state: {[(node.obj, node.pri) for node in q.heap]}")
    step += 1

print("\n=== Testing Pops Until Empty ===")
while True:
    removed = q.pop()
    if not removed:
        print("Queue empty.")
        break
    print(f"Removed: ({removed.obj}, {removed.pri}) | New heap: {[(n.obj, n.pri) for n in q.heap]}")
    