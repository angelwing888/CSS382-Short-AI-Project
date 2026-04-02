from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Load balance data
DATA_FILE = 'balance_data.json'

def load_balance_data():
    """Load balance data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


@app.route('/')
def index():
    """Render main page"""
    heroes = load_balance_data()
    # Sort heroes alphabetically
    sorted_heroes = sorted(heroes.keys())
    return render_template('index.html', heroes=sorted_heroes, total_heroes=len(heroes))


@app.route('/api/hero/<hero_name>')
def get_hero_adjustments(hero_name):
    """Get adjustments for a specific hero"""
    heroes = load_balance_data()
    
    if hero_name in heroes:
        return jsonify({
            'name': hero_name,
            'adjustments': heroes[hero_name]
        })
    
    return jsonify({'error': 'Hero not found'}), 404


@app.route('/api/heroes')
def get_all_heroes():
    """Get all heroes and their adjustment counts"""
    heroes = load_balance_data()
    
    heroes_summary = []
    for hero_name, adjustments in heroes.items():
        heroes_summary.append({
            'name': hero_name,
            'adjustment_count': len(adjustments)
        })
    
    # Sort by adjustment count (most adjusted first)
    heroes_summary.sort(key=lambda x: x['adjustment_count'], reverse=True)
    
    return jsonify(heroes_summary)


@app.route('/api/stats')
def get_stats():
    """Get overall statistics"""
    heroes = load_balance_data()
    
    total_adjustments = sum(len(adjustments) for adjustments in heroes.values())
    
    return jsonify({
        'total_heroes': len(heroes),
        'total_adjustments': total_adjustments,
        'most_adjusted': max(heroes.items(), key=lambda x: len(x[1]))[0] if heroes else None
    })


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
