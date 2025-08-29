from app import create_app
from models import db, User

def create_test_users():
    app = create_app()
    with app.app_context():
        # Kiểm tra xem đã có user nào chưa
        existing_users = User.query.all()
        if existing_users:
            print("Đã có tài khoản trong hệ thống:")
            for user in existing_users:
                print(f"- {user.username} ({user.email})")
            return
        
        # Tạo tài khoản test
        test_users = [
            {
                'username': 'admin',
                'email': 'admin@example.com',
                'password': 'admin123'
            },
            {
                'username': 'user1',
                'email': 'user1@example.com',
                'password': 'user123'
            },
            {
                'username': 'test',
                'email': 'test@example.com',
                'password': 'test123'
            }
        ]
        
        for user_data in test_users:
            user = User(username=user_data['username'], email=user_data['email'])
            user.set_password(user_data['password'])
            db.session.add(user)
            print(f"Đã tạo tài khoản: {user_data['username']} (Mật khẩu: {user_data['password']})")
        
        db.session.commit()
        print("\n✅ Đã tạo thành công các tài khoản test!")
        print("\n📋 Thông tin đăng nhập:")
        print("=" * 40)
        for user_data in test_users:
            print(f"👤 {user_data['username']}")
            print(f"📧 {user_data['email']}")
            print(f"🔑 {user_data['password']}")
            print("-" * 20)

if __name__ == "__main__":
    create_test_users() 