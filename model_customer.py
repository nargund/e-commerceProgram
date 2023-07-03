from model_user import User

"""
This class is the main class for customers they are initialized and handled

Name: Pavan Ramesh Nargund
Student Id: 33503575
Create date: 30-05-2023
Final date: 30-05-2023
"""

class Customer(User):
    
    default_customer_email = "default@monash.edu"
    default_customer_mobile = "04xxxxxxxx"
    
    def __init__(
        self, 
        user_id:str = User.default_user_id,
        user_name:str = User.default_user_name,
        user_password:str = User.default_user_password,
        user_register_time:str = User.default_register_time,
        user_role:str = User.customer_role,
        user_email:str = default_customer_email,
        user_mobile:str = default_customer_mobile
     ):
        """
        This method initilaizes customer instances, overrides from User

        Parameters
        ----------
        user_id : str, optional
            DESCRIPTION. The default is User.default_user_id.
        user_name : str, optional
            DESCRIPTION. The default is User.default_user_name.
        user_password : str, optional
            DESCRIPTION. The default is User.default_user_password.
        user_register_time : str, optional
            DESCRIPTION. The default is User.default_register_time.
        user_role : str, optional
            DESCRIPTION. The default is User.customer_role.
        user_email : str, optional
            DESCRIPTION. The default is default_customer_email.
        user_mobile : str, optional
            DESCRIPTION. The default is default_customer_mobile.

        Returns
        -------
        None.

        """
        super().__init__(user_id,user_name,user_password,user_register_time,\
                         user_role)
        self.user_email = user_email
        self.user_mobile = user_mobile
        
    def __str__(
        self
    )->str:
        """
        specific way of printing instances 

        Returns
        -------
        str
            DESCRIPTION.

        """
        return super().__str__()
        
        