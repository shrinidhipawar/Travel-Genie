import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10

# Create output directory
import os
os.makedirs('docs/figures', exist_ok=True)

# Figure 6.1 - Response Time Distribution
fig, ax = plt.subplots(figsize=(10, 6))
trip_types = ['Single\n3-day', 'Single\n7-day', 'Multi\n2-city', 'Multi\n3-city', 'Multi\n4-city', 'Multi\n5-city']
avg_times = [8.4, 11.2, 13.7, 16.9, 18.5, 20.2]
min_times = [5.2, 7.8, 10.1, 12.3, 14.1, 15.8]
max_times = [12.1, 15.3, 18.4, 22.7, 24.3, 26.1]

x = np.arange(len(trip_types))
ax.bar(x, avg_times, color='#667eea', alpha=0.8, label='Average')
ax.errorbar(x, avg_times, yerr=[np.array(avg_times)-np.array(min_times), 
                                  np.array(max_times)-np.array(avg_times)],
            fmt='none', ecolor='#333', capsize=5, alpha=0.6)
ax.axhline(y=15, color='red', linestyle='--', label='Target (15s)', linewidth=2)
ax.set_xlabel('Trip Type', fontsize=12, fontweight='bold')
ax.set_ylabel('Response Time (seconds)', fontsize=12, fontweight='bold')
ax.set_title('Figure 6.1: Response Time Distribution by Trip Type', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(trip_types)
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('docs/figures/fig6_1_response_time.png', dpi=300, bbox_inches='tight')
plt.close()

# Figure 6.2 - Component-wise Latency
fig, ax = plt.subplots(figsize=(10, 6))
components = ['API Fetching', 'RAG Retrieval', 'LLM Generation', 'Post-processing']
times = [3.2, 1.8, 4.6, 1.2]
percentages = [30, 17, 43, 11]
colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe']

bars = ax.barh(components, times, color=colors, alpha=0.8)
for i, (bar, pct) in enumerate(zip(bars, percentages)):
    width = bar.get_width()
    ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
            f'{times[i]}s ({pct}%)', va='center', fontweight='bold')

ax.set_xlabel('Time (seconds)', fontsize=12, fontweight='bold')
ax.set_title('Figure 6.2: Component-wise Latency Breakdown\nTotal Average: 10.8 seconds', 
             fontsize=14, fontweight='bold')
ax.set_xlim(0, 6)
plt.tight_layout()
plt.savefig('docs/figures/fig6_2_latency.png', dpi=300, bbox_inches='tight')
plt.close()

# Figure 6.4 - Relevance Score Distribution
fig, ax = plt.subplots(figsize=(10, 6))
score_ranges = ['4.5-5.0\n(Excellent)', '4.0-4.4\n(Good)', '3.5-3.9\n(Acceptable)', '<3.5\n(Poor)']
percentages = [62, 28, 8, 2]
colors = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444']

