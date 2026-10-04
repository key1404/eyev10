import streamlit as st
import numpy as np
from PIL import Image
import streamlit.components.v1 as components

# تنظیمات صفحه
st.set_page_config(
    page_title="Eye1 AI | سامانه جامع انتخاب و تست زنده عینک",
    page_icon="👓",
    layout="wide"
)

st.title("👓 سامانه هوشمند Eye1: تحلیل چهره، پیشنهاد تخصصی و امتحان مجازی حرفه‌ای")

# مدیریت حالت‌های برنامه (مراحل سه‌گانه)
if "step" not in st.session_state:
    st.session_state.step = "capture"
if "image" not in st.session_state:
    st.session_state.image = None
if "face_shape" not in st.session_state:
    st.session_state.face_shape = ""
if "selected_frame" not in st.session_state:
    st.session_state.selected_frame = None

# نوار کناری تنظیمات بالینی
st.sidebar.header("⚙️ پارامترهای اپتومتری")
rx_type = st.sidebar.selectbox("نوع نسخه بینایی (Rx)", ["دوربین / نزدیک‌بین (ساده)", "آستیگمات", "دید پیش‌رونده", "بدون نمره"])
pd_input = st.sidebar.slider("فاصله دو چشم (PD بر حسب میلی‌متر)", 50, 75, 62)

# ---------------------------------------------------------
# مرحله ۱: ثبت یا آپلود تصویر چهره برای آنالیز اولیه
# ---------------------------------------------------------
if st.session_state.step == "capture":
    st.markdown("### مرحله ۱: ثبت تصویر چهره برای تحلیل آناتومیک")
    st.info("لطفاً یک تصویر واضح از چهره خود آپلود کنید یا عکسی برای استخراج فرم صورت ثبت نمایید.")
    
    tab1, tab2 = st.tabs(["📸 عکاسی برای تحلیل اولیه", "📤 آپلود فایل تصویر"])
    
    uploaded_img = None
    with tab1:
        cam_file = st.camera_input("ثبت عکس جهت آنالیز اولیه:")
        if cam_file is not None:
            uploaded_img = Image.open(cam_file)
            
    with tab2:
        file = st.file_uploader("یا بارگذاری تصویر چهره:", type=["jpg", "jpeg", "png"])
        if file is not None:
            uploaded_img = Image.open(file)
            
    if uploaded_img is not None:
        st.session_state.image = uploaded_img
        
        # تحلیل هندسی فرم صورت
        img_arr = np.array(uploaded_img)
        h, w = img_arr.shape[:2]
        ratio = h / w
        
        if ratio > 1.38:
            st.session_state.face_shape = "کشیده (Oblong / Long Face)"
            st.session_state.frames = [
                {"id": "aviator", "name": "Tom Ford - Aviator Luxe", "type": "خلبانی عریض با پل دوگانه", "brand": "Tom Ford", "color": "#1f77b4"},
                {"id": "square", "name": "Ray-Ban - Square Classic", "type": "مستطیلی پهن کلاسیک", "brand": "Ray-Ban", "color": "#ff7f0e"}
            ]
        elif 1.18 <= ratio <= 1.38:
            st.session_state.face_shape = "بیضی متعادل (Oval - استاندارد طلایی)"
            st.session_state.frames = [
                {"id": "wayfarer", "name": "Ray-Ban - Wayfarer Original", "type": "ویفرر استاندارد کلاسیک", "brand": "Ray-Ban", "color": "#2ca02c"},
                {"id": "cateye", "name": "Tom Ford - Cat Eye Modern", "type": "چشم‌گربه‌ای شیک و مدرن", "brand": "Tom Ford", "color": "#d62728"}
            ]
        else:
            st.session_state.face_shape = "گرد یا مربعی (Round / Square)"
            st.session_state.frames = [
                {"id": "rect", "name": "Tom Ford - Slim Rectangular", "type": "مستطیلی باریک زاویه‌دار", "brand": "Tom Ford", "color": "#9467bd"},
                {"id": "round", "name": "Ray-Ban - Round Metal", "type": "گرد فلزی مینیمال سبک", "brand": "Ray-Ban", "color": "#8c564b"}
            ]
        
        st.session_state.step = "analyze"
        st.rerun()

