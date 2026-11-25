from src.leaf import make_sample_leaf
for k in ["healthy", "yellow", "diseased"]:
    make_sample_leaf(k, f"sample_leaves/{k}.png")
print("Sample leaf images created in sample_leaves/")
