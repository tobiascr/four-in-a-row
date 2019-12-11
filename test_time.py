
from engine import EngineInterface as EngineInterface
import time

engine = EngineInterface(3)



t0 = time.perf_counter()
for n in range(100):
    engine.new_game()
    engine.make_move(3)
    move = engine.engine_move()
t1 = time.perf_counter()
print(t1-t0)

