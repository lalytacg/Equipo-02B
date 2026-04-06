"""Exporta un RandomForestClassifier de scikit-learn a un archivo JS utilizable en un prototipo HTML.

Uso:
    python export_rf_to_js.py --model modelo_act4.joblib --out rf_model.js
"""

import argparse
import json
from pathlib import Path

from joblib import load

FEATURES = [
    'text_length', 'has_hashtag', 'has_mention', 'has_url',
    'has_question', 'has_exclamation', 'hour', 'day_of_week'
]


def tree_to_dict(estimator):
    tree = estimator.tree_
    return {
        'features': FEATURES,
        'children_left': tree.children_left.tolist(),
        'children_right': tree.children_right.tolist(),
        'feature': tree.feature.tolist(),
        'threshold': tree.threshold.tolist(),
        'value': tree.value.squeeze(axis=1).tolist()
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, help='Ruta al .joblib del modelo Random Forest')
    parser.add_argument('--out', default='rf_model.js', help='Archivo JS de salida')
    args = parser.parse_args()

    model = load(args.model)
    if not hasattr(model, 'estimators_'):
        raise TypeError('El archivo no contiene un RandomForestClassifier compatible.')

    payload = {
        'model_type': type(model).__name__,
        'n_estimators': len(model.estimators_),
        'features': FEATURES,
        'classes': getattr(model, 'classes_', [0, 1]).tolist() if hasattr(getattr(model, 'classes_', None), 'tolist') else [0, 1],
        'trees': [tree_to_dict(est) for est in model.estimators_]
    }

    js = 'window.RF_MODEL = ' + json.dumps(payload, ensure_ascii=False) + ';\n'
    Path(args.out).write_text(js, encoding='utf-8')
    print(f'Modelo exportado correctamente a {args.out}')


if __name__ == '__main__':
    main()
