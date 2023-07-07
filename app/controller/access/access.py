from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt

from app.models.User import Bookkeeping_account, Money_bookkeeping_role


# cara pengguaan, di atasnyya dibuat dulu
# variabel akses yang isinya user yang diijinkan
@jwt_required()
# melihat role user
def WhoAreYou(akses):
    user_id = get_jwt_identity()
    jwt_data = get_jwt()
    nested_session = jwt_data['nested_session']
    bookkeeping_id = nested_session.get('data')

    account = Bookkeeping_account.query.filter_by(user_id=user_id).first()
    role = Money_bookkeeping_role.query.filter_by(role_id=account.role_id).first()

    if account.bookkeeping_account_id == bookkeeping_id:
        if role.role_name in akses:
            return True
        else:
            return False
    else:
        return False