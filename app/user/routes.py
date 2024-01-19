from app.user import router
from app.user import controles


@router.post("/signup", status_code=200)
def signup():
    result = controles.user_signup()
    return result
