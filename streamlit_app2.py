import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import os
import requests
from PIL import Image
from io import BytesIO
from geopy.distance import geodesic
import folium
from streamlit_folium import folium_static

# ------------------ CẤU HÌNH ------------------
st.set_page_config(
    page_title="Hệ thống LIS - Shop Giày Dép",
    layout="wide",
    page_icon="👟"
)
st.title("👟 HỆ THỐNG LIS - SHOP GIÀY DÉP ĐA KÊNH")

# ------------------ DỮ LIỆU ------------------
# Đường dẫn file
kho_path = "data/kho.csv"
don_path = "data/don_hang.csv"
os.makedirs("data", exist_ok=True)

# Hình ảnh sản phẩm (URL từ internet)
product_images = {
    "Giày thể thao Nike Air Max": "https://static.nike.com/a/images/t_PDP_1280_v1/f_auto,q_auto:eco/skwgyqrbfy4ohnr4mrsl/air-max-270-mens-shoes-KkLcGR.png",
    "Giày da nam Clarks": "https://clarks.scene7.com/is/image/Pangaea2Build/26157262_W?fmt=jpeg&fit=constrain,1&wid=800",
    "Giày sandal nữ Adidas": "https://assets.adidas.com/images/w_600,f_auto,q_auto/89b8c7a6a9e54d7d8f22aaf20116ccfd_9366/Giay_Adilette_Aqua_W_Nau_IU3404_01_standard.jpg",
    "Giày búp bê nữ Zara": "https://static.zara.net/photos///2023/I/0/2/p/2251/020/040/2/w/750/2251020040_1_1_1.jpg",
    "Giày boot nam Timberland": "https://images.timberland.com/is/image/TimberlandEU/10062831-hero?wid=720&hei=720&fit=constrain,1",
    "Giày thể thao Puma RS-X": "https://images.puma.com/image/upload/f_auto,q_auto,b_rgb:f8f8f8,w_750,h_750/global/374915/01/sv01/fnd/EEA/fmt/png",
    "Giày lười nữ Charles & Keith": "https://img.cdn.vncdn.io/cdn-pos/1f2180-6629/ps/20230601_jHM3XvBKWN.jpg",
    "Giày thể thao New Balance 574": "https://nb.scene7.com/is/image/NB/m5740gy2_nb_02_i?$pdpflexf2$&qlt=80&fmt=webp&wid=800&hei=800",
    "Giày cao gót nữ Nine West": "https://m.media-amazon.com/images/I/71U+Kix4zPL._AC_UX575_.jpg",
    "Giày thể thao Converse Chuck Taylor": "https://www.converse.com/dw/image/v2/BCZC_PRD/on/demandware.static/-/Sites-cnv-master-catalog/default/dw3a93bfee/images/a_107/162050C_A_107X1.jpg"
}

# Tạo dữ liệu kho nếu chưa tồn tại
if os.path.exists(kho_path):
    df_kho = pd.read_csv(kho_path)
else:
    data = {
        "ten_sp": list(product_images.keys()),
        "so_luong": [50, 30, 20, 25, 15, 40, 35, 60, 10, 45],
        "gia": [2500000, 1800000, 1200000, 1500000, 3000000, 2200000, 1700000, 2000000, 1600000, 1900000],
        "mo_ta": [
            "Giày thể thao đế khí Nike Air Max",
            "Giày da nam cao cấp Clarks",
            "Sandal nữ thoáng mát Adidas",
            "Giày búp bê nữ thời trang Zara",
            "Giày boot nam chống nước Timberland",
            "Giày thể thao Puma RS-X phong cách",
            "Giày lười nữ thời trang Charles & Keith",
            "Giày thể thao New Balance 574",
            "Giày cao gót nữ Nine West",
            "Giày thể thao Converse Chuck Taylor"
        ]
    }
    df_kho = pd.DataFrame(data)
    df_kho.to_csv(kho_path, index=False)

if os.path.exists(don_path):
    df_don = pd.read_csv(don_path)
else:
    df_don = pd.DataFrame(columns=[
        "ten_khach", "san_pham", "kenh", "trang_thai", "ngay_tao",
        "gia_tri", "khu_vuc", "don_vi_vc", "eta_ngay"
    ])

# ------------------ HÀM TIỆN ÍCH ------------------
def tinh_khoang_cach(dia_chi_kho, dia_chi_khach):
    kho_toa_do = {
        "Kho HCM": (10.8231, 106.6297),
        "Kho Hà Nội": (21.0278, 105.8342),
        "Kho Đà Nẵng": (16.0544, 108.2022)
    }
    
    khach_toa_do = {
        "HCM": (10.7758, 106.7019),
        "Hà Nội": (21.0285, 105.8542),
        "Đà Nẵng": (16.0680, 108.2127),
        "Khác": (10.9639, 106.8567)
    }
    
    try:
        kho = kho_toa_do[dia_chi_kho]
        khach = khach_toa_do[dia_chi_khach]
        return geodesic(kho, khach).km
    except:
        return None

