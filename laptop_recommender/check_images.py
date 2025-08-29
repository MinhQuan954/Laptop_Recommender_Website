from app import create_app
from models import db, Laptop

def check_images():
    app = create_app()
    with app.app_context():
        laptops = Laptop.query.all()
        
        print("🎉 KẾT QUẢ CẬP NHẬT HÌNH ẢNH")
        print("=" * 60)
        
        # Thống kê
        total = len(laptops)
        with_real_images = 0
        with_placeholders = 0
        without_images = 0
        
        for laptop in laptops:
            if laptop.image_url:
                if 'webp' in laptop.image_url or 'jpg' in laptop.image_url:
                    with_real_images += 1
                    status = "✅"
                elif 'placeholder' in laptop.image_url:
                    with_placeholders += 1
                    status = "🎨"
                else:
                    without_images += 1
                    status = "❓"
            else:
                without_images += 1
                status = "❌"
            
            image_name = laptop.image_url.split('/')[-1] if laptop.image_url else "Không có"
            print(f"{status} {laptop.name}")
            print(f"   📸 {image_name}")
        
        print("\n" + "=" * 60)
        print("📊 THỐNG KÊ CUỐI CÙNG:")
        print(f"   🖼️  Có hình thật: {with_real_images}/{total}")
        print(f"   🎨 Có placeholder: {with_placeholders}/{total}")
        print(f"   ❌ Không có hình: {without_images}/{total}")
        
        if with_real_images == total:
            print("\n🎉 HOÀN HẢO! Tất cả laptop đều có hình ảnh thật!")
        elif with_real_images > total * 0.8:
            print(f"\n👍 Tuyệt vời! {with_real_images}/{total} laptop có hình ảnh thật!")
        else:
            print(f"\n⚠️  Cần cải thiện: Chỉ {with_real_images}/{total} laptop có hình ảnh thật")

if __name__ == "__main__":
    check_images() 