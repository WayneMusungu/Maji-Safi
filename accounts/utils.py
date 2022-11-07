"""
This file will contain any helper function for myAccount
"""

def detectUser(user):
    if user.role == 1:
        redirectUrl = 'supplierDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'customerDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
        
    
        
    
    
        