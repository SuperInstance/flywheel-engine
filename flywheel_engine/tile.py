"""Tiles — immutable knowledge units with priority scoring."""
import hashlib
import time
import math
import json
import os


class Tile:
    __slots__ = ("id", "question", "answer", "domain", "confidence",
                 "source", "tags", "timestamp", "usage_count", "success_count", "version")
    
    def __init__(self, question, answer, domain="general", confidence=0.5,
                 source="agent", tags=None, id="", timestamp=0.0):
        self.question = question
        self.answer = answer
        self.domain = domain
        self.confidence = confidence
        self.source = source
        self.tags = tags or []
        self.id = id or hashlib.md5(f"{question}:{answer}:{domain}".encode()).hexdigest()[:12]
        self.timestamp = timestamp or time.time()
        self.usage_count = 0
        self.success_count = 0
        self.version = 1
    
    def record_use(self, success=True):
        self.usage_count += 1
        if success:
            self.success_count += 1
    
    @property
    def success_rate(self):
        return self.success_count / max(self.usage_count, 1)
    
    @property
    def priority(self):
        return (math.log(self.usage_count + 1) + 0.5) * self.confidence * max(self.success_rate, 0.5)
    
    def to_dict(self):
        return {s: getattr(self, s) for s in self.__slots__}


class TileStore:
    """JSONL-persistent tile storage."""
    
    def __init__(self, path="data/tiles.jsonl"):
        self.path = path
        self.tiles = {}
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self._load()
    
    def _load(self):
        if os.path.exists(self.path):
            for line in open(self.path):
                if line.strip():
                    try:
                        d = json.loads(line)
                        t = Tile(d["question"], d["answer"], d.get("domain", "general"),
                                d.get("confidence", 0.5), d.get("source", "agent"),
                                d.get("tags"), d.get("id", ""), d.get("timestamp", 0))
                        t.usage_count = d.get("usage_count", 0)
                        t.success_count = d.get("success_count", 0)
                        t.version = d.get("version", 1)
                        self.tiles[t.id] = t
                    except:
                        pass
    
    def _save(self):
        with open(self.path, "w") as f:
            for t in self.tiles.values():
                f.write(json.dumps(t.to_dict()) + "\n")
    
    def add(self, tile):
        if tile.id in self.tiles:
            existing = self.tiles[tile.id]
            existing.version += 1
            existing.answer = tile.answer
            existing.confidence = max(existing.confidence, tile.confidence)
        else:
            self.tiles[tile.id] = tile
        self._save()
        return self.tiles[tile.id]
    
    def all_tiles(self):
        return list(self.tiles.values())
    
    @property
    def count(self):
        return len(self.tiles)
