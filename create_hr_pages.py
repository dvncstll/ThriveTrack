#!/usr/bin/env python3
"""
Script to create basic HR page templates
"""

import os

# HR page configurations
hr_pages = [
    {
        'filename': 'hr-orders.html',
        'title': 'HR Orders',
        'page_title': 'Order Management',
        'subtitle': 'Manage employee orders and requests',
        'content': '''
        <h3>Order Management</h3>
        <p>This page would contain order management features such as:</p>
        <ul>
          <li>Employee request tracking</li>
          <li>Approval workflows</li>
          <li>Order history</li>
          <li>Budget management</li>
        </ul>
        '''
    },
    {
        'filename': 'hr-purchase.html',
        'title': 'HR Purchase',
        'page_title': 'Purchase Management',
        'subtitle': 'Manage company purchases and procurement',
        'content': '''
        <h3>Purchase Management</h3>
        <p>This page would contain purchase management features such as:</p>
        <ul>
          <li>Purchase requisitions</li>
          <li>Vendor management</li>
          <li>Budget tracking</li>
          <li>Approval processes</li>
        </ul>
        '''
    },
    {
        'filename': 'hr-reporting.html',
        'title': 'HR Reporting',
        'page_title': 'Reports & Analytics',
        'subtitle': 'Generate reports and view analytics',
        'content': '''
        <h3>Reports & Analytics</h3>
        <p>This page would contain reporting features such as:</p>
        <ul>
          <li>Employee performance reports</li>
          <li>Turnover analytics</li>
          <li>Budget reports</li>
          <li>Custom report builder</li>
        </ul>
        '''
    },
    {
        'filename': 'hr-support.html',
        'title': 'HR Support',
        'page_title': 'Support & Help',
        'subtitle': 'Get help and support for HR operations',
        'content': '''
        <h3>Support & Help</h3>
        <p>This page would contain support features such as:</p>
        <ul>
          <li>Knowledge base</li>
          <li>Ticket system</li>
          <li>Live chat support</li>
          <li>Training resources</li>
        </ul>
        '''
    },
    {
        'filename': 'hr-settings.html',
        'title': 'HR Settings',
        'page_title': 'System Settings',
        'subtitle': 'Configure HR system preferences',
        'content': '''
        <h3>System Settings</h3>
        <p>This page would contain configuration options such as:</p>
        <ul>
          <li>User permissions</li>
          <li>System preferences</li>
          <li>Integration settings</li>
          <li>Backup and restore</li>
        </ul>
        '''
    }
]

