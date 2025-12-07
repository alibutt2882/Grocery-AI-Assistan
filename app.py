import streamlit as st
from streamlit_option_menu import option_menu
import cv2
import pytesseract
from PIL import Image, ImageDraw
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import random
import qrcode
from io import BytesIO
import re
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Grocery AI Assistant",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86C1;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 1rem;
    }
    .alert-expired {
        background-color: #FADBD8;
        padding: 1rem;
        border-left: 5px solid #E74C3C;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .alert-warning {
        background-color: #FCF3CF;
        padding: 1rem;
        border-left: 5px solid #F1C40F;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .alert-success {
        background-color: #D5F4E6;
        padding: 1rem;
        border-left: 5px solid #58D68D;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .product-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: white;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(45deg, #2196F3, #21CBF3);
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 10px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'shopping_cart' not in st.session_state:
    st.session_state.shopping_cart = []
if 'scanned_items' not in st.session_state:
    st.session_state.scanned_items = []
if 'total_savings' not in st.session_state:
    st.session_state.total_savings = 0

# Mock databases (in real app, these would be actual databases)
HALAL_DATABASE = {
    "8801234567890": {"name": "Al Safa Chicken Sausages", "halal": True, "certificate": "JAKIM"},
    "8801234567891": {"name": "Nestlé Maggi Noodles", "halal": True, "certificate": "MFM"},
    "8801234567892": {"name": "Coca-Cola", "halal": True, "certificate": "FDA"},
    "8801234567893": {"name": "Haribo Gummy Bears", "halal": False, "certificate": None},
    "8801234567894": {"name": "Farm Fresh Milk", "halal": True, "certificate": "JAKIM"},
}

PRICE_DATABASE = {
    "8801234567890": {"store_price": 25.90, "market_avg": 24.50, "recommended_price": 23.99},
    "8801234567891": {"store_price": 4.50, "market_avg": 4.20, "recommended_price": 4.00},
    "8801234567892": {"store_price": 3.20, "market_avg": 3.00, "recommended_price": 2.80},
    "8801234567893": {"store_price": 8.90, "market_avg": 8.50, "recommended_price": 8.00},
    "8801234567894": {"store_price": 12.50, "market_avg": 11.90, "recommended_price": 11.50},
}

# Utility functions
def extract_date_from_text(text):
    """Extract and parse dates from OCR text"""
    date_patterns = [
        r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b',
        r'\b(\d{4})[/-](\d{1,2})[/-](\d{1,2})\b',
        r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b',
        r'\b(BEST BEFORE|EXP|EXPIRY|USE BY)[:\s]*([^\n]+)'
    ]
    
    for pattern in date_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            return matches[0] if isinstance(matches[0], str) else " ".join(matches[0])
    return None

def calculate_freshness_score(image):
    """Mock freshness detection - in real app, use ML model"""
    # Convert to numpy array
    img_array = np.array(image)
    
    # Simple mock: check brightness and contrast
    if len(img_array.shape) == 3:
        brightness = np.mean(img_array)
        contrast = np.std(img_array)
        
        # Mock scoring
        if brightness > 150 and contrast > 50:
            return 85, "Fresh"
        elif brightness > 100 and contrast > 30:
            return 65, "Average"
        else:
            return 30, "Not Fresh"
    return 50, "Average"

def check_halal_status(product_code):
    """Check halal status from database"""
    return HALAL_DATABASE.get(product_code, {"name": "Unknown", "halal": None, "certificate": None})

def check_price(product_code):
    """Check price comparison"""
    return PRICE_DATABASE.get(product_code, {"store_price": 0, "market_avg": 0, "recommended_price": 0})

def generate_qr_code(data):
    """Generate QR code image"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# Sidebar navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3082/3082383.png", width=100)
    st.title("🛒 Grocery AI")
    
    selected = option_menu(
        menu_title="Main Menu",
        options=["Dashboard", "Product Scanner", "Freshness Check", "Bill Checker", "Shopping Cart", "Settings"],
        icons=["house", "camera", "apple", "receipt", "cart", "gear"],
        menu_icon="cast",
        default_index=0,
    )

# Dashboard Page
if selected == "Dashboard":
    st.markdown('<h1 class="main-header">🛍️ Grocery AI Assistant Dashboard</h1>', unsafe_allow_html=True)
    
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Items Scanned", len(st.session_state.scanned_items), "12 items")
    with col2:
        st.metric("Total Savings", f"${st.session_state.total_savings:.2f}", "+$5.40")
    with col3:
        st.metric("Expiry Alerts", "3", "2 critical")
    with col4:
        st.metric("Halal Verified", "89%", "+2%")
    
    # Recent scans
    st.subheader("📋 Recent Scans")
    if st.session_state.scanned_items:
        df = pd.DataFrame(st.session_state.scanned_items[-5:])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No items scanned yet. Use the Product Scanner to get started!")
    
    # Savings chart
    st.subheader("💰 Savings Overview")
    fig = go.Figure(data=[
        go.Bar(name='Store Price', x=['Item 1', 'Item 2', 'Item 3'], y=[25, 18, 32]),
        go.Bar(name='Market Average', x=['Item 1', 'Item 2', 'Item 3'], y=[23, 16, 30])
    ])
    fig.update_layout(barmode='group', height=300)
    st.plotly_chart(fig, use_container_width=True)

# Product Scanner Page
elif selected == "Product Scanner":
    st.markdown('<h1 class="main-header">📱 Smart Product Scanner</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📸 Camera Scan", "📁 Upload Image", "🔢 Manual Barcode", "⚙️ Scan Settings"])
    
    with tab1:
        st.subheader("Scan Product with Camera")
        camera_input = st.camera_input("Take a picture of the product barcode/label")
        
        if camera_input:
            image = Image.open(camera_input)
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(image, caption="Scanned Product", use_container_width=True)
                
                # Mock QR/Barcode detection
                product_code = "880123456789" + str(random.randint(0, 9))
                st.info(f"Detected Barcode: `{product_code}`")
            
            with col2:
                # Product Information
                st.subheader("📦 Product Analysis")
                
                # Expiry Check
                st.markdown("### ⚠️ Expiry Check")
                expiry_date = datetime.now() + timedelta(days=random.randint(-5, 30))
                days_left = (expiry_date - datetime.now()).days
                
                if days_left < 0:
                    st.markdown('<div class="alert-expired"><strong>❌ EXPIRED!</strong><br>'
                               f'Expired {abs(days_left)} days ago</div>', unsafe_allow_html=True)
                elif days_left <= 3:
                    st.markdown(f'<div class="alert-warning"><strong>⚠️ EXPIRING SOON!</strong><br>'
                               f'Expires in {days_left} days ({expiry_date.strftime("%d %b %Y")})</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="alert-success"><strong>✅ OKAY</strong><br>'
                               f'Expires: {expiry_date.strftime("%d %b %Y")} ({days_left} days left)</div>', unsafe_allow_html=True)
                
                # Halal Check
                st.markdown("### 🕌 Halal Status")
                halal_info = check_halal_status(product_code)
                if halal_info["halal"]:
                    st.success(f"✅ **Halal Certified**\nCertificate: {halal_info['certificate']}")
                elif halal_info["halal"] is False:
                    st.error("❌ **Not Halal Certified**\nContains non-halal ingredients")
                else:
                    st.warning("⚠️ **Status Unknown**\nNot in database")
                
                # Price Check
                st.markdown("### 💰 Price Comparison")
                price_info = check_price(product_code)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Store Price", f"${price_info['store_price']:.2f}")
                with col_b:
                    st.metric("Market Avg", f"${price_info['market_avg']:.2f}")
                
                if price_info['store_price'] > price_info['market_avg']:
                    diff = ((price_info['store_price'] - price_info['market_avg']) / price_info['market_avg']) * 100
                    st.warning(f"⏫ **{diff:.1f}% above market average**")
                else:
                    diff = ((price_info['market_avg'] - price_info['store_price']) / price_info['market_avg']) * 100
                    st.success(f"⏬ **{diff:.1f}% below market average**")
                
                # Add to cart
                if st.button("🛒 Add to Shopping Cart"):
                    item = {
                        "name": halal_info["name"],
                        "price": price_info["store_price"],
                        "expiry": expiry_date.strftime("%Y-%m-%d"),
                        "halal": halal_info["halal"],
                        "barcode": product_code
                    }
                    st.session_state.shopping_cart.append(item)
                    st.session_state.scanned_items.append(item)
                    st.session_state.total_savings += (price_info['market_avg'] - price_info['store_price'])
                    st.success("Added to cart!")
    
    with tab2:
        st.subheader("Upload Product Image")
        uploaded_file = st.file_uploader("Choose an image file", type=['jpg', 'jpeg', 'png'])
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Product", use_container_width=True)
            
            # OCR Text Extraction
            st.subheader("📝 Extracted Text (OCR)")
            # In real app: text = pytesseract.image_to_string(image)
            sample_text = """NESTLÉ MAGGI 2-MINUTE NOODLES
            BEST BEFORE: 15/06/2024
            Ingredients: Wheat flour, palm oil, salt, ...
            Net Weight: 280g
            Product of Malaysia"""
            
            st.code(sample_text)
            
            # Date extraction
            extracted_date = extract_date_from_text(sample_text)
            if extracted_date:
                st.success(f"✅ Found expiry date: {extracted_date}")
            else:
                st.warning("⚠️ No expiry date found in image")
    
    with tab3:
        st.subheader("Manual Barcode Entry")
        barcode = st.text_input("Enter 13-digit barcode:", placeholder="8801234567890")
        
        if barcode and len(barcode) == 13:
            st.success(f"✅ Valid barcode entered: {barcode}")
            
            # Generate QR code
            qr_img = generate_qr_code(barcode)
            st.image(qr_img, caption="Generated QR Code", width=200)
            
            # Product lookup
            product_name = st.text_input("Product Name:", "Al Safa Chicken Sausages")
            expiry_date = st.date_input("Expiry Date:", datetime.now() + timedelta(days=30))
            
            if st.button("Check Product Details"):
                st.info(f"Checking details for {product_name}...")
    
    with tab4:
        st.subheader("Scanner Settings")
        st.slider("Scan Quality", 1, 10, 7)
        st.checkbox("Enable Auto-focus", True)
        st.checkbox("Beep on successful scan", True)
        st.checkbox("Auto-detect expiry dates", True)
        st.checkbox("Show price alerts", True)
        st.checkbox("Verify halal status automatically", True)

# Freshness Check Page
elif selected == "Freshness Check":
    st.markdown('<h1 class="main-header">🥦 Freshness Checker</h1>', unsafe_allow_html=True)
    
    st.info("Take a picture of fruits, vegetables, or meat to check freshness using AI")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📸 Capture Image")
        camera_img = st.camera_input("Take picture of produce", key="freshness_cam")
        
        upload_img = st.file_uploader("Or upload image", type=['jpg', 'png', 'jpeg'])
        
        if camera_img or upload_img:
            image = Image.open(camera_img if camera_img else upload_img)
            st.image(image, caption="Product for Freshness Check", use_container_width=True)
    
    with col2:
        st.subheader("🔍 Freshness Analysis")
        
        if camera_img or upload_img:
            image = Image.open(camera_img if camera_img else upload_img)
            
            # Mock analysis with progress bar
            progress_bar = st.progress(0)
            for i in range(100):
                # Simulate processing
                progress_bar.progress(i + 1)
            
            # Freshness score
            score, status = calculate_freshness_score(image)
            
            # Display results
            st.metric("Freshness Score", f"{score}/100", delta=f"{score-50}" if score != 50 else None)
            
            # Color-coded indicator
            if score >= 80:
                st.markdown('<div class="alert-success"><h3>✅ EXCELLENT FRESHNESS</h3>'
                           'Perfect for consumption. Great color and texture.</div>', unsafe_allow_html=True)
            elif score >= 60:
                st.markdown('<div class="alert-warning"><h3>⚠️ AVERAGE FRESHNESS</h3>'
                           'Okay for consumption. Use within 2-3 days.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-expired"><h3>❌ POOR FRESHNESS</h3>'
                           'Consider discarding or using immediately.</div>', unsafe_allow_html=True)
            
            # Detailed metrics
            st.subheader("📊 Detailed Analysis")
            
            metrics = {
                "Color Vibrancy": random.randint(70, 95),
                "Texture Score": random.randint(60, 90),
                "Moisture Level": random.randint(65, 88),
                "Visual Defects": random.randint(0, 20)
            }
            
            for metric, value in metrics.items():
                st.progress(value/100, text=f"{metric}: {value}%")
            
            # Recommendations
            st.subheader("💡 Recommendations")
            if score >= 80:
                st.success("• Perfect for salads and raw consumption")
                st.success("• Can be stored for 5-7 days")
            elif score >= 60:
                st.warning("• Best for cooking within 2-3 days")
                st.warning("• Store in refrigerator")
            else:
                st.error("• Use immediately in cooked dishes")
                st.error("• Do not store for more than 1 day")
    
    # Freshness guide
    with st.expander("📚 Freshness Guide & Tips"):
        st.markdown("""
        ### How to Identify Fresh Produce:
        
        **Fruits & Vegetables:**
        - 🍎 **Firmness**: Should be firm, not mushy
        - 🎨 **Color**: Bright, uniform color without dark spots
        - 🌱 **Stems**: Green and flexible, not dry
        - 👃 **Smell**: Fresh, natural aroma
        
        **Meat & Poultry:**
        - 🎨 **Color**: Bright red for beef, pink for poultry
        - 👃 **Smell**: No sour or ammonia odor
        - ✋ **Texture**: Firm to touch, springs back
        - 💧 **Moisture**: Minimal liquid in packaging
        """)

# Bill Checker Page
elif selected == "Bill Checker":
    st.markdown('<h1 class="main-header">🧾 Smart Bill Checker</h1>', unsafe_allow_html=True)
    
    st.info("Upload your receipt to check for errors, verify prices, and track savings")
    
    tab1, tab2 = st.tabs(["📄 Upload Receipt", "📊 Bill Analysis"])
    
    with tab1:
        st.subheader("Upload Receipt Image")
        
        uploaded_receipt = st.file_uploader("Upload receipt photo", type=['jpg', 'png', 'jpeg'])
        
        if uploaded_receipt:
            receipt_img = Image.open(uploaded_receipt)
            st.image(receipt_img, caption="Uploaded Receipt", use_container_width=True)
            
            # Mock OCR results
            if st.button("🔍 Analyze Receipt"):
                st.success("✅ Receipt processed successfully!")
                
                # Mock extracted data
                mock_receipt_data = {
                    "Store": "Fresh Mart Supermarket",
                    "Date": datetime.now().strftime("%Y-%m-%d"),
                    "Time": "14:30",
                    "Items": [
                        {"name": "Chicken Sausages", "price": 25.90, "qty": 1},
                        {"name": "Maggi Noodles", "price": 4.50, "qty": 3},
                        {"name": "Fresh Milk", "price": 12.50, "qty": 1},
                        {"name": "Coca-Cola", "price": 3.20, "qty": 2},
                        {"name": "Apples", "price": 8.75, "qty": 1},
                    ],
                    "Subtotal": 67.85,
                    "Tax": 4.07,
                    "Total": 71.92
                }
                
                st.session_state.receipt_data = mock_receipt_data
                st.rerun()
    
    with tab2:
        if 'receipt_data' in st.session_state:
            data = st.session_state.receipt_data
            
            # Receipt Summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Items", len(data["Items"]))
            with col2:
                st.metric("Bill Total", f"${data['Total']:.2f}")
            with col3:
                st.metric("Potential Savings", "$5.40", "-7.5%")
            
            # Items table
            st.subheader("🛒 Purchased Items")
            items_df = pd.DataFrame(data["Items"])
            st.dataframe(items_df, use_container_width=True)
            
            # Price comparison chart
            st.subheader("📈 Price Comparison")
            
            # Mock market prices
            market_prices = [23.99, 4.00, 11.50, 2.80, 8.20]
            item_names = [item["name"] for item in data["Items"]]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Paid Price', x=item_names, 
                                y=[item["price"] for item in data["Items"]]))
            fig.add_trace(go.Bar(name='Market Price', x=item_names, y=market_prices))
            
            fig.update_layout(
                title="Price Comparison vs Market Average",
                barmode='group',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Error detection
            st.subheader("⚠️ Error Detection")
            
            errors_found = random.randint(0, 2)
            if errors_found > 0:
                st.warning(f"Found {errors_found} potential error(s) in receipt:")
                st.error("• **Double charge detected**: Apples charged twice")
                st.error("• **Tax miscalculation**: Tax should be $3.89, not $4.07")
            else:
                st.success("✅ No errors detected in receipt")
            
            # Savings summary
            st.subheader("💰 Savings Summary")
            savings_data = {
                "Price Savings": 5.40,
                "Expired Items Avoided": 0.00,
                "Halal Verified Items": 4,
                "Total Value": 67.85
            }
            
            for item, value in savings_data.items():
                if isinstance(value, float):
                    st.metric(item, f"${value:.2f}")
                else:
                    st.metric(item, value)

# Shopping Cart Page
elif selected == "Shopping Cart":
    st.markdown('<h1 class="main-header">🛒 Smart Shopping Cart</h1>', unsafe_allow_html=True)
    
    if not st.session_state.shopping_cart:
        st.info("Your cart is empty. Scan some products to get started!")
    else:
        # Cart summary
        total_items = len(st.session_state.shopping_cart)
        total_price = sum(item["price"] for item in st.session_state.shopping_cart)
        halal_items = sum(1 for item in st.session_state.shopping_cart if item["halal"])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Items", total_items)
        with col2:
            st.metric("Total Price", f"${total_price:.2f}")
        with col3:
            st.metric("Halal Items", halal_items)
        with col4:
            st.metric("Total Savings", f"${st.session_state.total_savings:.2f}")
        
        # Cart items
        st.subheader("📋 Cart Items")
        
        for idx, item in enumerate(st.session_state.shopping_cart):
            with st.container():
                col_a, col_b, col_c, col_d = st.columns([3, 2, 1, 1])
                
                with col_a:
                    st.write(f"**{item['name']}**")
                    st.write(f"Barcode: `{item['barcode']}`")
                
                with col_b:
                    st.write(f"Price: ${item['price']:.2f}")
                    st.write(f"Expiry: {item['expiry']}")
                
                with col_c:
                    if item["halal"]:
                        st.success("✅ Halal")
                    else:
                        st.error("❌ Non-Halal")
                
                with col_d:
                    if st.button("❌", key=f"remove_{idx}"):
                        st.session_state.shopping_cart.pop(idx)
                        st.rerun()
                
                st.divider()
        
        # Checkout
        st.subheader("💳 Checkout")
        
        col_x, col_y = st.columns(2)
        with col_x:
            if st.button("✅ Proceed to Checkout", type="primary"):
                st.success("Order placed successfully! 🎉")
                st.balloons()
                st.session_state.shopping_cart = []
                st.session_state.total_savings = 0
                st.rerun()
        
        with col_y:
            if st.button("🗑️ Clear Cart"):
                st.session_state.shopping_cart = []
                st.rerun()
        
        # Export options
        st.subheader("📤 Export Cart")
        col_export1, col_export2, col_export3 = st.columns(3)
        
        with col_export1:
            if st.button("📄 Generate PDF Receipt"):
                st.info("PDF receipt generated! (Mock)")
        
        with col_export2:
            if st.button("📱 Share Cart"):
                st.info("Cart shared! (Mock)")
        
        with col_export3:
            if st.button("💾 Save for Later"):
                st.info("Cart saved! (Mock)")

# Settings Page
elif selected == "Settings":
    st.markdown('<h1 class="main-header">⚙️ Settings</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["General", "Alerts", "Preferences", "About"])
    
    with tab1:
        st.subheader("General Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("Language", ["English", "Bahasa Malaysia", "中文", "हिन्दी"])
            st.selectbox("Currency", ["MYR (RM)", "USD ($)", "EUR (€)", "GBP (£)"])
            st.selectbox("Temperature Unit", ["Celsius", "Fahrenheit"])
        
        with col2:
            st.slider("Scan Sensitivity", 1, 10, 7)
            st.slider("Image Quality", 1, 10, 8)
            st.checkbox("Auto-save scans", True)
        
        if st.button("Save General Settings"):
            st.success("Settings saved successfully!")
    
    with tab2:
        st.subheader("Alert Preferences")
        
        st.checkbox("Expiry alerts", True)
        st.checkbox("Near-expiry alerts (3-7 days)", True)
        st.checkbox("Price drop alerts", True)
        st.checkbox("Halal status alerts", True)
        
        st.number_input("Expiry warning days", min_value=1, max_value=30, value=7)
        st.number_input("Price threshold (%)", min_value=1, max_value=50, value=10)
        
        st.selectbox("Notification Method", ["Push Notification", "Email", "Both"])
        
        if st.button("Save Alert Settings"):
            st.success("Alert settings saved!")
    
    with tab3:
        st.subheader("Shopping Preferences")
        
        dietary_pref = st.multiselect(
            "Dietary Preferences",
            ["Halal", "Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Nut-Free"]
        )
        
        budget_limit = st.number_input("Monthly Budget Limit (MYR)", min_value=100, max_value=5000, value=2000)
        
        favorite_stores = st.multiselect(
            "Favorite Stores",
            ["Tesco", "Giant", "AEON", "Mydin", "Lotus's", "Village Grocer"]
        )
        
        if st.button("Save Preferences"):
            st.success("Preferences saved!")
    
    with tab4:
        st.subheader("About Grocery AI Assistant")
        
        st.markdown("""
        ### 🛒 Grocery AI Assistant v1.0
        
        **Description:**
        An intelligent grocery shopping assistant that helps you make better purchasing decisions using AI.
        
        **Features:**
        - ✅ Expired item detection
        - 🥦 Freshness checking
        - 🕌 Halal status verification
        - 💰 Price comparison
        - 🧾 Bill error checking
        
        **Technologies Used:**
        - Computer Vision (OpenCV)
        - OCR (Tesseract)
        - Machine Learning (TensorFlow)
        - Streamlit for web interface
        
        **Data Sources:**
        - JAKIM Halal Database
        - GS1 Product Database
        - Market price aggregators
        
        **Disclaimer:**
        This app provides AI-assisted recommendations. Always use your own judgment when making purchasing decisions.
        """)
        
        st.info("📧 Contact: support@grocery-ai.com")
        st.info("🌐 Website: https://grocery-ai.demo")
        
        if st.button("Check for Updates"):
            st.success("You have the latest version! ✅")

# Footer
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)
with footer_col1:
    st.caption("🛒 Grocery AI Assistant v1.0")
with footer_col2:
    st.caption("🤖 Powered by AI & Computer Vision")
with footer_col3:
    st.caption("© 2024 All rights reserved")