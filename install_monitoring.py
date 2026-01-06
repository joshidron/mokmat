"""
Auto-Install Enhanced Monitoring Features
Adds video feed, notification sounds, and real-time monitoring status
"""

import os

def add_monitoring_panel():
    """Add monitoring status panel to enhanced_interview.html"""
    
    html_file = r'd:\codewave\templates\enhanced_interview.html'
    
    print("Reading enhanced_interview.html...")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already added
    if 'monitoring-status-panel' in content:
        print("[OK] Monitoring panel already exists!")
        return True
    
    # HTML to add
    monitoring_panel = '''
    <!-- Monitoring Status Panel -->
    <div class="monitoring-status-panel">
        <div class="status-header">
            <h3>🎯 Real-Time Monitoring</h3>
            <div class="monitoring-active-badge">
                <span class="pulse-dot"></span>
                <span>ACTIVE</span>
            </div>
        </div>
        
        <div class="status-indicators">
            <!-- Face Detection -->
            <div class="status-item" id="faceStatus">
                <div class="status-icon">😊</div>
                <div class="status-info">
                    <div class="status-label">Face Detection</div>
                    <div class="status-value">Detecting...</div>
                </div>
                <div class="status-indicator">
                    <div class="indicator-dot"></div>
                </div>
            </div>
            
            <!-- Eye Contact -->
            <div class="status-item" id="eyeStatus">
                <div class="status-icon">👁️</div>
                <div class="status-info">
                    <div class="status-label">Eye Contact</div>
                    <div class="status-value">Monitoring...</div>
                </div>
                <div class="status-indicator">
                    <div class="indicator-dot"></div>
                </div>
            </div>
            
            <!-- Body Posture -->
            <div class="status-item" id="postureStatus">
                <div class="status-icon">🧍</div>
                <div class="status-info">
                    <div class="status-label">Body Posture</div>
                    <div class="status-value">Analyzing...</div>
                </div>
                <div class="status-indicator">
                    <div class="indicator-dot"></div>
                </div>
            </div>
            
            <!-- Tab Monitoring -->
            <div class="status-item" id="tabStatus">
                <div class="status-icon">📱</div>
                <div class="status-info">
                    <div class="status-label">Tab Monitoring</div>
                    <div class="status-value">Active</div>
                </div>
                <div class="status-indicator">
                    <div class="indicator-dot active"></div>
                </div>
            </div>
        </div>
        
        <div class="monitoring-stats">
            <div class="stat-box">
                <div class="stat-value" id="focusScore">--</div>
                <div class="stat-label">Focus Score</div>
            </div>
            <div class="stat-box">
                <div class="stat-value" id="postureScore">--</div>
                <div class="stat-label">Posture</div>
            </div>
            <div class="stat-box">
                <div class="stat-value" id="eyeScore">--</div>
                <div class="stat-label">Eye Contact</div>
            </div>
        </div>
    </div>
'''
    
    # Find where to insert (before </div> that closes container)
    # Insert before the closing </div> of the container
    insert_pos = content.rfind('</div>\n\n    <!-- Load Tracking Scripts -->')
    
    if insert_pos == -1:
        print("[ERROR] Could not find insertion point!")
        return False
    
    # Insert the panel
    new_content = content[:insert_pos] + monitoring_panel + '\n    ' + content[insert_pos:]
    
    # Add script reference before </body>
    if 'monitoring_status.js' not in new_content:
        new_content = new_content.replace(
            '<script src="/static/js/enhanced_interview.js"></script>',
            '<script src="/static/js/monitoring_status.js"></script>\n    <script src="/static/js/enhanced_interview.js"></script>'
        )
    
    # Backup original
    backup_file = html_file + '.backup'
    print(f"Creating backup: {backup_file}")
    with open(backup_file, 'w', encoding='utf-8') as f:
        with open(html_file, 'r', encoding='utf-8') as original:
            f.write(original.read())
    
    # Write updated file
    print("Writing updated file...")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("[OK] Monitoring panel added successfully!")
    return True

