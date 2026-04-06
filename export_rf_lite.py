"""Exporta una versión optimizada del RF para predicción de viralidad de tweets.
Selecciona los árboles más compactos y minimiza el JSON para caber en GitHub (<100MB)."""
import json
import numpy as np
from pathlib import Path
from joblib import load

FEATURES = [
    'text_length', 'has_hashtag', 'has_mention', 'has_url',
    'has_question', 'has_exclamation', 'hour', 'day_of_week'
]

TARGET_MB = 90

def tree_to_dict(estimator):
    t = estimator.tree_
    return {
        'features': FEATURES,
        'children_left': t.children_left.tolist(),
        'children_right': t.children_right.tolist(),
        'feature': t.feature.tolist(),
        'threshold': [round(x, 4) for x in t.threshold.tolist()],
        'value': [[round(v, 2) for v in row] for row in t.value.squeeze(axis=1).tolist()]
    }

def tree_compactness(estimator):
    """Menor puntaje = árbol más compacto y ligero."""
    t = estimator.tree_
    return t.node_count

model = load('modelo_act4.joblib')
print(f'Modelo original: {len(model.estimators_)} arboles')

# Ordenar por compacidad (árboles más pequeños primero)
scored = sorted(enumerate(model.estimators_), key=lambda x: tree_compactness(x[1]))

selected = []
for idx, est in scored:
    selected.append(est)
    if len(selected) % 10 == 0:
        test = json.dumps([tree_to_dict(e) for e in selected], separators=(',', ':'))
        size_mb = len(test.encode('utf-8')) / (1024 * 1024)
        print(f'  {len(selected)} arboles -> ~{size_mb:.1f} MB')
        if size_mb > TARGET_MB * 0.85:
            selected.pop()
            break

print(f'\nSeleccionados: {len(selected)} arboles (los mas compactos)')

payload = {
    'model_type': 'RandomForestClassifier',
    'n_estimators': len(selected),
    'features': FEATURES,
    'classes': model.classes_.tolist() if hasattr(model.classes_, 'tolist') else [0, 1],
    'trees': [tree_to_dict(est) for est in selected]
}

js = 'window.RF_MODEL=' + json.dumps(payload, separators=(',', ':'), ensure_ascii=False) + ';\n'
Path('rf_model.js').write_text(js, encoding='utf-8')
size_mb = Path('rf_model.js').stat().st_size / (1024 * 1024)
print(f'Archivo final: {size_mb:.1f} MB')
if size_mb < 100:
    print('OK - Cabe en GitHub!')
else:
    print('ADVERTENCIA - Aun es muy grande, se necesitan menos arboles')