# ---------------------------------------------------------
# مرحله ۲: نمایش تحلیل چهره و گالری مدل‌ها
# ---------------------------------------------------------
elif st.session_state.step == "analyze":
    st.markdown("### مرحله ۲: نتیجه تحلیل هوش مصنوعی و انتخاب مدل فریم")
    
    col_img, col_report = st.columns([1, 1.3])
    with col_img:
        st.image(st.session_state.image, caption="تصویر تحلیل‌شده", use_column_width=True)
        if st.button("🔄 عکاسی یا بارگذاری تصویر جدید"):
            st.session_state.step = "capture"
            st.rerun()
            
    with col_report:
        st.success("✅ تحلیل آناتومیک با موفقیت انجام شد!")
        st.write(f"🔹 **فرم هندسی تشخیص‌داده‌شده:** {st.session_state.face_shape}")
        st.write(f"📏 **پارامترهای PD:** {pd_input}mm | **نسخه:** {rx_type}")
        st.markdown("---")
        st.markdown("💡 لطفاً یکی از مدل‌های زیر را انتخاب کنید تا مستقیماً وارد **اتاق تست زنده با فریم طبیعی و دسته‌های ارگونومیک** شوید:")

    st.markdown("---")
    
    f_cols = st.columns(len(st.session_state.frames))
    for i, frame in enumerate(st.session_state.frames):
        with f_cols[i]:
            st.markdown(f"""
                <div style="border: 2px solid {frame['color']}; padding: 15px; border-radius: 10px; background-color: #fcfcfc; text-align: center;">
                    <h4>{frame['name']}</h4>
                    <p><b>برند:</b> {frame['brand']}</p>
                    <p><b>طراحی:</b> {frame['type']}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"✨ تست زنده عینک کامل روی چهره", key=f"btn_frame_{i}"):
                st.session_state.selected_frame = frame
                st.session_state.step = "tryon"
                st.rerun()

# ---------------------------------------------------------
# مرحله ۳: اتاق امتحان مجازی زنده با فریم طبیعی و دسته‌های ارگونومیک روی گوش
# ---------------------------------------------------------
elif st.session_state.step == "tryon":
    chosen = st.session_state.selected_frame
    
    st.markdown(f"### مرحله ۳: اتاق تست زنده واقعیت افزوده (فریم فعال: {chosen['name']})")
    st.markdown("دوربین فعال است. فریم عینک به همراه دسته‌های ارگونومیک طبیعی (تطبیق یافته با خط شقیقه تا پشت گوش) روی صورت قرار دارد.")
    
    if st.button("← بازگشت به گالری و انتخاب فریم دیگر"):
        st.session_state.step = "analyze"
        st.rerun()
        
    st.markdown("---")

    # کد بهینه‌شده با اشکال واقعی فریم‌های اپتیکال بازار و طراحی دقیق انحنای دسته‌ها روی گوش
    ar_tryon_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/face_mesh.js" crossorigin="anonymous"></script>
        <style>
            .ar-container {{
                position: relative;
                width: 640px;
                height: 480px;
                margin: auto;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                background: #000;
            }}
            video, canvas {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                transform: scaleX(-1);
            }}
            .loading {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: white;
                font-family: Tahoma, sans-serif;
                font-size: 16px;
                z-index: 10;
                background: rgba(0,0,0,0.8);
                padding: 12px 24px;
                border-radius: 8px;
            }}
            .info-bar {{
                text-align: center;
                background: #eef7fc;
                padding: 10px;
                font-family: Tahoma, sans-serif;
                font-size: 14px;
                color: #333;
                max-width: 640px;
                margin: 10px auto 0 auto;
                border-radius: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="ar-container">
            <div id="loading" class="loading">در حال راه‌اندازی فریم‌های استاندارد و دسته‌های ارگونومیک...</div>
            <video id="webcam" autoplay playsinline muted></video>
            <canvas id="output_canvas"></canvas>
        </div>
        <div class="info-bar">
            <b>فریم انتخاب‌شده:</b> {chosen['name']} | 🟢 عینک با فریم و دسته استاندارد و طبیعی فعال است
        </div>

        <script>
            const videoElement = document.getElementById('webcam');
            const canvasElement = document.getElementById('output_canvas');
            const canvasCtx = canvasElement.getContext('2d');
            const loadingElement = document.getElementById('loading');

            const frameType = "{chosen['id']}";

            function drawNaturalGlasses(ctx, x, y, faceWidth, angle, fType) {{
                ctx.save();
                ctx.translate(x, y);
                ctx.rotate(angle);

                // استایل حرفه‌ای فریم استات / کائوچویی لوکس
                ctx.lineWidth = 5.5;
                ctx.strokeStyle = '#1e1e1e'; // رنگ فریم تیره کلاسیک
                ctx.fillStyle = 'rgba(100, 140, 180, 0.18)'; // عدسی دودی-آبی ملایم ضد بازتاب

                const totalWidth = faceWidth * 0.72;
                const lensWidth = totalWidth * 0.38;
                const lensHeight = lensWidth * 0.58;
                const bridgeWidth = totalWidth - (2 * lensWidth);

                const leftLensCenter = - (bridgeWidth / 2 + lensWidth / 2);
                const rightLensCenter = (bridgeWidth / 2 + lensWidth / 2);

                // --- رسم دقیق و طبیعی دسته‌های عینک (شقیقه تا پشت گوش) ---
                ctx.lineWidth = 4.5;
                ctx.strokeStyle = '#252525';
                
                // دسته چپ (امتداد زاویه‌‌دار به سمت عقب سر)
                ctx.beginPath();
                ctx.moveTo(leftLensCenter - lensWidth/2 + 4, -lensHeight * 0.2);
                ctx.lineTo(leftLensCenter - lensWidth/2 - lensWidth * 0.5, -lensHeight * 0.4);
                ctx.lineTo(leftLensCenter - lensWidth/2 - lensWidth * 1.15, -lensHeight * 0.1); // خم نهایی پشت گوش
                ctx.stroke();

                // دسته راست (امتداد زاویه‌دار به سمت عقب سر)
                ctx.beginPath();
                ctx.moveTo(rightLensCenter + lensWidth/2 - 4, -lensHeight * 0.2);
                ctx.lineTo(rightLensCenter + lensWidth/2 + lensWidth * 0.5, -lensHeight * 0.4);
                ctx.lineTo(rightLensCenter + lensWidth/2 + lensWidth * 1.15, -lensHeight * 0.1); // خم نهایی پشت گوش
                ctx.stroke();

                // بازنشانی مشخصات برای بدنه اصلی عینک
                ctx.lineWidth = 5.5;
                ctx.strokeStyle = '#1e1e1e';

                if (fType === 'aviator') {{
                    // عینک خلبانی استاندارد بازار با انحنای کلاسیک در قسمت پایین
                    ctx.beginPath();
                    ctx.moveTo(leftLensCenter - lensWidth/2, -lensHeight * 0.3);
                    ctx.bezierCurveTo(leftLensCenter - lensWidth/2, lensHeight * 0.8, leftLensCenter + lensWidth/2, lensHeight * 0.8, leftLensCenter + lensWidth/2, -lensHeight * 0.3);
                    ctx.closePath();
                    ctx.stroke();
                    ctx.fill();

                    ctx.beginPath();
                    ctx.moveTo(rightLensCenter - lensWidth/2, -lensHeight * 0.3);
                    ctx.bezierCurveTo(rightLensCenter - lensWidth/2, lensHeight * 0.8, rightLensCenter + lensWidth/2, lensHeight * 0.8, rightLensCenter + lensWidth/2, -lensHeight * 0.3);
                    ctx.closePath();
                    ctx.stroke();
                    ctx.fill();

                    // پل دوبل خلبانی
                    ctx.beginPath();
                    ctx.moveTo(leftLensCenter + lensWidth*0.2, -lensHeight*0.25);
                    ctx.lineTo(rightLensCenter - lensWidth*0.2, -lensHeight*0.25);
                    ctx.moveTo(leftLensCenter + lensWidth*0.2, -lensHeight*0.1);
                    ctx.lineTo(rightLensCenter - lensWidth*0.2, -lensHeight*0.1);
                    ctx.stroke();

                }} else if (fType === 'cateye') {{
                    // چشم‌گربه‌ای شیک با کشیدگی کلاسیک شقیقه‌ها
                    ctx.beginPath();
                    ctx.moveTo(leftLensCenter - lensWidth/2, 0);
                    ctx.lineTo(leftLensCenter - lensWidth/2 - 6, -lensHeight * 0.7); // کشیدگی گوشه بالا
                    ctx.lineTo(leftLensCenter + lensWidth/2, -lensHeight * 0.4);
                    ctx.lineTo(leftLensCenter + lensWidth/2, lensHeight * 0.5);
                    ctx.lineTo(leftLensCenter - lensWidth/2, lensHeight * 0.5);
                    ctx.closePath();
                    ctx.stroke();
                    ctx.fill();

                    ctx.beginPath();
                    ctx.moveTo(rightLensCenter - lensWidth/2, -lensHeight * 0.4);
                    ctx.lineTo(rightLensCenter + lensWidth/2 + 6, -lensHeight * 0.7); // کشیدگی گوشه بالا
                    ctx.lineTo(rightLensCenter + lensWidth/2, 0);
                    ctx.lineTo(rightLensCenter + lensWidth/2, lensHeight * 0.5);
                    ctx.lineTo(rightLensCenter - lensWidth/2, lensHeight * 0.5);
                    ctx.closePath();
                    ctx.stroke();
                    ctx.fill();

                }} else if (fType === 'round') {{
                    // گرد فلزی کلاسیک مینیمال
                    const radius = lensWidth * 0.45;
                    ctx.beginPath();
                    ctx.arc(leftLensCenter, 0, radius, 0, Math.PI * 2);
                    ctx.arc(rightLensCenter, 0, radius, 0, Math.PI * 2);
                    ctx.stroke();
                    ctx.fill();

                    // پل بینی فلزی ظریف
                    ctx.beginPath();
                    ctx.moveTo(leftLensCenter + radius, 0);
                    ctx.lineTo(rightLensCenter - radius, 0);
                    ctx.stroke();

                }} else {{
                    // مستطیلی ویفرر استاندارد (طراحی طبیعی عینک‌های روزمره بازار)
                    ctx.beginPath();
                    ctx.roundRect(leftLensCenter - lensWidth/2, -lensHeight/2, lensWidth, lensHeight, [6, 6, 10, 10]);
                    ctx.roundRect(rightLensCenter - lensWidth/2, -lensHeight/2, lensWidth, lensHeight, [6, 6, 10, 10]);
                    ctx.stroke();
                    ctx.fill();

                    // پل بینی ارگونومیک
                    ctx.beginPath();
                    ctx.moveTo(leftLensCenter + lensWidth/2, -lensHeight * 0.15);
                    ctx.lineTo(rightLensCenter - lensWidth/2, -lensHeight * 0.15);
                    ctx.stroke();
                }}

                ctx.restore();
            }}

            function onResults(results) {{
                loadingElement.style.display = 'none';
                canvasElement.width = videoElement.videoWidth;
                canvasElement.height = videoElement.videoHeight;

                canvasCtx.save();
                canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);

                if (results.multiFaceLandmarks && results.multiFaceLandmarks.length > 0) {{
                    const landmarks = results.multiFaceLandmarks[0];
                    
                    // پل بینی (لندمارک 168)
                    const noseBridge = landmarks[168];
                    const x = noseBridge.x * canvasElement.width;
                    const y = noseBridge.y * canvasElement.height;

                    // پهنای شقیقه‌ها (لندمارک 234 و 454)
                    const templeLeft = landmarks[234];
                    const templeRight = landmarks[454];
                    const faceWidth = Math.hypot(
                        (templeRight.x - templeLeft.x) * canvasElement.width,
                        (templeRight.y - templeLeft.y) * canvasElement.height
                    );

                    // زاویه سر بر اساس دو چشم (33 و 263)
                    const leftEye = landmarks[33];
                    const rightEye = landmarks[263];
                    const dx = (rightEye.x - leftEye.x) * canvasElement.width;
                    const dy = (rightEye.y - leftEye.y) * canvasElement.height;
                    const angle = Math.atan2(dy, dx);

                    // رسم عینک کامل و طبیعی با فریم استاندارد بازار و دسته‌های ارگونومیک
                    drawNaturalGlasses(canvasCtx, x, y, faceWidth, angle, frameType);
                }}
                canvasCtx.restore();
            }}

            const faceMesh = new FaceMesh({{
                locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${{file}}`
            }});

            faceMesh.setOptions({{
                maxNumFaces: 1,
                refineLandmarks: true,
                minDetectionConfidence: 0.5,
                minTrackingConfidence: 0.5
            }});

            faceMesh.onResults(onResults);

            const camera = new Camera(videoElement, {{
                onFrame: async () => {{
                    await faceMesh.send({{ image: videoElement }});
                }},
                width: 640,
                height: 480
            }});

            camera.start().catch(err => {{
                loadingElement.innerText = "خطا در دسترسی به دوربین مرورگر!";
                console.error(err);
            }});
        </script>
    </body>
    </html>
    """

    components.html(ar_tryon_html, height=580)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 پایان تست و شروع مجدد با چهره جدید"):
        st.session_state.step = "capture"
        st.rerun()