"""Flywheel — capture, inject, compound."""
from .tile import Tile, TileStore
from .room import Room


class Flywheel:
    """
    The compounding loop: every exchange becomes a tile,
    tiles inject context into future exchanges, the flywheel compounds.
    """
    
    def __init__(self, data_dir="data"):
        self.store = TileStore(path=f"{data_dir}/tiles.jsonl")
        self.rooms = {}
        self.history = []
    
    def ensure_room(self, name, description=""):
        if name not in self.rooms:
            self.rooms[name] = Room(name=name, description=description, store=self.store)
        return self.rooms[name]
    
    def record(self, question, answer, room="general", confidence=0.5, tags=None):
        r = self.ensure_room(room)
        tile = r.feed(question=question, answer=answer, confidence=confidence, tags=tags)
        self.history.append({"q": question, "room": room, "tile": tile.id})
        return tile
    
    def get_context(self, question, rooms=None, limit=8):
        contexts = []
        for name in (rooms or list(self.rooms.keys())):
            if name in self.rooms:
                match = self.rooms[name].query(question)
                if match:
                    contexts.append(match)
        contexts.sort(key=lambda t: t.priority, reverse=True)
        if not contexts:
            return ""
        lines = ["[Previous knowledge:]"]
        for t in contexts[:limit]:
            lines.append(f"  Q: {t.question}")
            lines.append(f"  A: {t.answer[:200]} (conf: {t.confidence:.2f})")
        return "\n".join(lines)
    
    def stats(self):
        return {
            "tiles": self.store.count,
            "rooms": {n: {"tiles": len(r.tiles), "sentiment": round(r.sentiment, 2)}
                      for n, r in self.rooms.items()},
            "exchanges": len(self.history),
        }
