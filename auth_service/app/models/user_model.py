from .. import db

# ✅ Khai báo bảng phụ trước
user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),  # 🔧 'users.id' thay vì 'user.id'
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)   # 🔧 Nếu Role cũng đặt __tablename__ = 'roles'
)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=True)
    code = db.Column(db.String(50), nullable=True)
    expired_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    roles = db.relationship(
        'Role',
        secondary=user_roles,
        backref=db.backref('users', lazy='dynamic')
    )
