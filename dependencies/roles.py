from fastapi import Depends, HTTPException, status
from auth_service import get_current_user
from models import User

def admin_required(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only!"
        )
    return user
