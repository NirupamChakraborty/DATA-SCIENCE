import math

log = []
pruned = set()


def build_tree(depth, branching, leaves, idx=0):
    """Recursively build tree. Leaves are filled left-to-right."""
    if depth == 0:
        val = leaves[idx % len(leaves)]
        return {"val": val, "children": [], "id": idx}, idx + 1
    children = []
    for _ in range(branching):
        child, idx = build_tree(depth - 1, branching, leaves, idx)
        children.append(child)
    return {"val": None, "children": children, "id": None}, idx


#  Alpha-Beta
def alpha_beta(node, depth, alpha, beta, is_max, path="root"):
    if not node["children"]:
        log.append(f"  LEAF {path} = {node['val']}")
        return node["val"]

    layer = "MAX" if is_max else "MIN"
    log.append(f"\n{'  '*depth}[{layer}] {path}  α={alpha}  β={beta}")

    if is_max:
        value = -math.inf
        for i, child in enumerate(node["children"]):
            cp = f"{path}→{i}"
            cv = alpha_beta(child, depth+1, alpha, beta, False, cp)
            value = max(value, cv)
            alpha = max(alpha, value)
            log.append(f"{'  '*depth}  ↳ child={cv}  α={alpha}  β={beta}")
            if alpha >= beta:
                for j in range(i+1, len(node["children"])):
                    pruned.add(f"{path}→{j}")
                log.append(f"{'  '*depth}  ✂ PRUNED (α≥β: {alpha}≥{beta})")
                break
    else:
        value = math.inf
        for i, child in enumerate(node["children"]):
            cp = f"{path}→{i}"
            cv = alpha_beta(child, depth+1, alpha, beta, True, cp)
            value = min(value, cv)
            beta = min(beta, value)
            log.append(f"{'  '*depth}  ↳ child={cv}  α={alpha}  β={beta}")
            if alpha >= beta:
                for j in range(i+1, len(node["children"])):
                    pruned.add(f"{path}→{j}")
                log.append(f"{'  '*depth}  ✂ PRUNED (α≥β: {alpha}≥{beta})")
                break

    node["val"] = value
    return value


# Tree printer 
def print_tree(node, depth_left, prefix="", is_last=True, path="root"):
    connector  = "└── " if is_last else "├── "
    ptag       = "  ✂PRUNED" if path in pruned else ""
    layer      = "MAX" if (depth_left % 2 == 0) else "MIN"
    val_str    = str(node["val"]) if node["val"] is not None else "?"
    label      = f"[{val_str}] ({layer}){ptag}"
    if not node["children"]:
        label = f"[{val_str}] (leaf){ptag}"
    print(f"{prefix}{connector}{label}  {path}")
    child_prefix = prefix + ("    " if is_last else "│   ")
    for i, child in enumerate(node["children"]):
        last = (i == len(node["children"]) - 1)
        print_tree(child, depth_left-1, child_prefix, last, f"{path}→{i}")



def get_int(prompt, lo=1, hi=10):
    while True:
        try:
            v = int(input(prompt))
            if lo <= v <= hi:
                return v
            print(f"  ⚠ Enter a value between {lo} and {hi}.")
        except ValueError:
            print("  ⚠ Integers only.")

def get_leaf_values(n_leaves):
    print(f"\nEnter exactly {n_leaves} leaf values (space or comma separated):")
    while True:
        raw = input("  Values: ").replace(",", " ").split()
        try:
            vals = [int(x) for x in raw]
            if len(vals) == n_leaves:
                return vals
            print(f"  ⚠ Need exactly {n_leaves} values, got {len(vals)}.")
        except ValueError:
            print("  ⚠ Integers only.")


# Main part
print("=" * 55)
print("       ALPHA-BETA PRUNING — FLEXIBLE VISUALIZER")
print("=" * 55)

print("\n── Configure your tree ─────────────────────────────────")
depth     = get_int("Depth (levels below root, 1–6): ", 1, 6)
branching = get_int("Branching factor (children per node, 2–5): ", 2, 5)

n_leaves  = branching ** depth
print(f"\nThis tree will have  {n_leaves}  terminal (leaf) nodes.")

print("\n1 — Enter leaf values manually")
print("2 — Auto-fill with example values")
mode = input("Choice (1/2): ").strip()

if mode == "1":
    leaves = get_leaf_values(n_leaves)
else:
    import random
    random.seed(42)
    leaves = [random.randint(1, 10) for _ in range(n_leaves)]
    print(f"  Auto-generated leaves: {leaves}")

tree, _ = build_tree(depth, branching, leaves)

print("\n── Running Alpha-Beta Pruning ──────────────────────────")
best = alpha_beta(tree, 0, -math.inf, math.inf, True)

print("\n── Step-by-step log ────────────────────────────────────")
for line in log:
    print(line)

print("\nTree structure (with pruning) ")
print_tree(tree, depth)

print(f"\n Optimal value at root = {best}")
if pruned:
    print(f"Pruned nodes: {sorted(pruned)}")
else:
    print("No nodes pruned.")