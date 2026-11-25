"""Command-line demo: python main.py"""
from PIL import Image
from src.models import train_all, recommend_crops, predict_yield
from src.advisor import fertilizer_advice, irrigation_advice, disease_risk
from src.leaf import analyze_leaf

print("=== Training models ===")
train_all()

soil = dict(N=85, P=45, K=38, ph=6.2, temperature=25, humidity=80, rainfall=200)
print("\n=== Crop recommendation ===")
for crop, p in recommend_crops(**soil):
    print(f"  {crop:10s} {p}%")
best = recommend_crops(**soil)[0][0]
print(f"\n=== Yield for {best} (2 ha) ===")
print("  tonnes/ha, total:", predict_yield(best, **soil, area_ha=2))
print("\n=== Fertilizer advice ===")
for t in fertilizer_advice(best, soil["N"], soil["P"], soil["K"], soil["ph"]):
    print("  -", t)
print("\n=== Irrigation ===")
print(" ", irrigation_advice(best, soil_moisture=30, temperature=34, rain_chance=20))
print("\n=== Disease risk ===")
print(" ", disease_risk(85, 24, 10))
print("\n=== Leaf analysis ===")
for name in ["healthy", "yellow", "diseased"]:
    try:
        print(" ", name, "->", analyze_leaf(Image.open(f"sample_leaves/{name}.png")))
    except FileNotFoundError:
        print("  run make_samples.py first")
        break