bars = ax.bar(score_ranges, percentages, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
for bar, pct in zip(bars, percentages):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 1, f'{pct}%', 
            ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_ylabel('Percentage of Itineraries (%)', fontsize=12, fontweight='bold')
ax.set_xlabel('Relevance Score Range', fontsize=12, fontweight='bold')
ax.set_title('Figure 6.4: Relevance Score Distribution\nAverage: 4.47/5.0 (Target: 4.0)', 
             fontsize=14, fontweight='bold')
ax.set_ylim(0, 70)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('docs/figures/fig6_4_relevance.png', dpi=300, bbox_inches='tight')
plt.close()

# Figure 6.5 - Factual Accuracy by Data Source
fig, ax = plt.subplots(figsize=(10, 6))
sources = ['Wikipedia', 'Geoapify', 'Google\nPlaces', 'Restaurant\nRec.', 'Budget\nEst.', 'Operating\nHours']
accuracy = [97.8, 91.4, 94.6, 89.7, 88.3, 87.4]
colors_acc = ['#10b981' if a >= 90 else '#f59e0b' for a in accuracy]

bars = ax.bar(sources, accuracy, color=colors_acc, alpha=0.8, edgecolor='black', linewidth=1.5)
ax.axhline(y=90, color='red', linestyle='--', label='Target (90%)', linewidth=2)
ax.axhline(y=93.2, color='green', linestyle=':', label='Overall (93.2%)', linewidth=2)

for bar, acc in zip(bars, accuracy):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 0.5, f'{acc}%', 
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
ax.set_xlabel('Data Source', fontsize=12, fontweight='bold')
ax.set_title('Figure 6.5: Factual Accuracy by Data Source', fontsize=14, fontweight='bold')
ax.set_ylim(80, 100)
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('docs/figures/fig6_5_accuracy.png', dpi=300, bbox_inches='tight')
plt.close()

# Figure 6.6 - User Satisfaction Scores
fig, ax = plt.subplots(figsize=(10, 6))
dimensions = ['Ease of\nUse', 'Interface\nDesign', 'Quality of\nRecommendations', 'Overall\nSatisfaction']
scores = [4.6, 4.5, 4.3, 4.4]
colors_sat = ['#667eea', '#764ba2', '#f093fb', '#4facfe']

bars = ax.bar(dimensions, scores, color=colors_sat, alpha=0.8, edgecolor='black', linewidth=1.5)
ax.axhline(y=4.2, color='red', linestyle='--', label='Target (4.2)', linewidth=2)

for bar, score in zip(bars, scores):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 0.05, f'{score}', 
            ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_ylabel('Score (out of 5.0)', fontsize=12, fontweight='bold')
ax.set_xlabel('Dimension', fontsize=12, fontweight='bold')
ax.set_title('Figure 6.6: User Satisfaction Scores by Dimension\n(n=50 users)', 
             fontsize=14, fontweight='bold')
ax.set_ylim(3.5, 5.0)
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('docs/figures/fig6_6_satisfaction.png', dpi=300, bbox_inches='tight')
plt.close()

# Figure 6.7 - System Comparison
fig, ax = plt.subplots(figsize=(12, 6))
systems = ['TravelGenie', 'ChatGPT-4', 'Gemini', 'Lonely\nPlanet', 'TripAdvisor\nManual', 'Human\nAgent']
relevance = [4.47, 4.12, 4.08, 4.31, 3.95, 4.58]
colors_sys = ['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6', '#ec4899', '#14b8a6']

bars = ax.bar(systems, relevance, color=colors_sys, alpha=0.8, edgecolor='black', linewidth=1.5)
ax.axhline(y=4.0, color='red', linestyle='--', label='Target (4.0)', linewidth=2)

for bar, rel in zip(bars, relevance):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 0.03, f'{rel}', 
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_ylabel('Relevance Score (out of 5.0)', fontsize=12, fontweight='bold')
ax.set_xlabel('System', fontsize=12, fontweight='bold')
ax.set_title('Figure 6.7: Multi-System Performance Comparison\nTravelGenie vs. Competing Solutions', 
             fontsize=14, fontweight='bold')
ax.set_ylim(3.5, 5.0)
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('docs/figures/fig6_7_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# Figure 6.8 - Cost Efficiency Comparison
fig, ax = plt.subplots(figsize=(12, 7))
systems_cost = ['TravelGenie', 'ChatGPT-4', 'Gemini', 'TripAdvisor\nManual', 'Lonely\nPlanet', 'Human\nAgent']
costs = [0.0051, 0.15, 0.08, 1.88, 3.42, 125.04]
colors_cost = ['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6', '#ec4899', '#ef4444']

bars = ax.bar(systems_cost, costs, color=colors_cost, alpha=0.8, edgecolor='black', linewidth=1.5)

for bar, cost in zip(bars, costs):
    height = bar.get_height()
    if cost < 1:
        label = f'${cost:.4f}'
    elif cost < 10:
        label = f'${cost:.2f}'
    else:
        label = f'${cost:.2f}'
    ax.text(bar.get_x() + bar.get_width()/2, height + 2, label, 
            ha='center', va='bottom', fontsize=10, fontweight='bold', rotation=0)

ax.set_ylabel('Cost per Itinerary (USD, log scale)', fontsize=12, fontweight='bold')
ax.set_xlabel('System', fontsize=12, fontweight='bold')
ax.set_title('Figure 6.8: Cost Efficiency Comparison\nTravelGenie is 29x cheaper than ChatGPT-4, 24,519x cheaper than Human Agent', 
             fontsize=14, fontweight='bold')
ax.set_yscale('log')
ax.grid(axis='y', alpha=0.3, which='both')
plt.tight_layout()
plt.savefig('docs/figures/fig6_8_cost.png', dpi=300, bbox_inches='tight')
plt.close()

# Figure 6.15 - System Availability
fig, ax = plt.subplots(figsize=(12, 6))
days = list(range(1, 31))
uptime = [100] * 30
uptime[9] = 87.5  # Day 10: 3-hour maintenance
uptime[22] = 94.6  # Day 23: 1.3-hour outage

ax.fill_between(days, uptime, 99, color='#10b981', alpha=0.3, label='Above Target')
ax.fill_between(days, 0, uptime, color='#10b981', alpha=0.6)
ax.plot(days, uptime, color='#059669', linewidth=2.5, marker='o', markersize=4)
ax.axhline(y=99, color='red', linestyle='--', label='Target (99%)', linewidth=2)

# Annotate downtime events
ax.annotate('Scheduled\nMaintenance\n(3h)', xy=(10, 87.5), xytext=(10, 80),
            arrowprops=dict(arrowstyle='->', color='red', lw=2),
            fontsize=10, ha='center', color='red', fontweight='bold')
ax.annotate('Unplanned\nOutage\n(1.3h)', xy=(23, 94.6), xytext=(23, 88),
            arrowprops=dict(arrowstyle='->', color='orange', lw=2),
            fontsize=10, ha='center', color='orange', fontweight='bold')

ax.set_xlabel('Day of Month', fontsize=12, fontweight='bold')
ax.set_ylabel('Uptime (%)', fontsize=12, fontweight='bold')
ax.set_title('Figure 6.15: System Availability Over 30 Days\nOverall: 99.4% (Target: 99%)', 
             fontsize=14, fontweight='bold')
ax.set_ylim(75, 101)
ax.set_xlim(0, 31)
ax.legend(loc='lower right')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('docs/figures/fig6_15_availability.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ All 8 figures generated successfully in docs/figures/")
print("\nGenerated files:")
print("- fig6_1_response_time.png")
print("- fig6_2_latency.png")
print("- fig6_4_relevance.png")
print("- fig6_5_accuracy.png")
print("- fig6_6_satisfaction.png")
print("- fig6_7_comparison.png")
print("- fig6_8_cost.png")
print("- fig6_15_availability.png")
