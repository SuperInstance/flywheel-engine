# flywheel-engine

The compounding intelligence loop: every exchange becomes a tile, tiles inject context, the system compounds.

## The Flywheel

1. **Capture** — Agent interactions generate raw knowledge
2. **Refine** — Raw knowledge becomes structured tiles (via tile-refiner)
3. **Inject** — Tiles inject into agent context windows via PLATO rooms
4. **Compound** — Agents build on previous knowledge, generating deeper tiles
5. **Loop** — Each cycle produces more valuable knowledge than the last

## Installation

```bash
pip install flywheel-engine
```

## Usage

```python
from flywheel_engine import Flywheel, Tile, Room

room = Room(name='fleet_orchestration')
tile = Tile(question='How do agents coordinate?', answer='Via Bottle Protocol...')
room.add_tile(tile)

flywheel = Flywheel()
flywheel.add_room(room)
result = flywheel.compound()  # Returns compounded knowledge
```

## Architecture

The flywheel is the core of the Cocapn fleet's self-improving knowledge system. It transforms agent interactions into persistent, queryable knowledge that compounds over time.

## Part of the Cocapn Fleet

Works with tile-refiner (raw→structured), plato-tile-spec (format), and plato-server (storage).

## License

MIT