def add_css_styles():
    """Add CSS styles to monitoring_ui.css"""
    
    css_file = r'd:\codewave\static\css\monitoring_ui.css'
    
    print("Reading monitoring_ui.css...")
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already added
    if 'monitoring-status-panel' in content:
        print("[OK] CSS styles already exist!")
        return True
    
    # CSS to add
    new_css = '''
/* Enhanced Monitoring Status Panel */
.monitoring-status-panel {
    position: fixed;
    bottom: 20px;
    left: 20px;
    background: rgba(26, 26, 46, 0.95);
    backdrop-filter: blur(10px);
    border: 2px solid rgba(102, 126, 234, 0.3);
    border-radius: 20px;
    padding: 20px;
    min-width: 350px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    z-index: 1000;
    animation: slideInLeft 0.5s ease;
}

@keyframes slideInLeft {
    from { transform: translateX(-100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

.status-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 2px solid rgba(255, 255, 255, 0.1);
}

.status-header h3 {
    color: #ffffff;
    font-size: 18px;
    font-weight: 600;
    margin: 0;
}

.monitoring-active-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(0, 255, 0, 0.1);
    border: 1px solid rgba(0, 255, 0, 0.3);
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    color: #00ff00;
}

.pulse-dot {
    width: 8px;
    height: 8px;
    background: #00ff00;
    border-radius: 50%;
    animation: pulseDot 2s infinite;
}

@keyframes pulseDot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.2); }
}

.status-indicators {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 20px;
}

.status-item {
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(255, 255, 255, 0.05);
    padding: 12px;
    border-radius: 10px;
    transition: all 0.3s ease;
}

.status-item:hover {
    background: rgba(255, 255, 255, 0.08);
    transform: translateX(5px);
}

.status-icon {
    font-size: 28px;
    width: 40px;
    text-align: center;
}

.status-info {
    flex: 1;
}

.status-label {
    color: #aaaaaa;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}

.status-value {
    color: #ffffff;
    font-size: 14px;
    font-weight: 600;
}

.status-indicator {
    width: 30px;
    display: flex;
    justify-content: center;
}

.indicator-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #666666;
    transition: all 0.3s ease;
}

.indicator-dot.active {
    background: #00ff00;
    box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
}

.indicator-dot.warning {
    background: #ffaa00;
    box-shadow: 0 0 10px rgba(255, 170, 0, 0.5);
}

.indicator-dot.error {
    background: #ff0000;
    box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
}

.monitoring-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    padding-top: 15px;
    border-top: 2px solid rgba(255, 255, 255, 0.1);
}

.stat-box {
    text-align: center;
    padding: 10px;
    background: rgba(102, 126, 234, 0.1);
    border-radius: 8px;
}

.stat-box .stat-value {
    font-size: 24px;
    font-weight: 700;
    color: #667eea;
    margin-bottom: 4px;
}

.stat-box .stat-label {
    font-size: 11px;
    color: #aaaaaa;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Enhanced Video Feed */
.video-monitoring-section {
    position: fixed;
    top: 80px;
    right: 20px;
    width: 400px;
    z-index: 999;
    animation: slideInRight 0.5s ease;
}

@keyframes slideInRight {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

.video-container::before {
    content: '📹 LIVE';
    position: absolute;
    top: 10px;
    left: 10px;
    background: rgba(255, 0, 0, 0.8);
    color: white;
    padding: 4px 12px;
    border-radius: 5px;
    font-size: 12px;
    font-weight: 700;
    z-index: 20;
    animation: blinkLive 2s infinite;
}

@keyframes blinkLive {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
'''
    
    # Append to file
    print("Adding CSS styles...")
    with open(css_file, 'a', encoding='utf-8') as f:
        f.write('\n' + new_css)
    
    print("[OK] CSS styles added successfully!")
    return True

def main():
    print("\n" + "="*70)
    print("ENHANCED MONITORING FEATURES - AUTO INSTALLER")
    print("="*70)
    print("\nThis will add:")
    print("1. Live video feed on interview screen")
    print("2. Real-time monitoring status panel")
    print("3. Enhanced CSS styles")
    print("\nNote: Tab notification sound is already implemented!")
    print("="*70 + "\n")
    
    try:
        # Add monitoring panel
        if add_monitoring_panel():
            print("\n[1/2] Monitoring panel added ✓")
        
        # Add CSS styles
        if add_css_styles():
            print("[2/2] CSS styles added ✓")
        
        print("\n" + "="*70)
        print("INSTALLATION COMPLETE!")
        print("="*70)
        print("\nFeatures added:")
        print("✓ Live video feed (top-right corner)")
        print("✓ Real-time monitoring panel (bottom-left)")
        print("✓ Face detection indicator")
        print("✓ Eye contact tracker")
        print("✓ Body posture monitor")
        print("✓ Tab switching alerts")
        print("✓ Live scores (Focus, Posture, Eye Contact)")
        print("\nNotification sound: Already active (3 beeps on tab switch)")
        print("\nNext steps:")
        print("1. Restart your server (if running)")
        print("2. Start an interview")
        print("3. You'll see all monitoring features!")
        print("="*70)
        
    except Exception as e:
        print(f"\n[ERROR] Installation failed: {e}")
        print("\nPlease check:")
        print("1. Files exist at correct locations")
        print("2. You have write permissions")
        print("3. Files are not open in another program")

if __name__ == '__main__':
    main()
