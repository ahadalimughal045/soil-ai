import matplotlib.pyplot as plt
import numpy as np

# Set style
plt.style.use('dark_background')
accent_color = '#00ff88'
secondary_color = '#00bcd4'

def create_cost_chart():
    categories = ['Traditional Lab', 'Soil AI Agent']
    costs = [150, 2]
    
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(categories, costs, color=[secondary_color, accent_color], width=0.6)
    
    ax.set_ylabel('Cost per Analysis ($)', color='white', fontsize=12)
    ax.set_title('Cost Reduction: Traditional vs AI', color=accent_color, fontsize=14, fontweight='bold')
    
    # Add values on top
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 5, f'${yval}', ha='center', va='bottom', color='white', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('chart_cost.png', transparent=True)
    plt.close()

def create_yield_chart():
    years = ['Year 1', 'Year 2', 'Year 3', 'Year 4']
    traditional = [100, 102, 98, 101]
    soil_ai = [100, 115, 128, 142]
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(years, traditional, marker='o', color=secondary_color, label='Traditional Farming', linewidth=3)
    ax.plot(years, soil_ai, marker='s', color=accent_color, label='Soil AI (Nano-Optimized)', linewidth=3)
    
    ax.set_ylabel('Yield Index (%)', color='white', fontsize=12)
    ax.set_title('Yield Growth Projection', color=accent_color, fontsize=14, fontweight='bold')
    ax.legend()
    
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig('chart_yield.png', transparent=True)
    plt.close()

def create_accuracy_chart():
    samples = ['1k', '5k', '10k', '20k (Target)']
    accuracy = [72, 85, 94, 98]
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.fill_between(samples, accuracy, color=accent_color, alpha=0.3)
    ax.plot(samples, accuracy, color=accent_color, marker='o', linewidth=3)
    
    ax.set_ylabel('Confidence Score (%)', color='white', fontsize=12)
    ax.set_title('AI Training Efficiency', color=accent_color, fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('chart_accuracy.png', transparent=True)
    plt.close()

if __name__ == "__main__":
    create_cost_chart()
    create_yield_chart()
    create_accuracy_chart()
    print("Graphs generated successfully.")
