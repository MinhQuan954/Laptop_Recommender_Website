from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import db, User, Laptop, Favorite
from config import Config

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(Config)
    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/")
    def index():
        brands = db.session.query(Laptop.brand).distinct().all()
        return render_template("index.html", brands=[b[0] for b in brands])

    @app.route("/laptops")
    def laptops():
        # Filters: brand, price_min, price_max, ram_gb, category, q
        query = Laptop.query
        brand = request.args.get("brand")
        if brand:
            query = query.filter(Laptop.brand == brand)

        price_min = request.args.get("price_min", type=int)
        price_max = request.args.get("price_max", type=int)
        if price_min is not None:
            query = query.filter(Laptop.price >= price_min)
        if price_max is not None:
            query = query.filter(Laptop.price <= price_max)

        ram_gb = request.args.get("ram_gb", type=int)
        if ram_gb:
            query = query.filter(Laptop.ram_gb >= ram_gb)

        category = request.args.get("category")
        if category:
            query = query.filter(Laptop.category == category)

        q = request.args.get("q")
        if q:
            like = f"%{q.lower()}%"
            query = query.filter(db.func.lower(Laptop.name).like(like))

        items = query.order_by(Laptop.price.asc()).all()
        brands = db.session.query(Laptop.brand).distinct().all()
        return render_template("laptops.html", items=items, brands=[b[0] for b in brands])

    @app.route("/laptop/<int:laptop_id>")
    def laptop_detail(laptop_id):
        item = Laptop.query.get_or_404(laptop_id)
        return render_template("laptop_detail.html", item=item)

    @app.route("/compare")
    def compare():
        ids = request.args.getlist("id", type=int)
        items = Laptop.query.filter(Laptop.id.in_(ids)).all() if ids else []
        
        # Tính toán thống kê so sánh
        if len(items) >= 2:
            # Tìm laptop có hiệu năng tốt nhất
            best_performance = max(items, key=lambda x: calculate_performance_score(x))
            
            # Tìm laptop có giá trị tốt nhất
            best_value = min(items, key=lambda x: x.price)
            
            # Tìm laptop có giá cao nhất và thấp nhất
            price_range = {
                'min': min(items, key=lambda x: x.price),
                'max': max(items, key=lambda x: x.price)
            }
            
            # Phân tích theo nhu cầu
            category_analysis = {}
            for item in items:
                if item.category not in category_analysis:
                    category_analysis[item.category] = []
                category_analysis[item.category].append(item)
            
            # Nhận xét theo tiêu chí
            # Điểm hiệu năng tổng hợp dùng calculate_performance_score (đã có)
            # Tỷ lệ giá/hiệu năng: price_performance = price / (score + 1) để tránh chia 0
            scored = [(it, calculate_performance_score(it)) for it in items]
            best_price_performance = min(scored, key=lambda t: (t[0].price / (t[1] + 1)))[0]
            
            return render_template("compare.html", 
                                 items=items, 
                                 best_performance=best_performance,
                                 best_value=best_value,
                                 price_range=price_range,
                                 category_analysis=category_analysis,
                                 best_price_performance=best_price_performance)
        
        return render_template("compare.html", items=items)

    @app.route("/api/compare_data")
    def api_compare_data():
        """API để lấy dữ liệu so sánh theo mode"""
        laptop_ids = request.args.getlist('id')
        mode = request.args.get('mode', 'plugged')  # plugged hoặc battery
        
        items = []
        for laptop_id in laptop_ids:
            laptop = Laptop.query.get(laptop_id)
            if laptop:
                items.append(laptop)
        
        # Chuẩn bị dữ liệu theo mode
        data = {
            'cpu_single_core': [],
            'cpu_multi_core': [],
            'gpu_score': []
        }
        
        for laptop in items:
            if mode == 'battery':
                data['cpu_single_core'].append({
                    'name': laptop.name,
                    'score': laptop.cpu_single_core_battery or 0
                })
                data['cpu_multi_core'].append({
                    'name': laptop.name,
                    'score': laptop.cpu_multi_core_battery or 0
                })
                data['gpu_score'].append({
                    'name': laptop.name,
                    'score': laptop.gpu_score_battery or 0
                })
            else:  # plugged
                data['cpu_single_core'].append({
                    'name': laptop.name,
                    'score': laptop.cpu_single_core_plugged or 0
                })
                data['cpu_multi_core'].append({
                    'name': laptop.name,
                    'score': laptop.cpu_multi_core_plugged or 0
                })
                data['gpu_score'].append({
                    'name': laptop.name,
                    'score': laptop.gpu_score_plugged or 0
                })
        
        return jsonify(data)

    # Admin routes
    def admin_required(f):
        """Decorator để kiểm tra quyền admin"""
        @login_required
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != 'admin':
                flash('Bạn không có quyền truy cập trang này!', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function

    @app.route("/admin")
    @admin_required
    def admin_dashboard():
        """Trang dashboard admin"""
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        # Lấy danh sách laptop với phân trang
        pagination = Laptop.query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        laptops = pagination.items
        
        # Thống kê
        stats = {
            'total_laptops': Laptop.query.count(),
            'total_users': User.query.count(),
            'total_favorites': Favorite.query.count(),
            'total_brands': db.session.query(Laptop.brand).distinct().count()
        }
        
        # Danh sách thương hiệu
        brands = [brand[0] for brand in db.session.query(Laptop.brand).distinct().all()]
        
        return render_template('admin/dashboard.html', 
                             laptops=laptops, 
                             pagination=pagination,
                             stats=stats,
                             brands=brands)

    @app.route("/admin/laptop/add", methods=["GET", "POST"])
    @admin_required
    def admin_add_laptop():
        """Thêm laptop mới"""
        if request.method == "POST":
            try:
                # Lấy dữ liệu từ form
                laptop = Laptop(
                    name=request.form['name'],
                    brand=request.form['brand'],
                    cpu=request.form['cpu'],
                    ram_gb=int(request.form['ram_gb']),
                    gpu=request.form['gpu'] or None,
                    storage=request.form['storage'],
                    screen=request.form['screen'],
                    price=int(request.form['price']),
                    category=request.form['category'],
                    battery_capacity=int(request.form['battery_capacity']) if request.form['battery_capacity'] else None,
                    battery_life_office=int(request.form['battery_life_office']) if request.form['battery_life_office'] else None,
                    battery_life_gaming=int(request.form['battery_life_gaming']) if request.form['battery_life_gaming'] else None,
                    cpu_single_core_plugged=int(request.form['cpu_single_core_plugged']) if request.form['cpu_single_core_plugged'] else None,
                    cpu_multi_core_plugged=int(request.form['cpu_multi_core_plugged']) if request.form['cpu_multi_core_plugged'] else None,
                    cpu_single_core_battery=int(request.form['cpu_single_core_battery']) if request.form['cpu_single_core_battery'] else None,
                    cpu_multi_core_battery=int(request.form['cpu_multi_core_battery']) if request.form['cpu_multi_core_battery'] else None,
                    gpu_score_plugged=int(request.form['gpu_score_plugged']) if request.form['gpu_score_plugged'] else None,
                    gpu_score_battery=int(request.form['gpu_score_battery']) if request.form['gpu_score_battery'] else None
                )
                
                # Xử lý upload hình ảnh
                if 'image' in request.files:
                    file = request.files['image']
                    if file and file.filename:
                        filename = secure_filename(file.filename)
                        # Tạo tên file unique
                        import time
                        timestamp = int(time.time())
                        name_without_ext = os.path.splitext(filename)[0]
                        ext = os.path.splitext(filename)[1]
                        unique_filename = f"{name_without_ext}_{timestamp}{ext}"
                        
                        # Lưu file
                        file_path = os.path.join('static', 'images', unique_filename)
                        file.save(file_path)
                        laptop.image_url = f'/static/images/{unique_filename}'
                
                db.session.add(laptop)
                db.session.commit()
                
                flash(f'Đã thêm laptop "{laptop.name}" thành công!', 'success')
                return redirect(url_for('admin_dashboard'))
                
            except Exception as e:
                db.session.rollback()
                flash(f'Lỗi khi thêm laptop: {str(e)}', 'danger')
        
        return render_template('admin/laptop_form.html', laptop=None)

    @app.route("/admin/laptop/<int:laptop_id>/edit", methods=["GET", "POST"])
    @admin_required
    def admin_edit_laptop(laptop_id):
        """Sửa laptop"""
        laptop = Laptop.query.get_or_404(laptop_id)
        
        if request.method == "POST":
            try:
                # Cập nhật dữ liệu
                laptop.name = request.form['name']
                laptop.brand = request.form['brand']
                laptop.cpu = request.form['cpu']
                laptop.ram_gb = int(request.form['ram_gb'])
                laptop.gpu = request.form['gpu'] or None
                laptop.storage = request.form['storage']
                laptop.screen = request.form['screen']
                laptop.price = int(request.form['price'])
                laptop.category = request.form['category']
                laptop.battery_capacity = int(request.form['battery_capacity']) if request.form['battery_capacity'] else None
                laptop.battery_life_office = int(request.form['battery_life_office']) if request.form['battery_life_office'] else None
                laptop.battery_life_gaming = int(request.form['battery_life_gaming']) if request.form['battery_life_gaming'] else None
                laptop.cpu_single_core_plugged = int(request.form['cpu_single_core_plugged']) if request.form['cpu_single_core_plugged'] else None
                laptop.cpu_multi_core_plugged = int(request.form['cpu_multi_core_plugged']) if request.form['cpu_multi_core_plugged'] else None
                laptop.cpu_single_core_battery = int(request.form['cpu_single_core_battery']) if request.form['cpu_single_core_battery'] else None
                laptop.cpu_multi_core_battery = int(request.form['cpu_multi_core_battery']) if request.form['cpu_multi_core_battery'] else None
                laptop.gpu_score_plugged = int(request.form['gpu_score_plugged']) if request.form['gpu_score_plugged'] else None
                laptop.gpu_score_battery = int(request.form['gpu_score_battery']) if request.form['gpu_score_battery'] else None
                
                # Xử lý upload hình ảnh mới
                if 'image' in request.files:
                    file = request.files['image']
                    if file and file.filename:
                        filename = secure_filename(file.filename)
                        import time
                        timestamp = int(time.time())
                        name_without_ext = os.path.splitext(filename)[0]
                        ext = os.path.splitext(filename)[1]
                        unique_filename = f"{name_without_ext}_{timestamp}{ext}"
                        
                        file_path = os.path.join('static', 'images', unique_filename)
                        file.save(file_path)
                        laptop.image_url = f'/static/images/{unique_filename}'
                
                db.session.commit()
                flash(f'Đã cập nhật laptop "{laptop.name}" thành công!', 'success')
                return redirect(url_for('admin_dashboard'))
                
            except Exception as e:
                db.session.rollback()
                flash(f'Lỗi khi cập nhật laptop: {str(e)}', 'danger')
        
        return render_template('admin/laptop_form.html', laptop=laptop)

    @app.route("/admin/laptop/<int:laptop_id>/delete", methods=["POST"])
    @admin_required
    def admin_delete_laptop(laptop_id):
        """Xóa laptop (yêu cầu xác nhận)"""
        laptop = Laptop.query.get_or_404(laptop_id)
        laptop_name = laptop.name
        
        # Kiểm tra xác nhận từ form
        confirm = request.form.get('confirm')
        if not confirm:
            flash('Bạn chưa xác nhận xóa. Thao tác đã bị hủy.', 'warning')
            return redirect(url_for('admin_dashboard'))
        
        try:
            db.session.delete(laptop)
            db.session.commit()
            flash(f'Đã xóa laptop "{laptop_name}" thành công!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi khi xóa laptop: {str(e)}', 'danger')
        
        return redirect(url_for('admin_dashboard'))

    def calculate_performance_score(laptop):
        """Tính điểm hiệu năng cho laptop"""
        score = 0
        
        # Điểm cho CPU
        if 'H' in laptop.cpu or 'HX' in laptop.cpu or 'HK' in laptop.cpu:
            score += 30
        elif 'P' in laptop.cpu:
            score += 20
        else:
            score += 10
        
        # Điểm cho RAM
        if laptop.ram_gb >= 16:
            score += 25
        elif laptop.ram_gb >= 8:
            score += 15
        else:
            score += 5
        
        # Điểm cho GPU
        if laptop.gpu:
            if 'rtx' in laptop.gpu.lower() or 'gtx' in laptop.gpu.lower():
                score += 30
            elif 'mx' in laptop.gpu.lower() or 'iris' in laptop.gpu.lower():
                score += 15
        
        # Điểm cho storage
        if 'ssd' in laptop.storage.lower():
            score += 15
        
        return score

    @app.route("/register", methods=["GET","POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username","").strip()
            email = request.form.get("email","").strip()
            password = request.form.get("password","").strip()
            
            # Validation
            errors = []
            
            if not username or not email or not password:
                errors.append("Vui lòng điền đầy đủ thông tin")
            
            if username and len(username) < 3:
                errors.append("Tên đăng nhập phải có ít nhất 3 ký tự")
            
            if username and len(username) > 20:
                errors.append("Tên đăng nhập không được quá 20 ký tự")
            
            if email and '@' not in email:
                errors.append("Email không hợp lệ")
            
            if password and len(password) < 6:
                errors.append("Mật khẩu phải có ít nhất 6 ký tự")
            
            # Kiểm tra username và email đã tồn tại
            if username and User.query.filter_by(username=username).first():
                errors.append("Tên đăng nhập đã tồn tại")
            
            if email and User.query.filter_by(email=email).first():
                errors.append("Email đã được sử dụng")
            
            if errors:
                for error in errors:
                    flash(error, "danger")
                return redirect(url_for("register"))
            
            # Tạo tài khoản mới
            try:
                u = User(username=username, email=email)
                u.set_password(password)
                db.session.add(u)
                db.session.commit()
                flash("Đăng ký thành công! Vui lòng đăng nhập.", "success")
                return redirect(url_for("login"))
            except Exception as e:
                db.session.rollback()
                flash("Có lỗi xảy ra khi đăng ký. Vui lòng thử lại.", "danger")
                return redirect(url_for("register"))
        
        return render_template("register.html")

    @app.route("/login", methods=["GET","POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username","").strip()
            password = request.form.get("password","").strip()
            
            # Validation
            if not username or not password:
                flash("Vui lòng nhập đầy đủ thông tin đăng nhập", "danger")
                return redirect(url_for("login"))
            
            # Tìm user
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                login_user(user)
                flash(f"Chào mừng {user.username} quay trở lại!", "success")
                
                # Redirect về trang trước đó nếu có
                next_page = request.args.get('next')
                if next_page and next_page.startswith('/'):
                    return redirect(next_page)
                return redirect(url_for("index"))
            else:
                flash("Tên đăng nhập hoặc mật khẩu không đúng", "danger")
        
        return render_template("login.html")

    @app.route("/profile")
    @login_required
    def profile():
        favorites = Favorite.query.filter_by(user_id=current_user.id).all()
        favorites_count = len(favorites)
        compare_count = 0  # Có thể thêm logic đếm số lần so sánh sau
        
        return render_template("profile.html", 
                             favorites=favorites,
                             favorites_count=favorites_count,
                             compare_count=compare_count)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Đã đăng xuất.", "info")
        return redirect(url_for("index"))

    @app.route("/favorites")
    @login_required
    def favorites():
        favs = Favorite.query.filter_by(user_id=current_user.id).all()
        items = [f.laptop for f in favs]
        return render_template("favorites.html", items=items)

    @app.route("/favorite/<int:laptop_id>", methods=["POST"])
    @login_required
    def add_favorite(laptop_id):
        if not Favorite.query.filter_by(user_id=current_user.id, laptop_id=laptop_id).first():
            db.session.add(Favorite(user_id=current_user.id, laptop_id=laptop_id))
            db.session.commit()
            flash("Đã thêm vào yêu thích.", "success")
        return redirect(url_for("laptop_detail", laptop_id=laptop_id))

    @app.route("/favorite/<int:laptop_id>/remove", methods=["POST"])
    @login_required
    def remove_favorite(laptop_id):
        fav = Favorite.query.filter_by(user_id=current_user.id, laptop_id=laptop_id).first()
        if fav:
            db.session.delete(fav)
            db.session.commit()
            flash("Đã bỏ yêu thích.", "info")
        return redirect(url_for("favorites"))

    # Thuật toán gợi ý chi tiết theo profile nhu cầu
    @app.route("/recommend")
    def recommend():
        need = request.args.get("need")  # office, student, gaming, design, dev
        budget = request.args.get("budget", type=int)  # VND
        priority = request.args.get("priority", "balanced")  # performance, budget, balanced
        
        query = Laptop.query
        
        # Định nghĩa tiêu chí cho từng loại nhu cầu
        criteria = {
            "gaming": {
                "min_ram": 16,
                "cpu_series": ["H", "HX", "HK"],  # CPU hiệu năng cao
                "gpu_required": True,  # Yêu cầu GPU rời
                "min_price": 15000000,  # Tối thiểu 15 triệu
                "weight": {
                    "gpu": 0.3,
                    "cpu": 0.25,
                    "ram": 0.2,
                    "price": 0.15,
                    "storage": 0.1
                }
            },
            "design": {
                "min_ram": 16,
                "cpu_series": ["H", "HX", "HK", "P"],  # CPU hiệu năng cao hoặc P-series
                "gpu_required": True,
                "min_price": 20000000,  # Tối thiểu 20 triệu
                "weight": {
                    "gpu": 0.25,
                    "cpu": 0.25,
                    "ram": 0.2,
                    "screen": 0.2,
                    "price": 0.1
                }
            },
            "dev": {
                "min_ram": 16,
                "cpu_series": ["H", "HX", "HK", "P", "U"],  # Linh hoạt hơn
                "gpu_required": False,
                "min_price": 12000000,  # Tối thiểu 12 triệu
                "weight": {
                    "cpu": 0.3,
                    "ram": 0.25,
                    "storage": 0.2,
                    "price": 0.15,
                    "gpu": 0.1
                }
            },
            "student": {
                "min_ram": 8,
                "cpu_series": ["U", "P", "H"],  # Linh hoạt
                "gpu_required": False,
                "min_price": 8000000,  # Tối thiểu 8 triệu
                "weight": {
                    "price": 0.4,
                    "cpu": 0.25,
                    "ram": 0.2,
                    "storage": 0.15
                }
            },
            "office": {
                "min_ram": 8,
                "cpu_series": ["U", "P"],  # CPU tiết kiệm điện
                "gpu_required": False,
                "min_price": 6000000,  # Tối thiểu 6 triệu
                "weight": {
                    "price": 0.5,
                    "cpu": 0.2,
                    "ram": 0.2,
                    "storage": 0.1
                }
            }
        }
        
        if need and need in criteria:
            crit = criteria[need]
            
            # Áp dụng các bộ lọc cơ bản
            if crit["min_ram"]:
                query = query.filter(Laptop.ram_gb >= crit["min_ram"])
            
            if crit["gpu_required"]:
                # Lọc laptop có GPU rời (không phải Intel UHD, AMD Radeon Graphics)
                query = query.filter(
                    ~Laptop.gpu.like('%Intel UHD%'),
                    ~Laptop.gpu.like('%AMD Radeon Graphics%'),
                    ~Laptop.gpu.like('%Intel Graphics%')
                )
            
            if budget:
                query = query.filter(Laptop.price <= budget)
            elif crit["min_price"]:
                query = query.filter(Laptop.price >= crit["min_price"])
            
            # Lấy tất cả laptop phù hợp
            candidates = query.all()
            
            # Tính điểm cho từng laptop
            scored_laptops = []
            for laptop in candidates:
                score = calculate_laptop_score(laptop, crit, priority)
                scored_laptops.append((laptop, score))
            
            # Sắp xếp theo điểm số
            scored_laptops.sort(key=lambda x: x[1], reverse=True)
            
            # Trả về top 10 laptop tốt nhất
            items = [laptop for laptop, score in scored_laptops[:10]]
            
        else:
            # Nếu không có nhu cầu cụ thể, trả về tất cả laptop
            if budget:
                query = query.filter(Laptop.price <= budget)
            items = query.order_by(Laptop.price.asc()).all()
        
        return render_template("laptops.html", items=items, recommendation_type=need)

    @app.route("/api/search_suggest")
    def api_search_suggest():
        q = request.args.get("q", "").strip()
        limit = min(request.args.get("limit", 3, type=int), 3)
        suggestions = []
        if len(q) >= 2:
            like = f"%{q.lower()}%"
            results = (Laptop.query
                       .filter(db.func.lower(Laptop.name).like(like))
                       .order_by(Laptop.price.asc())
                       .limit(limit)
                       .all())
            for it in results:
                suggestions.append({
                    "id": it.id,
                    "name": it.name,
                    "image_url": it.image_url,
                    "price": it.price
                })
        return jsonify({"items": suggestions})

    @app.route("/api/products")
    def api_products():
        """API để lấy danh sách sản phẩm cho trang chủ"""
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 9, type=int)
        
        # Lấy sản phẩm với phân trang
        pagination = Laptop.query.order_by(Laptop.price.asc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        products = []
        for laptop in pagination.items:
            products.append({
                "id": laptop.id,
                "name": laptop.name,
                "brand": laptop.brand,
                "cpu": laptop.cpu,
                "ram_gb": laptop.ram_gb,
                "gpu": laptop.gpu,
                "storage": laptop.storage,
                "screen": laptop.screen,
                "price": laptop.price,
                "category": laptop.category,
                "image_url": laptop.image_url
            })
        
        return jsonify({
            "products": products,
            "has_next": pagination.has_next,
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": page
        })

    return app

def calculate_laptop_score(laptop, criteria, priority):
    """
    Tính điểm cho laptop dựa trên tiêu chí và ưu tiên
    """
    score = 0
    weights = criteria["weight"]
    
    # Điểm cho CPU
    cpu_score = 0
    cpu_series = criteria.get("cpu_series", [])
    for series in cpu_series:
        if series in laptop.cpu.upper():
            cpu_score = 1.0
            break
    if not cpu_score and "U" in laptop.cpu.upper():
        cpu_score = 0.5  # CPU U-series cơ bản
    
    # Điểm cho RAM
    ram_score = min(laptop.ram_gb / 32.0, 1.0)  # Chuẩn hóa theo 32GB
    
    # Điểm cho GPU
    gpu_score = 0
    if laptop.gpu:
        gpu_lower = laptop.gpu.lower()
        if any(gpu in gpu_lower for gpu in ['rtx', 'gtx', 'rx', 'radeon']):
            gpu_score = 1.0
        elif any(gpu in gpu_lower for gpu in ['mx', 'iris xe']):
            gpu_score = 0.6
        else:
            gpu_score = 0.3
    
    # Điểm cho giá (càng thấp càng tốt)
    price_score = 1.0 - (laptop.price / 50000000.0)  # Chuẩn hóa theo 50 triệu
    price_score = max(0, price_score)
    
    # Điểm cho storage
    storage_score = 0.5  # Mặc định
    if "ssd" in laptop.storage.lower():
        storage_score = 1.0
    elif "hdd" in laptop.storage.lower():
        storage_score = 0.3
    
    # Tính điểm tổng hợp
    score = (
        cpu_score * weights.get("cpu", 0.2) +
        ram_score * weights.get("ram", 0.2) +
        gpu_score * weights.get("gpu", 0.1) +
        price_score * weights.get("price", 0.3) +
        storage_score * weights.get("storage", 0.1)
    )
    
    # Điều chỉnh theo ưu tiên
    if priority == "performance":
        score *= 1.2  # Tăng 20% cho laptop hiệu năng cao
    elif priority == "budget":
        score *= 0.8  # Giảm 20% cho laptop giá rẻ
    
    return score

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        from models import db
        db.create_all()
    app.run(debug=True)