def tao_ban_do(dia_chi_kho, dia_chi_khach):
    kho_toa_do = {
        "Kho HCM": (10.8231, 106.6297),
        "Kho Hà Nội": (21.0278, 105.8342),
        "Kho Đà Nẵng": (16.0544, 108.2022)
    }
    
    khach_toa_do = {
        "HCM": (10.7758, 106.7019),
        "Hà Nội": (21.0285, 105.8542),
        "Đà Nẵng": (16.0680, 108.2127),
        "Khác": (10.9639, 106.8567)
    }
    
    try:
        kho = kho_toa_do[dia_chi_kho]
        khach = khach_toa_do[dia_chi_khach]
        
        m = folium.Map(location=[(kho[0]+khach[0])/2, (kho[1]+khach[1])/2], zoom_start=10)
        
        folium.Marker(
            location=kho,
            popup=dia_chi_kho,
            icon=folium.Icon(color="green", icon="warehouse")
        ).add_to(m)
        
        folium.Marker(
            location=khach,
            popup=f"Khách hàng: {dia_chi_khach}",
            icon=folium.Icon(color="red", icon="user")
        ).add_to(m)
        
        folium.PolyLine(
            locations=[kho, khach],
            color="blue",
            weight=2.5,
            opacity=1
        ).add_to(m)
        
        return m
    except:
        return None

# ------------------ GIỎ HÀNG ------------------
if 'cart' not in st.session_state:
    st.session_state.cart = []

# ------------------ GIAO DIỆN KHÁCH HÀNG ------------------
menu = st.sidebar.radio("🔍 Bạn là:", ["🛍️ Khách hàng", "👨‍💼 Doanh nghiệp"])

