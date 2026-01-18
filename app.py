"""
Thể Thao 24/7 - Flask Backend Application
Ứng dụng web tin tức thể thao với đầy đủ tính năng
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
import os
from functools import wraps

# Khởi tạo Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thethao247.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-key-change-in-production-2024'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Khởi tạo extensions
db = SQLAlchemy(app)
CORS(app)

# ==================== MODELS ====================

class User(db.Model):
    """Model User cho database"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    avatar = db.Column(db.String(10))
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        """Hash password trước khi lưu"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Kiểm tra password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'avatar': self.avatar,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Article(db.Model):
    """Model Article cho tin tức"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(300))
    image_url = db.Column(db.String(500))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert article to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'content': self.content,
            'excerpt': self.excerpt,
            'image_url': self.image_url,
            'views': self.views,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# ==================== DECORATORS ====================

def token_required(f):
    """Decorator để bảo vệ routes cần authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'success': False, 'message': 'Token không tồn tại'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token.split(' ')[1]
            
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            
            if not current_user:
                return jsonify({'success': False, 'message': 'User không tồn tại'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'message': 'Token đã hết hạn'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'message': 'Token không hợp lệ'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

# ==================== ROUTES - WEB PAGES ====================

@app.route('/')
def index():
    """Trang chủ"""
    return render_template('index.html')

@app.route('/login')
def login_page():
    """Trang đăng nhập"""
    return render_template('login.html')

@app.route('/register')
def register_page():
    """Trang đăng ký"""
    return render_template('register.html')

@app.route('/category/<category_name>')
def category_page(category_name):
    """Trang danh mục"""
    return render_template('category.html', category=category_name)

@app.route('/article/<int:article_id>')
def article_page(article_id):
    """Trang chi tiết bài viết"""
    return render_template('article.html', article_id=article_id)

@app.route('/profile')
def profile_page():
    """Trang profile người dùng"""
    return render_template('profile.html')

@app.route('/search')
def search_page():
    """Trang tìm kiếm"""
    query = request.args.get('q', '')
    return render_template('search.html', query=query)

# ==================== API ROUTES - AUTHENTICATION ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """API đăng ký user mới"""
    try:
        data = request.get_json()
        
        # Validation
        if not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Vui lòng điền đầy đủ thông tin'
            }), 400
        
        if data.get('password') != data.get('confirmPassword'):
            return jsonify({
                'success': False,
                'message': 'Mật khẩu xác nhận không khớp'
            }), 400
        
        # Kiểm tra email đã tồn tại
        if User.query.filter_by(email=data['email']).first():
            return jsonify({
                'success': False,
                'message': 'Email này đã được đăng ký'
            }), 400
        
        # Tạo user mới
        new_user = User(
            name=data['name'],
            email=data['email'],
            avatar=data['name'][0].upper()
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        # Tạo JWT token
        token = jwt.encode({
            'user_id': new_user.id,
            'exp': datetime.utcnow() + timedelta(days=7)
        }, app.config['JWT_SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'success': True,
            'message': 'Đăng ký thành công!',
            'data': {
                'user': new_user.to_dict(),
                'token': token
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """API đăng nhập"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Vui lòng nhập email và mật khẩu'
            }), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({
                'success': False,
                'message': 'Email hoặc mật khẩu không đúng'
            }), 401
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Tạo JWT token
        token_expiry = timedelta(days=30) if data.get('rememberMe') else timedelta(days=7)
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + token_expiry
        }, app.config['JWT_SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'success': True,
            'message': 'Đăng nhập thành công!',
            'data': {
                'user': user.to_dict(),
                'token': token
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500

@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """API lấy thông tin user hiện tại"""
    return jsonify({
        'success': True,
        'data': {
            'user': current_user.to_dict()
        }
    })

@app.route('/api/auth/logout', methods=['POST'])
@token_required
def logout(current_user):
    """API đăng xuất"""
    return jsonify({
        'success': True,
        'message': 'Đăng xuất thành công'
    })

# ==================== API ROUTES - ARTICLES ====================

@app.route('/api/articles', methods=['GET'])
def get_articles():
    """API lấy danh sách tin tức"""
    try:
        category = request.args.get('category')
        limit = request.args.get('limit', 10, type=int)
        
        query = Article.query
        
        if category:
            query = query.filter_by(category=category)
        
        articles = query.order_by(Article.created_at.desc()).limit(limit).all()
        
        return jsonify({
            'success': True,
            'data': {
                'articles': [article.to_dict() for article in articles]
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500

@app.route('/api/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """API lấy chi tiết một tin tức"""
    try:
        article = Article.query.get(article_id)
        
        if not article:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy bài viết'
            }), 404
        
        # Tăng lượt xem
        article.views += 1
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'article': article.to_dict()
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500

@app.route('/api/articles', methods=['POST'])
@token_required
def create_article(current_user):
    """API tạo tin tức mới (chỉ admin)"""
    try:
        if current_user.role != 'admin':
            return jsonify({
                'success': False,
                'message': 'Bạn không có quyền tạo bài viết'
            }), 403
        
        data = request.get_json()
        
        new_article = Article(
            title=data['title'],
            category=data['category'],
            content=data['content'],
            excerpt=data.get('excerpt'),
            image_url=data.get('image_url'),
            author_id=current_user.id
        )
        
        db.session.add(new_article)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tạo bài viết thành công',
            'data': {
                'article': new_article.to_dict()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500

# ==================== UTILITY FUNCTIONS ====================

def init_sample_data():
    """Khởi tạo dữ liệu mẫu"""
    # Kiểm tra xem đã có dữ liệu chưa
    if User.query.first() or Article.query.first():
        return
    
    print("🔄 Đang tạo dữ liệu mẫu...")
    
    # Tạo admin user
    admin = User(
        name='Admin',
        email='admin@thethao247.vn',
        avatar='A',
        role='admin'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Tạo user thường
    user = User(
        name='Nguyễn Văn A',
        email='user@example.com',
        avatar='N'
    )
    user.set_password('123456')
    db.session.add(user)
    
    # Tạo bài viết mẫu
    sample_articles = [
        {
            'title': 'Ronaldo lập hat-trick, phá kỷ lục 800 bàn thắng',
            'category': 'Bóng đá',
            'content': 'Cristiano Ronaldo tiếp tục khẳng định đẳng cấp siêu sao với cú hat-trick ấn tượng...',
            'excerpt': 'Siêu sao người Bồ Đào Nha lập cú hat-trick lịch sử trong trận đấu tối qua',
            'image_url': 'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800&h=600&fit=crop',
            'author_id': 1
        },
        {
            'title': 'Quang Hải tỏa sáng tại AFC Champions League',
            'category': 'Bóng đá Việt Nam',
            'content': 'Tiền vệ Nguyễn Quang Hải đã có màn trình diễn ấn tượng trong trận đấu...',
            'excerpt': 'Ngôi sao CAHN ghi bàn thắng đẹp mắt giúp đội nhà giành chiến thắng',
            'image_url': 'https://images.unsplash.com/photo-1574068468668-a05a11f871da?w=800&h=600&fit=crop',
            'author_id': 1
        },
        {
            'title': 'Djokovic vs Nadal: Trận đấu kinh điển tại Australian Open',
            'category': 'Tennis',
            'content': 'Hai huyền thoại tennis thế giới sẽ đối đầu trong trận bán kết...',
            'excerpt': 'Cuộc đối đầu lần thứ 60 giữa hai tay vợt vĩ đại nhất mọi thời đại',
            'image_url': 'https://images.unsplash.com/photo-1554068865-24cecd4e34b8?w=800&h=600&fit=crop',
            'author_id': 1
        },
        {
            'title': 'LeBron James đạt cột mốc 40,000 điểm trong sự nghiệp',
            'category': 'Bóng rổ',
            'content': 'Ngôi sao của LA Lakers tiếp tục viết nên lịch sử NBA...',
            'excerpt': 'King James trở thành cầu thủ đầu tiên đạt mốc 40,000 điểm',
            'image_url': 'https://images.unsplash.com/photo-1519861531473-9200262188bf?w=800&h=600&fit=crop',
            'author_id': 1
        },
        {
            'title': 'Verstappen thống trị chặng đua Monaco',
            'category': 'Formula 1',
            'content': 'Tay đua Red Bull Racing giành pole position và chiến thắng...',
            'excerpt': 'Verstappen tiếp tục chuỗi thành tích ấn tượng trong mùa giải',
            'image_url': 'https://images.unsplash.com/photo-1586985289688-ca3cf47d3e6e?w=800&h=600&fit=crop',
            'author_id': 1
        }
    ]
    
    for article_data in sample_articles:
        article = Article(**article_data)
        db.session.add(article)
    
    db.session.commit()
    print("✅ Dữ liệu mẫu đã được tạo!")
    print("👤 Admin: admin@thethao247.vn / admin123")
    print("👤 User: user@example.com / 123456")

# ==================== APP INITIALIZATION ====================

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'Server đang hoạt động',
        'timestamp': datetime.utcnow().isoformat()
    })

# ==================== MAIN ====================

if __name__ == '__main__':
    with app.app_context():
        # Tạo database và tables
        db.create_all()
        # Khởi tạo dữ liệu mẫu
        init_sample_data()
    
    print("\n" + "="*60)
    print("🏆 THỂ THAO 24/7 - SERVER ĐANG CHẠY")
    print("="*60)
    print("🌐 URL: http://localhost:5000")
    print("📊 Admin Panel: http://localhost:5000/login")
    print("="*60 + "\n")
    
    # Chạy Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
