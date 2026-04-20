import sys, os, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flywheel_engine import Tile, TileStore, Room, Flywheel

def test_tile():
    t = Tile(question="test", answer="test", confidence=0.8)
    assert t.id and t.priority > 0
    t.record_use(True)
    assert t.success_rate == 1.0
    print("PASS: tile")

def test_room():
    with tempfile.TemporaryDirectory() as tmp:
        store = TileStore(path=f"{tmp}/t.jsonl")
        room = Room(name="code", store=store)
        room.feed("How to read a file?", "open(f)", confidence=0.9)
        room.feed("How to sort?", "sorted(lst)", confidence=0.8)
        r = room.query("read file")
        assert r and "open" in r.answer
        print("PASS: room")

def test_flywheel():
    with tempfile.TemporaryDirectory() as tmp:
        fw = Flywheel(data_dir=tmp)
        fw.record("What is Rust?", "A systems language", room="code", confidence=0.8)
        fw.record("What is Python?", "An interpreted language", room="code", confidence=0.9)
        ctx = fw.get_context("Tell me about Rust")
        assert "Rust" in ctx
        print("PASS: flywheel")

def test_persistence():
    with tempfile.TemporaryDirectory() as tmp:
        fw = Flywheel(data_dir=tmp)
        fw.record("persist?", "yes", room="general", confidence=0.9)
        fw2 = Flywheel(data_dir=tmp)
        assert fw2.store.count == 1
        print("PASS: persistence")

if __name__ == "__main__":
    test_tile()
    test_room()
    test_flywheel()
    test_persistence()
    print("\nAll 4 pass. The flywheel compounds.")
