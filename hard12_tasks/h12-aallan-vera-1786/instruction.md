You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

The collector marks free blocks: a stale payload word reaching the free list retains the whole free chain, and a 599-key string map traps in `$gc_collect`

## Description

The collector's mark phase scans free blocks. The sweep writes the free-list link into a freed block's first payload word and leaves the rest of the payload as it was, `$alloc` hands a block out whole with no zeroing, and `$gc_is_base` accepts any block on the allocation chain, so a stale word that points at a block on the free list marks that block, the free chain behind it and every stale graph those blocks still hold. The effect is silent false retention at every collection, and it becomes loud once the retained graph pushes the mark worklist past its 16,384 entries: a `Map<String, Int>` built by `map_insert` over 599 keys traps `unreachable` in `$gc_collect`, where 598 keys return 598.

## Mechanism, Class and Instances

Three facts combine: (1) `$sweep` links a freed block into the free list through `payload[0]` and does not clear the remaining payload words; (2) `$alloc` reuses a block whole, without splitting or zeroing, so a live object can hold stale words from the block's previous life until it overwrites them; (3) `$gc_is_base` answers true for any block on the allocation chain, free or live. A stale word in a scanned object that happens to equal a free block's address is therefore taken as a pointer, the free block is marked and scanned, its `payload[0]` is the next free block, and the whole free chain and every stale graph behind it is marked. The class is every program whose heap has been through a collection and whose live objects carry stale words from reused blocks: in practice any program that allocates, frees and allocates again, with string keys or other small heap values making the stale words likely to hit. Measured at `main` f9ca14f8 and 02319ac7 (the collector is unchanged between them) by PR #1715's and #1510's lanes' WAT instrument: at the overflowing collection (the 77th of the 599-key run) 14,519 of the 16,384 worklist entries were blocks on the free list, out of 17,053 free blocks in all, with 10,720 distinct values pending (10,762 three-byte and 4,543 two-byte key strings where 900 and 90 distinct keys exist, plus 157 old buckets); in a 2,000-key run the object being scanned when the worklist filled was itself a free block.

- [ ] `Map<String, Int>` built by `map_insert` over 599 keys (program below): traps natively and in the browser harness; 598 keys return 598. A string-keyed map first traps at 596 keys with the `map_keys` variant and is erratic past the onset (597, 599, 600, 605 and 700 complete; 596, 598, 601, 610, 800 and 1000 trap), which is what a stale-word-dependent mechanism looks like.

Related: issue #1510 (the mark worklist's fixed capacity) is the mechanism that turns the retention loud; its fix (overflow-tolerant marking) removes the trap and leaves the retention, which this issue tracks. Issue #1676 (persistent `Map` and `Set` in generated code) changes what this shape allocates but not the collector's rule.

## Effect

Silent at every collection (memory that should be reclaimed is retained, and stale graphs are kept alive); loud today when the retained graph exceeds the worklist (an `unreachable` trap in `$gc_collect`, reported with the generic five-cause text). After #1510's fix: silent only.

## Reach

A map of a few hundred string keys built by a fold: a word count. No corpus program reaches the onset; `tests/test_codegen_gc_reclamation.py`'s 10,000-insert chain uses integer keys.

## Vera Code

```vera
public fn main(-> @Int)
  requires(true) ensures(true) effects(pure)
{
  let @Map<String, Int> = map_new();
  let @Map<String, Int> = array_fold(array_range(0, 599), @Map<String, Int>.0, fn(@Map<String, Int>, @Int -> @Map<String, Int>) effects(pure) { map_insert(@Map<String, Int>.0, int_to_string(@Int.0), @Int.0) });
  map_size(@Map<String, Int>.0)
}
```

## Expected Behaviour

`vera run` prints 599; a collection marks live objects only, so a freed block is never scanned and the free list never retains a graph.

## Actual Behaviour

`vera run` dies with `Error: Reached unreachable WASM instruction` inside `$gc_collect`.

## Fix direction

Any one of the three facts removed closes the class: `$gc_is_base` rejecting a block whose header says free (one bit test per candidate pointer), or `$sweep` clearing a freed block's payload, or `$alloc` zeroing a block on reuse. The first is the cheapest at collection time and leaves allocation untouched; the instrument is the 599-key program plus a width matrix of maps and arrays of small strings across the former onset, under `VERA_EAGER_GC=1` and ordinary collection, on the three targets, asserting the run's value, with a collector counter or the WAT instrument asserting that no free block is ever marked.

## Environment

- Vera version: `main` at 02319ac7 (v0.2.3 plus the v0.2.4 wave-1 merges)
- Python version: 3.14
- OS: macOS; the browser harness (Node) traps the same way

