# ============================================================
#  Alpha-Beta Pruning — Interactive Tree Visualizer
#  Input a game tree, see the pruning happen step-by-step.
# ============================================================

# ── Tree representation ──────────────────────────────────────
# Node = {"val": int|None,  "children": [...]}
# Leaf nodes have a val; internal nodes have val=None.

def make_leaf(v):     return {"val": v,    "children": []}
def make_node(*kids): return {"val": None, "children": list(kids)}

# ── Example tree (depth-3) ───────────────────────────────────
#          MAX
#         / | \
#        /  |  \
#      MIN MIN MIN
#     /\   /\   /\
#    3  5 2  9 1  7
default_tree = make_node(
    make_node(make_leaf(3),  make_leaf(5)),
    make_node(make_leaf(2),  make_leaf(9)),
    make_node(make_leaf(1),  make_leaf(7)),
)

log    = []   # step-by-step explanation
pruned = []   # which nodes were pruned

# ── Alpha-Beta Algorithm ─────────────────────────────────────
def alpha_beta(node, depth, alpha, beta, is_max, path="root"):
    if not node["children"]:          # leaf
        log.append(f"  LEAF {path} = {node['val']}")
        return node["val"]

    layer = "MAX" if is_max else "MIN"
    log.append(f"\n{'  '*depth}[{layer}] {path}  α={alpha}  β={beta}")

    if is_max:
        value = -999
        for i, child in enumerate(node["children"]):
            child_path = f"{path}→{i}"
            child_val  = alpha_beta(child, depth+1, alpha, beta, False, child_path)
            value      = max(value, child_val)
            alpha      = max(alpha, value)
            log.append(f"{'  '*depth}  ↳ child val={child_val}  new α={alpha}")
            if alpha >= beta:
                # prune remaining siblings
                for j in range(i+1, len(node["children"])):
                    pruned.append(f"{path}→{j}")
                log.append(f"{'  '*depth}  ✂ PRUNED remaining children (α≥β: {alpha}≥{beta})")
                break
    else:
        value = 999
        for i, child in enumerate(node["children"]):
            child_path = f"{path}→{i}"
            child_val  = alpha_beta(child, depth+1, alpha, beta, True, child_path)
            value      = min(value, child_val)
            beta       = min(beta, value)
            log.append(f"{'  '*depth}  ↳ child val={child_val}  new β={beta}")
            if alpha >= beta:
                for j in range(i+1, len(node["children"])):
                    pruned.append(f"{path}→{j}")
                log.append(f"{'  '*depth}  ✂ PRUNED remaining children (α≥β: {alpha}≥{beta})")
                break

    node["val"] = value
    return value


# ── ASCII Tree printer ────────────────────────────────────────
def print_tree(node, prefix="", is_last=True, path="root"):
    connector  = "└── " if is_last else "├── "
    pruned_tag = "  ✂PRUNED" if path in pruned else ""
    val_str    = str(node["val"]) if node["val"] is not None else "?"
    print(f"{prefix}{connector}[{val_str}]{pruned_tag}  ({path})")

    child_prefix = prefix + ("    " if is_last else "│   ")
    for i, child in enumerate(node["children"]):
        last = (i == len(node["children"]) - 1)
        print_tree(child, child_prefix, last, f"{path}→{i}")


# ── Custom tree builder ───────────────────────────────────────
def build_tree_from_input():
    print("\nEnter leaf values row by row (comma-separated).")
    print("Example — 2 MIN nodes each with 2 leaves:")
    print("  Row 1: 3,5")
    print("  Row 2: 2,9")
    print("(Press ENTER with empty line when done)\n")

    groups = []
    while True:
        line = input("Leaf group: ").strip()
        if not line:
            break
        try:
            vals = [int(x) for x in line.split(",")]
            groups.append(vals)
        except ValueError:
            print("  ⚠ Only integers please.")

    if not groups:
        return None

    # Build MIN nodes from each group, then wrap in MAX root
    min_nodes = [make_node(*[make_leaf(v) for v in g]) for g in groups]
    return make_node(*min_nodes)


# ── Main ──────────────────────────────────────────────────────
print("=" * 55)
print("       ALPHA-BETA PRUNING VISUALIZER")
print("=" * 55)
print("\n1 — Use built-in example tree")
print("2 — Enter your own leaf values")
choice = input("\nChoice (1/2): ").strip()

tree = None
if choice == "2":
    tree = build_tree_from_input()

if tree is None:
    tree = default_tree
    print("\nUsing default example tree.")

print("\n── Running Alpha-Beta Pruning ──────────────────────────")
best_val = alpha_beta(tree, 0, -999, 999, True)

print("\n── Step-by-step log ────────────────────────────────────")
for line in log:
    print(line)

print("\n── Tree with pruning marked ────────────────────────────")
print_tree(tree)

print(f"\n✓  Optimal value at root = {best_val}")
if pruned:
    print(f"✂  Pruned nodes          = {pruned}")
else:
    print("   No nodes were pruned.")