if menu == "🛍️ Khách hàng":
    st.header("🛍️ CỬA HÀNG GIÀY DÉP")
    
    # Hiển thị sản phẩm
    st.subheader("👟 Sản phẩm nổi bật")
    cols = st.columns(4)
    
    for idx, product in enumerate(product_images.keys()):
        with cols[idx % 4]:
            st.image(product_images[product], width=200)
            product_info = df_kho[df_kho["ten_sp"] == product].iloc[0]
            st.markdown(f"**{product}**")
            st.markdown(f"💰 Giá: {product_info['gia']:,.0f} đ")
            st.markdown(f"📦 Tồn kho: {product_info['so_luong']}")
            
            # Thêm vào giỏ hàng
            quantity = st.number_input("Số lượng", 1, product_info['so_luong'], key=f"qty_{idx}")
            if st.button(f"🛒 Thêm vào giỏ #{idx+1}"):
                st.session_state.cart.append({
                    "san_pham": product,
                    "so_luong": quantity,
                    "don_gia": product_info['gia'],
                    "tong_tien": product_info['gia'] * quantity,
                    "anh": product_images[product]
                })
                st.success(f"✅ Đã thêm {product} vào giỏ hàng!")
                st.rerun()
    
    # Giỏ hàng trong sidebar
    st.sidebar.subheader("🛒 Giỏ hàng của bạn")
    if st.session_state.cart:
        total_price = 0
        for i, item in enumerate(st.session_state.cart):
            with st.sidebar.expander(f"{item['san_pham']}"):
                st.image(item['anh'], width=100)
                st.markdown(f"**Giá:** {item['don_gia']:,.0f} đ")
                st.markdown(f"**Số lượng:** {item['so_luong']}")
                st.markdown(f"**Thành tiền:** {item['tong_tien']:,.0f} đ")
                
                # Nút xóa sản phẩm
                if st.button("❌ Xóa", key=f"del_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()
            
            total_price += item['tong_tien']
        
        st.sidebar.markdown(f"**Tổng cộng:** {total_price:,.0f} đ")
        
        # Form thanh toán
        with st.sidebar.form("checkout_form"):
            st.subheader("Thông tin thanh toán")
            customer_name = st.text_input("Họ tên")
            customer_phone = st.text_input("Số điện thoại")
            khu_vuc = st.selectbox("Khu vực", ["HCM", "Hà Nội", "Đà Nẵng", "Khác"])
            
            if st.form_submit_button("💳 Đặt hàng"):
                if customer_name and customer_phone:
                    # Thêm đơn hàng
                    new_order = {
                        "ten_khach": customer_name,
                        "san_pham": ", ".join([item['san_pham'] for item in st.session_state.cart]),
                        "kenh": "Website",
                        "trang_thai": "Chờ xử lý",
                        "ngay_tao": datetime.date.today(),
                        "gia_tri": total_price,
                        "khu_vuc": khu_vuc,
                        "don_vi_vc": "GHTK" if khu_vuc == "HCM" else "GHN" if khu_vuc == "Hà Nội" else "VNPost",
                        "eta_ngay": 1 if khu_vuc == "HCM" else 2 if khu_vuc == "Hà Nội" else 3
                    }
                    
                    df_don = pd.concat([df_don, pd.DataFrame([new_order])], ignore_index=True)
                    df_don.to_csv(don_path, index=False)
                    
                    # Cập nhật tồn kho
                    for item in st.session_state.cart:
                        mask = df_kho["ten_sp"] == item['san_pham']
                        if mask.any():
                            df_kho.loc[mask, "so_luong"] -= item['so_luong']
                    
                    df_kho.to_csv(kho_path, index=False)
                    st.session_state.cart = []
                    st.sidebar.success("✅ Đơn hàng đã được đặt thành công!")
                    st.rerun()
                else:
                    st.sidebar.error("Vui lòng nhập đầy đủ thông tin")
        
        if st.sidebar.button("🗑️ Xóa toàn bộ giỏ hàng"):
            st.session_state.cart = []
            st.rerun()
    else:
        st.sidebar.warning("Giỏ hàng trống!")

# ------------------ QUẢN LÝ DOANH NGHIỆP ------------------
else:
    st.header("👨‍💼 Quản lý doanh nghiệp")
    tabs = st.tabs(["📋 Đơn hàng", "📦 Kho hàng", "📊 Thống kê", "🗺️ Theo dõi vận chuyển"])
    
    with tabs[0]:
        st.subheader("Quản lý đơn hàng")
        st.dataframe(df_don, use_container_width=True)
        
        # Cập nhật trạng thái đơn hàng
        TRANG_THAI_DON_HANG = ["Chờ xử lý", "Đang giao", "Đã giao", "Đã hủy"]
        if not df_don.empty:
            with st.expander("Cập nhật trạng thái đơn hàng"):
                order_id = st.selectbox("Chọn đơn hàng", df_don.index, key="order_select")
                new_status = st.selectbox("Trạng thái mới", TRANG_THAI_DON_HANG, key="status_select")
                
                if st.button("Cập nhật"):
                    df_don.at[order_id, "trang_thai"] = new_status
                    df_don.to_csv(don_path, index=False)
                    st.success("Đã cập nhật trạng thái!")
    
    with tabs[1]:
        st.subheader("Quản lý kho hàng")
        st.dataframe(df_kho, use_container_width=True)
        
        # Thêm sản phẩm mới
        with st.expander("Thêm sản phẩm mới"):
            with st.form("add_product"):
                new_name = st.text_input("Tên sản phẩm")
                new_desc = st.text_area("Mô tả")
                new_qty = st.number_input("Số lượng", 0, step=1)
                new_price = st.number_input("Giá", 0, step=10000)
                new_image = st.text_input("URL hình ảnh")
                
                if st.form_submit_button("Thêm"):
                    if new_name and new_qty and new_price:
                        new_product = pd.DataFrame([[new_name, new_qty, new_price, new_desc]], 
                                                 columns=df_kho.columns)
                        df_kho = pd.concat([df_kho, new_product], ignore_index=True)
                        df_kho.to_csv(kho_path, index=False)
                        
                        if new_image:
                            product_images[new_name] = new_image
                        
                        st.success("Đã thêm sản phẩm mới!")
                        st.rerun()
    
    with tabs[2]:
        st.subheader("Thống kê doanh thu")
        if not df_don.empty:
            # Doanh thu theo kênh
            st.plotly_chart(px.pie(df_don, names="kenh", title="Tỉ lệ kênh bán"))
            
            # Doanh thu theo thời gian
            df_don["ngay_tao"] = pd.to_datetime(df_don["ngay_tao"])
            revenue_by_date = df_don.groupby(df_don["ngay_tao"].dt.date)["gia_tri"].sum().reset_index()
            st.line_chart(revenue_by_date.set_index("ngay_tao"))
        else:
            st.warning("Chưa có dữ liệu đơn hàng")
    
    with tabs[3]:
        st.subheader("Theo dõi vận chuyển")
        if not df_don.empty:
            order_to_track = st.selectbox("Chọn đơn hàng", df_don.index, key="track_order_select")
            order = df_don.loc[order_to_track]
            
            st.info(f"""
            **Thông tin đơn hàng:**
            - Khách hàng: {order['ten_khach']}
            - Sản phẩm: {order['san_pham']}
            - Trạng thái: {order['trang_thai']}
            - Đơn vị vận chuyển: {order['don_vi_vc']}
            - Thời gian giao ước tính: {order['eta_ngay']} ngày
            """)
            
            # Hiển thị bản đồ
            map_obj = tao_ban_do("Kho HCM", order['khu_vuc'])
            if map_obj:
                folium_static(map_obj, width=700, height=400)