# HTML template
html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} - ThriveTrack</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #f4f7f8;
      --card: #ffffff;
      --text: #0f172a;
      --muted: #64748b;
      --line: #e5e7eb;
      --teal-50:#e6fbf7; --teal-200:#b7d7d2; --teal-600:#2c6d62;
      --green-50:#ecfdf5; --green-600:#059669;
      --cyan-50:#e6fafe; --cyan-600:#0891b2;
      --amber-50:#fff7ed; --amber-600:#d97706;
      --rose-50:#fef2f2; --rose-600:#dc2626;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ height: 100%; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans", "Apple Color Emoji", "Segoe UI Emoji";
    }}
    .shell {{
      max-width: 1400px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: 1fr;
    }}
    @media (min-width: 960px) {{
      .shell {{ grid-template-columns: 260px minmax(0,1fr); }}
    }}

    /* Sidebar */
    .sidebar {{
      display: none;
    }}
    @media (min-width: 960px) {{
      .sidebar {{
        display: flex;
        position: sticky; top: 0; height: 100vh;
        flex-direction: column; gap: 14px;
        background: var(--card);
        border-right: 1px solid var(--line);
        padding: 16px;
      }}
    }}
    .profile {{
      display: flex; gap: 12px; align-items: center;
      background: #f8fafc; border-radius: 16px; padding: 12px;
    }}
    .avatar {{ width: 40px; height: 40px; border-radius: 999px; background: linear-gradient(135deg,#14b8a6,#0f766e); }}
    .muted {{ color: var(--muted); }}
    .nav .nav-link {{
      width: 100%; text-align: left;
      padding: 10px 12px; border: 0; background: transparent; cursor: pointer;
      border-radius: 12px; color: #0f172a; font-size: 14px;
      text-decoration: none; display: block; transition: all 0.2s;
    }}
    .nav .nav-link:hover {{ background: #f8fafc; }}
    .nav .nav-link.active {{ background: #eef2f7; font-weight: 600; }}
    .logout {{
      margin-top: auto; width: 100%; border: 1px solid var(--line); background: #fff;
      padding: 10px 12px; border-radius: 12px; cursor: pointer;
    }}

    /* Main */
    main {{ padding: 16px; }}
    @media (min-width: 960px) {{ main {{ padding: 32px; }} }}
    
    .header {{
      text-align: center;
      margin-bottom: 32px;
    }}
    .welcome {{
      font-size: 28px;
      font-weight: 700;
      margin-bottom: 8px;
      color: var(--teal-600);
    }}
    .subtitle {{
      color: var(--muted);
      font-size: 16px;
    }}
    
    .card {{ 
      background: var(--card); 
      border: 1px solid var(--line); 
      border-radius: 16px; 
      padding: 24px; 
      box-shadow: 0 1px 2px rgba(0,0,0,.04); 
      max-width: 800px;
      margin: 0 auto;
    }}
    .card h3 {{ margin: 0 0 16px; font-size: 18px; font-weight: 600; }}
  </style>
</head>
<body>
  <div class="shell">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="profile">
        <div class="avatar"></div>
        <div>
          <div style="font-weight:600" id="userName">Nirmal Kumar P</div>
          <div class="muted" style="font-size:12px" id="userEmail">nirmalcom.job@gmail.com</div>
        </div>
      </div>

      <nav class="nav">
        <a href="/" class="nav-link">Dashboard</a>
        <a href="/hr-inventory" class="nav-link">Inventory</a>
        <a href="/hr-orders" class="nav-link">Orders</a>
        <a href="/hr-purchase" class="nav-link">Purchase</a>
        <a href="/hr-reporting" class="nav-link">Reporting</a>
        <a href="/hr-support" class="nav-link">Support</a>
        <a href="/hr-settings" class="nav-link">Settings</a>
      </nav>

      <button class="logout" id="logoutBtn">Logout</button>
    </aside>

    <!-- Main Content -->
    <main>
      <!-- Header -->
      <div class="header">
        <div class="welcome">{page_title}</div>
        <div class="subtitle">{subtitle}</div>
      </div>

      <!-- Content -->
      <div class="card">
        {content}
      </div>
    </main>
  </div>

  <script>
    // ===== AUTHENTICATION & SECURITY =====
    
    // Check if user is logged in and has HR role
    function checkAuth() {{
      const isLoggedIn = localStorage.getItem('isLoggedIn');
      const userRole = localStorage.getItem('userRole');
      const userEmail = localStorage.getItem('userEmail');
      
      if (!isLoggedIn || userRole !== 'hr') {{
        // Redirect to login if not authenticated or not HR
        window.location.href = '/login';
        return false;
      }}
      
      // Update user info in the UI
      if (userEmail) {{
        document.getElementById('userEmail').textContent = userEmail;
        // Extract name from email for demo purposes
        const name = userEmail.split('@')[0];
        document.getElementById('userName').textContent = name.charAt(0).toUpperCase() + name.slice(1);
      }}
      
      return true;
    }}
    
    // Logout functionality
    document.getElementById('logoutBtn').addEventListener('click', function() {{
      localStorage.removeItem('isLoggedIn');
      localStorage.removeItem('userRole');
      localStorage.removeItem('userEmail');
      window.location.href = '/redirect';
    }});
    
    // Check authentication on page load
    if (!checkAuth()) {{
      // Stop execution if not authenticated
      throw new Error('Authentication failed');
    }}
  </script>
</body>
</html>
'''

def create_hr_pages():
    """Create all HR page templates"""
    templates_dir = 'templates'
    
    # Ensure templates directory exists
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    for page in hr_pages:
        filename = os.path.join(templates_dir, page['filename'])
        
        # Update active nav link based on current page
        active_nav = page['filename'].replace('.html', '').replace('hr-', '')
        
        # Create the HTML content
        html_content = html_template.format(
            title=page['title'],
            page_title=page['page_title'],
            subtitle=page['subtitle'],
            content=page['content']
        )
        
        # Write the file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Created: {filename}")
    
    print("\nAll HR pages created successfully!")

if __name__ == "__main__":
    create_hr_pages()
